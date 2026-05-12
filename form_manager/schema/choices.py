"""Shared choice tuples for use across form schemas."""

from datetime import date
from typing import cast

from localflavor.us.us_states import US_STATES as _US_STATES


def _fiscal_year_choices() -> list[tuple[str, str]]:
    """Return the upcoming 3 fiscal year choices from the current date.

    The fiscal year runs October 1 – September 30. This list is computed once at
    module load time. Kayla confirmed "next 2 fiscal years continuously" is the
    desired range; 3 are included here as a small buffer.
    """
    today = date.today()
    # Before October: the current calendar year is the ending year of the current FY.
    start_fy = today.year + 1 if today.month >= 10 else today.year
    choices: list[tuple[str, str]] = [("", "Select a fiscal year")]
    for i in range(3):
        fy = start_fy + i
        choices.append((f"fy_{fy}", f"FY {fy} (October 1, {fy - 1} – September 30, {fy})"))
    return choices


FISCAL_YEAR_CHOICES: list[tuple[str, str]] = _fiscal_year_choices()

US_STATES: list[tuple[str, str]] = [("", "Select a state")] + list(
    cast(list[tuple[str, str]], _US_STATES)
)
