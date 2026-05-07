const HEARTBEAT_INTERVAL_MS = 5 * 60 * 1000;

function getCsrfToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? match[1] : "";
}

function post(url) {
  fetch(url, {
    method: "POST",
    headers: { "X-CSRFToken": getCsrfToken(), "Content-Type": "application/json" },
    keepalive: true,
  });
}

export function initEditingLock() {
  const el = document.getElementById("editing-lock-urls");
  if (!el) return;

  const heartbeatUrl = el.dataset.heartbeatUrl;
  const releaseUrl = el.dataset.releaseUrl;
  const lockToken = el.dataset.lockToken;

  const heartbeatTimer = setInterval(function () {
    post(heartbeatUrl);
  }, HEARTBEAT_INTERVAL_MS);

  // Suppress the unload release when the user is intentionally submitting the
  // form — the finalize POST requires the lock to still be alive when it arrives.
  let isSubmitting = false;
  const submitForm = document.getElementById("csf-form");
  if (submitForm) {
    submitForm.addEventListener("submit", function () {
      isSubmitting = true;
    });
  }

  // On pagehide (tab close, navigation away, or refresh), stop the heartbeat
  // and attempt an immediate lock release via sendBeacon.
  //
  // The lock_token ties the release to this specific page-load's lock instance.
  // Without it, a stale beacon sent during a refresh could arrive *after* the
  // reloaded page re-acquires the lock and accidentally release it.
  window.addEventListener("pagehide", function () {
    clearInterval(heartbeatTimer);
    if (isSubmitting) return;
    const formData = new FormData();
    formData.append("csrfmiddlewaretoken", getCsrfToken());
    formData.append("lock_token", lockToken);
    navigator.sendBeacon(releaseUrl, formData);
  });
}
