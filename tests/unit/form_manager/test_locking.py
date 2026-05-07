import uuid
from datetime import timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from form_manager.locking import (
    acquire_editing_lock,
    get_active_lock,
    refresh_editing_lock,
    release_editing_lock,
)
from form_manager.models import FormEditingLock


@pytest.mark.django_db
def test_acquire_creates_lock(form_entry, get_user):
    user = get_user("demo")
    token = acquire_editing_lock(form_entry, user)
    assert token is not None
    lock = FormEditingLock.objects.get(form_entry=form_entry)
    assert lock.locked_by == user
    assert lock.expires_at > timezone.now()
    assert lock.lock_token == token


@pytest.mark.django_db
def test_acquire_same_user_refreshes_lock(form_entry, get_user):
    user = get_user("demo")
    token1 = acquire_editing_lock(form_entry, user)
    original_expires = FormEditingLock.objects.get(form_entry=form_entry).expires_at

    token2 = acquire_editing_lock(form_entry, user)
    lock = FormEditingLock.objects.get(form_entry=form_entry)

    assert lock.expires_at >= original_expires
    assert token2 is not None
    assert token2 != token1
    assert lock.lock_token == token2


@pytest.mark.django_db
def test_acquire_blocked_by_other_user(form_entry, get_user):
    user1 = get_user("demo")
    user2 = get_user("demo-1")

    assert acquire_editing_lock(form_entry, user1) is not None
    assert acquire_editing_lock(form_entry, user2) is None


@pytest.mark.django_db
def test_acquire_takes_over_expired_lock(form_entry, get_user):
    user1 = get_user("demo")
    user2 = get_user("demo-1")

    # Create an already-expired lock for user1
    FormEditingLock.objects.create(
        form_entry=form_entry,
        locked_by=user1,
        expires_at=timezone.now() - timedelta(minutes=1),
    )

    token = acquire_editing_lock(form_entry, user2)
    assert token is not None
    lock = FormEditingLock.objects.get(form_entry=form_entry)
    assert lock.locked_by == user2
    assert lock.lock_token == token


@pytest.mark.django_db
def test_get_active_lock_returns_none_when_expired(form_entry, get_user):
    user = get_user("demo")
    FormEditingLock.objects.create(
        form_entry=form_entry,
        locked_by=user,
        expires_at=timezone.now() - timedelta(seconds=1),
    )
    assert get_active_lock(form_entry) is None


@pytest.mark.django_db
def test_get_active_lock_returns_lock_when_valid(form_entry, get_user):
    user = get_user("demo")
    acquire_editing_lock(form_entry, user)
    assert get_active_lock(form_entry) is not None


@pytest.mark.django_db
def test_release_deletes_lock_for_owner(form_entry, get_user):
    user = get_user("demo")
    acquire_editing_lock(form_entry, user)
    release_editing_lock(form_entry, user)
    assert not FormEditingLock.objects.filter(form_entry=form_entry).exists()


@pytest.mark.django_db
def test_release_does_not_delete_lock_for_non_owner(form_entry, get_user):
    user1 = get_user("demo")
    user2 = get_user("demo-1")
    acquire_editing_lock(form_entry, user1)
    release_editing_lock(form_entry, user2)
    assert FormEditingLock.objects.filter(form_entry=form_entry).exists()


@pytest.mark.django_db
def test_release_with_matching_token_deletes_lock(form_entry, get_user):
    user = get_user("demo")
    token = acquire_editing_lock(form_entry, user)
    release_editing_lock(form_entry, user, lock_token=token)
    assert not FormEditingLock.objects.filter(form_entry=form_entry).exists()


@pytest.mark.django_db
def test_release_with_stale_token_does_not_delete_lock(form_entry, get_user):
    """A sendBeacon with an old token (from before a refresh) must not release the new lock."""
    user = get_user("demo")
    stale_token = uuid.uuid4()
    acquire_editing_lock(form_entry, user)  # acquires with a new token
    release_editing_lock(form_entry, user, lock_token=stale_token)
    assert FormEditingLock.objects.filter(form_entry=form_entry).exists()


@pytest.mark.django_db
def test_refresh_extends_expiry(form_entry, get_user):
    user = get_user("demo")
    acquire_editing_lock(form_entry, user)

    # Wind the expiry back to simulate near-expiry
    FormEditingLock.objects.filter(form_entry=form_entry).update(
        expires_at=timezone.now() + timedelta(minutes=1)
    )

    refresh_editing_lock(form_entry, user)

    lock = FormEditingLock.objects.get(form_entry=form_entry)
    assert lock.expires_at > timezone.now() + timedelta(minutes=settings.LOCK_DURATION_MINUTES - 1)


@pytest.mark.django_db
def test_refresh_no_op_for_non_owner(form_entry, get_user):
    user1 = get_user("demo")
    user2 = get_user("demo-1")
    acquire_editing_lock(form_entry, user1)
    original_expires = FormEditingLock.objects.get(form_entry=form_entry).expires_at

    refresh_editing_lock(form_entry, user2)

    lock = FormEditingLock.objects.get(form_entry=form_entry)
    assert lock.expires_at == original_expires


@pytest.mark.django_db
def test_heartbeat_endpoint_refreshes_lock(form_entry, get_user, authenticated_client):
    user = get_user("demo")
    acquire_editing_lock(form_entry, user)
    original_expires = FormEditingLock.objects.get(form_entry=form_entry).expires_at

    FormEditingLock.objects.filter(form_entry=form_entry).update(
        expires_at=timezone.now() + timedelta(minutes=1)
    )

    url = reverse("editing_lock_heartbeat", args=[form_entry.pk])
    response = authenticated_client.post(url)

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
    lock = FormEditingLock.objects.get(form_entry=form_entry)
    assert lock.expires_at >= original_expires


@pytest.mark.django_db
def test_release_endpoint_with_matching_token_deletes_lock(
    form_entry, get_user, authenticated_client
):
    user = get_user("demo")
    token = acquire_editing_lock(form_entry, user)

    url = reverse("editing_lock_release", args=[form_entry.pk])
    response = authenticated_client.post(url, {"lock_token": str(token)})

    assert response.status_code == 200
    assert not FormEditingLock.objects.filter(form_entry=form_entry).exists()


@pytest.mark.django_db
def test_release_endpoint_with_stale_token_keeps_lock(form_entry, get_user, authenticated_client):
    user = get_user("demo")
    acquire_editing_lock(form_entry, user)

    url = reverse("editing_lock_release", args=[form_entry.pk])
    response = authenticated_client.post(url, {"lock_token": str(uuid.uuid4())})

    assert response.status_code == 200
    assert FormEditingLock.objects.filter(form_entry=form_entry).exists()


@pytest.mark.django_db
def test_release_endpoint_without_token_returns_400(form_entry, get_user, authenticated_client):
    user = get_user("demo")
    acquire_editing_lock(form_entry, user)

    url = reverse("editing_lock_release", args=[form_entry.pk])
    response = authenticated_client.post(url)

    assert response.status_code == 400
    assert FormEditingLock.objects.filter(form_entry=form_entry).exists()
