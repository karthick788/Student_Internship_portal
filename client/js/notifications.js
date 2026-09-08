if (!requireAuth()) throw new Error("Auth required");

mountAppShell("notifications", "Notifications", `<div id="notifications" class="card loading-state">Loading...</div>`);

async function loadNotifications() {
  const root = document.getElementById("notifications");
  try {
    const data = await API.apiRequest("/notifications");
    const items = data.items || [];
    if (!items.length) {
      root.className = "empty-state";
      root.textContent = "No notifications yet.";
      return;
    }
    root.className = "card";
    root.innerHTML = items
      .map(
        (n) => `
      <div class="notification-item ${n.is_read ? "" : "unread"}" data-id="${n.id}">
        <strong>${n.title}</strong>
        <p>${n.message}</p>
        <small>${formatDate(n.created_at)}</small>
        ${n.is_read ? "" : `<button class="btn btn-sm btn-outline mark-read" data-read="${n.id}">Mark read</button>`}
      </div>`
      )
      .join("");

    document.querySelectorAll(".mark-read").forEach((btn) => {
      btn.addEventListener("click", async () => {
        await API.apiRequest(`/notifications/${btn.dataset.read}/read`, { method: "PUT" });
        loadNotifications();
      });
    });
  } catch (err) {
    root.className = "error-state";
    root.textContent = err.message;
  }
}

loadNotifications();
