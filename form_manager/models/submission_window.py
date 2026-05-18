from datetime import date

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from organizations.models import BaseModel


class SubmissionWindow(BaseModel):
    """Configurable open/close dates for one form, for one federal fiscal year.

    ``fiscal_year`` is the FY ending calendar year (FY25 = 2025, covering
    Oct 1 2024 - Sep 30 2025). If ``opens_at`` / ``closes_at`` are left blank
    they default to the full federal FY (Oct 1 - Sep 30); admins can narrow
    the window per form as needed.
    """

    STATUS_UPCOMING = "upcoming"
    STATUS_OPEN = "open"
    STATUS_PAST_DUE = "past_due"

    form_definition = models.ForeignKey(
        "form_manager.FormDefinition",
        on_delete=models.CASCADE,
        related_name="submission_windows",
    )
    fiscal_year = models.PositiveSmallIntegerField(
        help_text="FY ending calendar year, e.g. 2025 for FY25",
    )
    opens_at = models.DateField(
        blank=True,
        help_text="Defaults to Oct 1 of the prior calendar year if left blank.",
    )
    closes_at = models.DateField(
        blank=True,
        help_text="Defaults to Sep 30 of the FY ending year if left blank.",
    )

    class Meta(BaseModel.Meta):
        unique_together = ("form_definition", "fiscal_year")
        ordering = ["-fiscal_year", "form_definition__name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.form_definition} FY{self.fiscal_year % 100:02d}"

    def save(self, *args, **kwargs):
        if not self.opens_at:
            self.opens_at = date(self.fiscal_year - 1, 10, 1)
        if not self.closes_at:
            self.closes_at = date(self.fiscal_year, 9, 30)
        super().save(*args, **kwargs)

    def clean(self) -> None:
        if self.opens_at and self.closes_at and self.closes_at <= self.opens_at:
            raise ValidationError({"closes_at": "Must be after opens_at."})

    def status_on(self, today: date) -> str:
        if today < self.opens_at:
            return self.STATUS_UPCOMING
        if today > self.closes_at:
            return self.STATUS_PAST_DUE
        return self.STATUS_OPEN

    @property
    def status(self) -> str:
        return self.status_on(timezone.localdate())
