"""Thin wrapper around the focusconsulting/formspec Python library.

`formspec-py` is alpha (0.1.0). We isolate every call to it behind this
module so the rest of the Django app doesn't import it directly. That
makes future version upgrades, error handling, and the "library not
installed" fallback path easy to manage in one place.

Used by:
  - staff_review.form_builder_views (lint definitions, surface diagnostics)
  - form_manager submit / FormEntry save (validate response payloads)
  - the publish flow (auto-suggest the semver bump)

All public functions are safe to call with arbitrary input -- they
never raise on bad data; they return a structured result the caller
can inspect.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from formspec import (
        evaluate_definition,
        generate_changelog,
        lint as _formspec_lint,
    )
    FORMSPEC_AVAILABLE = True
except ImportError:  # pragma: no cover -- defensive only
    FORMSPEC_AVAILABLE = False


# Path to the built-in formspec docs we ship with the prototype.
# Today only the Tribal Plan; more will land as we port more forms.
FORMSPEC_DOCS_DIR = Path(__file__).resolve().parent.parent / "formspec_docs"


# ---- Data classes ------------------------------------------------------

@dataclass(frozen=True)
class Diagnostic:
    code: str
    severity: str    # "error" | "warning" | "info"
    path: str
    message: str


@dataclass(frozen=True)
class LintReport:
    diagnostics: list[Diagnostic]

    @property
    def error_count(self) -> int:
        return sum(1 for d in self.diagnostics if d.severity == "error")

    @property
    def warning_count(self) -> int:
        return sum(1 for d in self.diagnostics if d.severity == "warning")

    @property
    def is_clean(self) -> bool:
        return self.error_count == 0

    @property
    def errors(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == "error"]

    @property
    def warnings(self) -> list[Diagnostic]:
        return [d for d in self.diagnostics if d.severity == "warning"]


@dataclass(frozen=True)
class ValidationResult:
    valid: bool
    item_count: int          # how many items the engine processed
    data: dict[str, Any]     # post-NRB normalized data (or original on failure)
    raw: Any = None          # the underlying ProcessingResult, for debugging


# ---- Public API --------------------------------------------------------

def lint_definition(schema: dict, mode: str = "strict") -> LintReport:
    """Lint a formspec definition. Returns LintReport regardless of input.

    `mode` matches formspec-py's lint modes:
      "strict"    -- full schema + structural checks (default for Form Builder)
      "authoring" -- more lenient, for in-progress drafts
    """
    if not FORMSPEC_AVAILABLE:
        return LintReport(diagnostics=[Diagnostic(
            code="X000", severity="warning", path="$",
            message="formspec-py is not installed; lint skipped.",
        )])
    if not isinstance(schema, dict) or not schema:
        return LintReport(diagnostics=[Diagnostic(
            code="X001", severity="error", path="$",
            message="No formspec definition provided.",
        )])
    try:
        raw = _formspec_lint(schema, mode=mode)
    except Exception as exc:
        return LintReport(diagnostics=[Diagnostic(
            code="X002", severity="error", path="$",
            message=f"Lint failed to run: {exc}",
        )])
    return LintReport(diagnostics=[
        Diagnostic(code=d.code, severity=d.severity, path=d.path, message=d.message)
        for d in raw
    ])


def validate_response(schema: dict, data: dict) -> ValidationResult:
    """Run a response payload through the formspec evaluator.

    Used on FormEntry save / submit. Defense-in-depth -- the client
    renderer already validated, but we always re-check on the server.
    """
    if not FORMSPEC_AVAILABLE or not isinstance(schema, dict) or not schema:
        # No spec to validate against -- treat as valid so we don't block
        # FormEntries on forms that haven't been ported yet.
        return ValidationResult(valid=True, item_count=0, data=data or {}, raw=None)
    try:
        raw = evaluate_definition(schema, data or {})
    except Exception as exc:  # pragma: no cover -- defensive
        return ValidationResult(valid=False, item_count=0, data=data or {}, raw=str(exc))
    return ValidationResult(
        valid=bool(getattr(raw, "valid", False)),
        item_count=int(getattr(raw, "counts", {}).get("total", 0)) if hasattr(raw, "counts") else 0,
        data=getattr(raw, "data", data) or data or {},
        raw=raw,
    )


def changelog_between(old_schema: dict, new_schema: dict, url: str = "") -> dict:
    """Compare two formspec definitions, return a changelog + suggested bump.

    Returned dict (subset of formspec-py's shape):
      {
        "suggested_bump": "major" | "minor" | "patch",
        "changes": [...]
      }
    """
    if not FORMSPEC_AVAILABLE:
        return {"suggested_bump": "minor", "changes": [], "_error": "formspec-py not installed"}
    if not (isinstance(old_schema, dict) and isinstance(new_schema, dict)):
        return {"suggested_bump": "minor", "changes": [], "_error": "missing schema"}
    try:
        raw = generate_changelog(old_schema, new_schema, url or "https://core.acf.gov/spec")
    except Exception as exc:
        return {"suggested_bump": "minor", "changes": [], "_error": str(exc)}
    # generate_changelog returns a structured object; project the bits Form Builder needs
    bump = getattr(raw, "suggested_bump", None) or getattr(raw, "bump", "minor")
    changes = getattr(raw, "changes", []) or []
    return {
        "suggested_bump": str(bump).lower(),
        "changes": [str(c) for c in changes],
        "raw": raw,
    }


def load_builtin_spec(name: str) -> dict | None:
    """Read a packaged formspec doc from form_manager/formspec_docs/.

    `name` is the filename stem (e.g. "csbg_tribal_plan").
    """
    import json
    path = FORMSPEC_DOCS_DIR / f"{name}.json"
    if not path.exists():
        return None
    return json.loads(path.read_text())
