"""Shared choice tuples for use across form schemas."""

from datetime import date


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

US_STATES: list[tuple[str, str]] = [
    ("", "Select a state"),
    ("Alabama", "Alabama"),
    ("Alaska", "Alaska"),
    ("Arizona", "Arizona"),
    ("Arkansas", "Arkansas"),
    ("California", "California"),
    ("Colorado", "Colorado"),
    ("Connecticut", "Connecticut"),
    ("Delaware", "Delaware"),
    ("Florida", "Florida"),
    ("Georgia", "Georgia"),
    ("Hawaii", "Hawaii"),
    ("Idaho", "Idaho"),
    ("Illinois", "Illinois"),
    ("Indiana", "Indiana"),
    ("Iowa", "Iowa"),
    ("Kansas", "Kansas"),
    ("Kentucky", "Kentucky"),
    ("Louisiana", "Louisiana"),
    ("Maine", "Maine"),
    ("Maryland", "Maryland"),
    ("Massachusetts", "Massachusetts"),
    ("Michigan", "Michigan"),
    ("Minnesota", "Minnesota"),
    ("Mississippi", "Mississippi"),
    ("Missouri", "Missouri"),
    ("Montana", "Montana"),
    ("Nebraska", "Nebraska"),
    ("Nevada", "Nevada"),
    ("New Hampshire", "New Hampshire"),
    ("New Jersey", "New Jersey"),
    ("New Mexico", "New Mexico"),
    ("New York", "New York"),
    ("North Carolina", "North Carolina"),
    ("North Dakota", "North Dakota"),
    ("Ohio", "Ohio"),
    ("Oklahoma", "Oklahoma"),
    ("Oregon", "Oregon"),
    ("Pennsylvania", "Pennsylvania"),
    ("Rhode Island", "Rhode Island"),
    ("South Carolina", "South Carolina"),
    ("South Dakota", "South Dakota"),
    ("Tennessee", "Tennessee"),
    ("Texas", "Texas"),
    ("Utah", "Utah"),
    ("Vermont", "Vermont"),
    ("Virginia", "Virginia"),
    ("Washington", "Washington"),
    ("West Virginia", "West Virginia"),
    ("Wisconsin", "Wisconsin"),
    ("Wyoming", "Wyoming"),
    ("District of Columbia", "District of Columbia"),
]
