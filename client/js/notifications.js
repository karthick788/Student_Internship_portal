if (!requireAuth()) throw new Error("Auth required");

mountAppShell(
  "notifications",
  "Notifications",
  `
  <div style="display:flex;justify-content:flex-end;margin-bottom:1rem">
    <button class="btn btn-outline btn-sm" id="mark-all-btn">Mark All Read</button>
  </div>
  <div id="notifications-container" class="loading-state">Loading notifications...</div>
  `
);

const container = document.getElementById("notifications-container");

async function loadNotifications() {
  container.className = "loading-state";
  container.textContent = "Loading notifications...";
  try {
    const data = await API.apiRequest("/notifications");
    const items = data.items || [];
    if (!items.length) {
      container.className = "empty-state";
      container.textContent = "No notifications yet.";
      return;
    }
    container.className = "card";
    container.innerHTML = items
      .map(
        (n) => `
      <div class="notification-item ${n.is_read ? "" : "unread"}">
        <strong>${escapeHtml(n.title)}</strong>
        <p>${escapeHtml(n.message)}</p>
        <small>${formatDate(n.created_at)}</small>
        ${n.is_read ? "" : `<button class="btn btn-sm btn-outline mark-read" data-id="${escapeHtml(n.id)}">Mark Read</button>`}
      </div>`
      )
      .join("");

    container.querySelectorAll(".mark-read").forEach((btn) => {
      btn.addEventListener("click", async () => {
        await API.apiRequest(`/notifications/${btn.dataset.id}/read`, { method: "PUT" });
        loadNotifications();
      });
    });
  } catch (err) {
    container.className = "error-state";
    container.textContent = err.message;
  }
}

document.getElementById("mark-all-btn").addEventListener("click", async () => {
  try {
    await API.apiRequest("/notifications/read-all", { method: "PUT" });
    showToast("All notifications marked as read", "success");
    loadNotifications();
  } catch (err) {
    showToast(err.message, "error");
  }
});

loadNotifications();
setInterval(loadNotifications, 30000);
