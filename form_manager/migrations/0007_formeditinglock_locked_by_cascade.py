import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


def delete_orphan_locks(apps, schema_editor):
    """Remove any locks whose locked_by is NULL before making the column non-nullable."""
    FormEditingLock = apps.get_model("form_manager", "FormEditingLock")
    FormEditingLock.objects.filter(locked_by__isnull=True).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("form_manager", "0006_add_formeditinglock"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RunPython(delete_orphan_locks, migrations.RunPython.noop),
        migrations.AlterField(
            model_name="formeditinglock",
            name="locked_by",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
