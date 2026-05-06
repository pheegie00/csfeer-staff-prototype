var HEARTBEAT_INTERVAL_MS = 5 * 60 * 1000;

function getCsrfToken() {
  var match = document.cookie.match(/csrftoken=([^;]+)/);
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
  var el = document.getElementById("editing-lock-urls");
  if (!el) return;

  var heartbeatUrl = el.dataset.heartbeatUrl;
  var releaseUrl = el.dataset.releaseUrl;
  var lockToken = el.dataset.lockToken;

  var heartbeatTimer = setInterval(function () {
    post(heartbeatUrl);
  }, HEARTBEAT_INTERVAL_MS);

  // On pagehide (tab close, navigation away, or refresh), stop the heartbeat
  // and attempt an immediate lock release via sendBeacon.
  //
  // The lock_token ties the release to this specific page-load's lock instance.
  // Without it, a stale beacon sent during a refresh could arrive *after* the
  // reloaded page re-acquires the lock and accidentally release it.
  window.addEventListener("pagehide", function () {
    clearInterval(heartbeatTimer);
    var formData = new FormData();
    formData.append("csrfmiddlewaretoken", getCsrfToken());
    formData.append("lock_token", lockToken);
    navigator.sendBeacon(releaseUrl, formData);
  });
}
