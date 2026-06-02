"""Rename the formspec_runtime FeatureFlag row to form_runtime.

The flag was renamed in REGISTERED_FLAGS to avoid surfacing a vendor name
in the admin UI. Existing prod rows still carry the old key and would
otherwise sit orphaned, defaulting back to a freshly-seeded row with the
new key. This migration carries any non-default state forward.
"""

from django.db import migrations


def rename_forward(apps, schema_editor):
    FeatureFlag = apps.get_model("staff_review", "FeatureFlag")
    old = FeatureFlag.objects.filter(key="formspec_runtime").first()
    if old is None:
        return
    new = FeatureFlag.objects.filter(key="form_runtime").first()
    if new is None:
        # Simple rename
        old.key = "form_runtime"
        old.save(update_fields=["key"])
    else:
        # New row already exists (auto-seeded). Preserve the old row's
        # toggle state if a user had turned it off, then delete the old row.
        if not old.is_enabled and new.is_enabled:
            new.is_enabled = False
            new.save(update_fields=["is_enabled"])
        old.delete()


def rename_backward(apps, schema_editor):
    FeatureFlag = apps.get_model("staff_review", "FeatureFlag")
    row = FeatureFlag.objects.filter(key="form_runtime").first()
    if row is not None:
        row.key = "formspec_runtime"
        row.save(update_fields=["key"])


class Migration(migrations.Migration):

    dependencies = [
        ("staff_review", "0003_feature_flags"),
    ]

    operations = [
        migrations.RunPython(rename_forward, rename_backward),
    ]
