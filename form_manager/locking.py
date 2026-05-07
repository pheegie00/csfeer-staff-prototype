import uuid
from datetime import timedelta

from django.db import IntegrityError, transaction
from django.utils import timezone

from csfeer.config import get_app_config
from form_manager.models import FormEditingLock


def _lock_duration():
    return timedelta(minutes=get_app_config().lock_duration_minutes)


def get_active_lock(form_entry):
    """Return the FormEditingLock for this entry if it exists and has not expired."""
    try:
        lock = form_entry.editing_lock
    except FormEditingLock.DoesNotExist:
        return None

    if lock.expires_at <= timezone.now():
        return None

    return lock


def annotate_active_editors(entries):
    """
    Attach `active_editor` and `active_lock_expires_at` attributes to each entry.

    `active_editor` is the User who holds a non-expired editing lock, or None.
    `active_lock_expires_at` is the expiry timestamp of that lock, or None.
    Accepts a queryset or list; returns a list with the attributes set on each item.
    """
    entries = list(entries)
    now = timezone.now()
    locks = FormEditingLock.objects.filter(
        form_entry__in=[e.pk for e in entries],
        expires_at__gt=now,
    ).select_related("locked_by")
    locks_by_entry = {lock.form_entry_id: lock for lock in locks}  # type: ignore[attr-defined]
    for entry in entries:
        lock = locks_by_entry.get(entry.pk)
        entry.active_editor = lock.locked_by if lock else None
        entry.active_lock_expires_at = lock.expires_at if lock else None
    return entries


@transaction.atomic
def acquire_editing_lock(form_entry, user) -> uuid.UUID | None:
    """
    Attempt to acquire the editing lock for the given user.

    Returns a new lock_token (UUID) if the lock was acquired or refreshed.
    Returns None if another user holds an active lock.

    A fresh token is generated on every successful acquisition so that a stale
    sendBeacon from a previous page load cannot release a lock that was already
    re-acquired by a refresh.

    Uses select_for_update to prevent concurrent acquisition races. The
    IntegrityError path handles the narrow window where two concurrent requests
    both see DoesNotExist before either INSERT completes: the loser re-reads the
    winner's row under a row lock and applies the normal active/expired/same-user
    logic from there.
    """
    now = timezone.now()
    expires_at = now + _lock_duration()
    token = uuid.uuid4()

    try:
        lock = FormEditingLock.objects.select_for_update().get(form_entry=form_entry)
    except FormEditingLock.DoesNotExist:
        try:
            # Inner savepoint: if two requests race here, the loser's IntegrityError
            # only rolls back this savepoint, not the outer transaction, so the
            # re-read below can still execute cleanly on PostgreSQL.
            with transaction.atomic():
                FormEditingLock.objects.create(
                    form_entry=form_entry, locked_by=user, expires_at=expires_at, lock_token=token
                )
            return token
        except IntegrityError:
            # Another concurrent request won the INSERT race; re-read under lock.
            lock = FormEditingLock.objects.select_for_update().get(form_entry=form_entry)

    # Expired lock — anyone can take it
    if lock.expires_at <= now:
        lock.locked_by = user
        lock.expires_at = expires_at
        lock.lock_token = token
        lock.save(update_fields=["locked_by", "expires_at", "lock_token", "updated_at"])
        return token

    # Same user — refresh and issue a new token
    if lock.locked_by == user:
        lock.expires_at = expires_at
        lock.lock_token = token
        lock.save(update_fields=["expires_at", "lock_token", "updated_at"])
        return token

    # Another user holds an active lock
    return None


def release_editing_lock(form_entry, user, lock_token=None) -> None:
    """
    Delete the lock if the given user holds it.

    If lock_token is provided, only delete when the token matches the current
    lock row — this prevents a stale sendBeacon (sent before a page refresh)
    from releasing a lock that was re-acquired by the reloaded page.
    """
    qs = FormEditingLock.objects.filter(form_entry=form_entry, locked_by=user)
    if lock_token is not None:
        qs = qs.filter(lock_token=lock_token)
    qs.delete()


def refresh_editing_lock(form_entry, user) -> None:
    """Reset expires_at to now + lock_duration_minutes if the user holds the lock."""
    FormEditingLock.objects.filter(form_entry=form_entry, locked_by=user).update(
        expires_at=timezone.now() + _lock_duration()
    )
