"""Visual Form Builder schema editor (STAFF-MP-14).

Pure functions that add / update / remove / reorder *sections* and *fields*
on a formspec definition dict, plus the draft lifecycle helpers used by the
Form Builder edit view.

Design notes
------------
* Every mutation operates on a deep copy and returns a NEW dict -- callers
  never have to worry about aliasing the live model JSON.
* formspec requires GLOBALLY-unique item keys across the whole document, so
  `add_section` / `add_field` mint keys via `unique_key()` which slugifies the
  label and disambiguates against every existing key.
* Non-technical users pick a friendly field *type* ("Short text", "Email",
  "Dollar amount", ...). FIELD_TYPES maps each one to the formspec
  `dataType` (+ optional `semanticType` / `optionSet`). `field_type_of()` is
  the reverse mapping used to pre-select the right option when editing.
* The published `schema` is never mutated here. The view layer reads/writes
  `FormDefinition.draft_schema`; `get_draft_schema()` seeds a fresh draft from
  the published schema on first edit.

This module deliberately knows nothing about Django models except inside the
small `draft_*` helpers at the bottom, which are the only functions that read
or write the database.
"""

from __future__ import annotations

import copy
import re
from typing import Any

# ---------------------------------------------------------------------------
# Field type registry
# ---------------------------------------------------------------------------
# Order matters -- this is the order options appear in the "Field type" dropdown.
FIELD_TYPES: list[dict[str, Any]] = [
    {"key": "short_text", "label": "Short text",            "dataType": "string"},
    {"key": "long_text",  "label": "Long text (paragraph)", "dataType": "text"},
    {"key": "email",      "label": "Email address",         "dataType": "string", "semanticType": "email"},
    {"key": "phone",      "label": "Phone number",          "dataType": "string", "semanticType": "phone"},
    {"key": "money",      "label": "Dollar amount",         "dataType": "money"},
    {"key": "date",       "label": "Date",                  "dataType": "date"},
    {"key": "yes_no",     "label": "Yes / No",              "dataType": "boolean"},
    {"key": "dropdown",   "label": "Dropdown",              "dataType": "choice"},
]

_FIELD_TYPE_BY_KEY = {ft["key"]: ft for ft in FIELD_TYPES}
VALID_TYPE_KEYS = set(_FIELD_TYPE_BY_KEY)


def field_type_label(type_key: str) -> str:
    """Friendly label for a type key (for display)."""
    ft = _FIELD_TYPE_BY_KEY.get(type_key)
    return ft["label"] if ft else type_key


def field_type_of(field: dict) -> str:
    """Reverse-map a formspec field dict to one of our friendly type keys."""
    data_type = (field or {}).get("dataType")
    semantic = (field or {}).get("semanticType")
    if data_type == "text":
        return "long_text"
    if data_type == "money":
        return "money"
    if data_type == "date":
        return "date"
    if data_type == "boolean":
        return "yes_no"
    if data_type == "choice":
        return "dropdown"
    if data_type == "string" and semantic == "email":
        return "email"
    if data_type == "string" and semantic == "phone":
        return "phone"
    return "short_text"


# ---------------------------------------------------------------------------
# Key helpers
# ---------------------------------------------------------------------------
def slug(label: str) -> str:
    """Turn a human label into a camel-ish key base, e.g. 'Annual goals' -> 'annualGoals'."""
    words = re.findall(r"[A-Za-z0-9]+", (label or "").strip())
    if not words:
        return "field"
    head, *tail = [w.lower() for w in words]
    return head + "".join(w.capitalize() for w in tail)


def all_keys(schema: dict) -> set[str]:
    """Collect every `key` in the document (sections + their children)."""
    keys: set[str] = set()
    for section in (schema or {}).get("items", []) or []:
        if isinstance(section, dict) and section.get("key"):
            keys.add(section["key"])
        for child in section.get("children", []) or []:
            if isinstance(child, dict) and child.get("key"):
                keys.add(child["key"])
    return keys


def unique_key(schema: dict, base: str) -> str:
    """Return `base` (or base2, base3, ...) such that it's globally unique."""
    base = slug(base)
    existing = all_keys(schema)
    if base not in existing:
        return base
    n = 2
    while f"{base}{n}" in existing:
        n += 1
    return f"{base}{n}"


# ---------------------------------------------------------------------------
# Read helpers
# ---------------------------------------------------------------------------
def sections(schema: dict) -> list[dict]:
    """The top-level group items (sections)."""
    return [s for s in (schema or {}).get("items", []) or [] if isinstance(s, dict)]


def find_section(schema: dict, section_key: str) -> dict | None:
    for s in sections(schema):
        if s.get("key") == section_key:
            return s
    return None


def option_set_keys(schema: dict) -> list[str]:
    """Names of option sets available for Dropdown fields."""
    return sorted((schema or {}).get("optionSets", {}).keys())


# ---------------------------------------------------------------------------
# Field-dict construction
# ---------------------------------------------------------------------------
def build_field(
    schema: dict,
    *,
    label: str,
    type_key: str,
    help_text: str = "",
    option_set: str = "",
    key: str | None = None,
) -> dict:
    """Construct a formspec field dict for the given friendly type."""
    if type_key not in VALID_TYPE_KEYS:
        type_key = "short_text"
    ft = _FIELD_TYPE_BY_KEY[type_key]

    field: dict[str, Any] = {
        "type": "field",
        "key": key or unique_key(schema, label),
        "label": (label or "Untitled field").strip(),
        "dataType": ft["dataType"],
    }
    if ft.get("semanticType"):
        field["semanticType"] = ft["semanticType"]
    if ft["dataType"] == "choice":
        # Prefer the explicit choice; else fall back to the first option set.
        avail = option_set_keys(schema)
        chosen = option_set if option_set in avail else (avail[0] if avail else "")
        if chosen:
            field["optionSet"] = chosen
    if help_text and help_text.strip():
        field["extensions"] = {"x-help": help_text.strip()}
    return field


def field_help(field: dict) -> str:
    return ((field or {}).get("extensions", {}) or {}).get("x-help", "") or ""


# ---------------------------------------------------------------------------
# Section mutations (all return a new schema)
# ---------------------------------------------------------------------------
def add_section(schema: dict, label: str) -> dict:
    out = copy.deepcopy(schema)
    out.setdefault("items", [])
    section = {
        "type": "group",
        "key": unique_key(out, label or "section"),
        "label": (label or "New section").strip(),
        "extensions": {"x-section-number": len(out["items"]) + 1},
        "children": [],
    }
    out["items"].append(section)
    return _renumber_sections(out)


def update_section(schema: dict, section_key: str, label: str) -> dict:
    out = copy.deepcopy(schema)
    s = find_section(out, section_key)
    if s is not None and label and label.strip():
        s["label"] = label.strip()
    return out


def remove_section(schema: dict, section_key: str) -> dict:
    out = copy.deepcopy(schema)
    out["items"] = [s for s in sections(out) if s.get("key") != section_key]
    return _renumber_sections(out)


def move_section(schema: dict, section_key: str, direction: str) -> dict:
    out = copy.deepcopy(schema)
    items = sections(out)
    idx = next((i for i, s in enumerate(items) if s.get("key") == section_key), None)
    if idx is None:
        return out
    swap = idx - 1 if direction == "up" else idx + 1
    if 0 <= swap < len(items):
        items[idx], items[swap] = items[swap], items[idx]
        out["items"] = items
    return _renumber_sections(out)


def _renumber_sections(schema: dict) -> dict:
    """Keep x-section-number in sync with display order."""
    for i, s in enumerate(sections(schema), start=1):
        s.setdefault("extensions", {})
        s["extensions"]["x-section-number"] = i
    return schema


# ---------------------------------------------------------------------------
# Field mutations (all return a new schema)
# ---------------------------------------------------------------------------
def add_field(
    schema: dict,
    section_key: str,
    *,
    label: str,
    type_key: str,
    help_text: str = "",
    option_set: str = "",
) -> dict:
    out = copy.deepcopy(schema)
    s = find_section(out, section_key)
    if s is None:
        return out
    s.setdefault("children", [])
    s["children"].append(build_field(
        out, label=label, type_key=type_key, help_text=help_text, option_set=option_set,
    ))
    return out


def update_field(
    schema: dict,
    section_key: str,
    field_key: str,
    *,
    label: str,
    type_key: str,
    help_text: str = "",
    option_set: str = "",
) -> dict:
    out = copy.deepcopy(schema)
    s = find_section(out, section_key)
    if s is None:
        return out
    for i, child in enumerate(s.get("children", []) or []):
        if child.get("key") == field_key:
            # Rebuild the field but KEEP the existing key (so saved response
            # data + version diffs stay anchored to a stable key).
            s["children"][i] = build_field(
                out, label=label, type_key=type_key,
                help_text=help_text, option_set=option_set, key=field_key,
            )
            break
    return out


def remove_field(schema: dict, section_key: str, field_key: str) -> dict:
    out = copy.deepcopy(schema)
    s = find_section(out, section_key)
    if s is not None:
        s["children"] = [c for c in s.get("children", []) or [] if c.get("key") != field_key]
    return out


def move_field(schema: dict, section_key: str, field_key: str, direction: str) -> dict:
    out = copy.deepcopy(schema)
    s = find_section(out, section_key)
    if s is None:
        return out
    children = s.get("children", []) or []
    idx = next((i for i, c in enumerate(children) if c.get("key") == field_key), None)
    if idx is None:
        return out
    swap = idx - 1 if direction == "up" else idx + 1
    if 0 <= swap < len(children):
        children[idx], children[swap] = children[swap], children[idx]
        s["children"] = children
    return out


# ---------------------------------------------------------------------------
# Draft lifecycle (the only DB-aware functions)
# ---------------------------------------------------------------------------
def has_draft(form_def) -> bool:
    """True when an unpublished draft exists and differs from the published schema."""
    return form_def.draft_schema is not None and form_def.draft_schema != form_def.schema


def get_draft_schema(form_def) -> dict:
    """Return the draft to edit -- the stored draft, or a fresh copy of the published schema."""
    if form_def.draft_schema is not None:
        return copy.deepcopy(form_def.draft_schema)
    return copy.deepcopy(form_def.schema or {})


def save_draft(form_def, schema: dict, user=None):
    """Persist an edited schema as the draft. Returns (ok, LintReport).

    Lints in 'authoring' mode (lenient -- drafts may be mid-edit). The caller
    decides whether to surface warnings; we only block on hard errors.
    """
    from django.utils import timezone

    from form_manager.services.formspec_service import lint_definition

    report = lint_definition(schema, mode="authoring")
    if not report.is_clean:
        return False, report
    form_def.draft_schema = schema
    form_def.draft_updated_at = timezone.now()
    form_def.save(update_fields=["draft_schema", "draft_updated_at", "updated_at"])
    return True, report


def discard_draft(form_def):
    """Throw away the draft, reverting to the published schema."""
    form_def.draft_schema = None
    form_def.draft_updated_at = None
    form_def.save(update_fields=["draft_schema", "draft_updated_at", "updated_at"])
