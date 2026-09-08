function showToast(message, type = "info") {
  let container = document.querySelector(".toast-container");
  if (!container) {
    container = document.createElement("div");
    container.className = "toast-container";
    document.body.appendChild(container);
  }
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.textContent = message;
  container.appendChild(toast);
  setTimeout(() => toast.remove(), 3200);
}

function requireAuth() {
  if (!API.getToken()) {
    window.location.href = "../login.html";
    return false;
  }
  return true;
}

function redirectIfAuthed(target = "pages/dashboard.html") {
  if (API.getToken()) {
    window.location.href = target;
  }
}

function logout() {
  API.clearSession();
  window.location.href = "../login.html";
}

function formatDate(value) {
  if (!value) return "Not specified";
  const date = new Date(value);
  if (Number.isNaN(date.getTime())) return value;
  return date.toLocaleDateString();
}

function statusBadge(status) {
  const map = {
    submitted: "badge",
    under_review: "badge-warning",
    shortlisted: "badge-success",
    rejected: "badge-danger",
    selected: "badge-success",
  };
  return `<span class="badge ${map[status] || "badge"}">${(status || "").replaceAll("_", " ")}</span>`;
}

function workModeBadge(mode) {
  return `<span class="badge">${mode || "onsite"}</span>`;
}

function renderSidebar(active) {
  const student = API.getStudent();
  return `
    <aside class="sidebar" id="sidebar">
      <div class="brand">
        <div class="brand-mark">SI</div>
        <div>
          <div>InternHub</div>
          <small style="color:#94a3b8">${student?.full_name || "Student"}</small>
        </div>
      </div>
      <nav class="sidebar-nav">
        <a href="dashboard.html" class="${active === "dashboard" ? "active" : ""}">Dashboard</a>
        <a href="profile.html" class="${active === "profile" ? "active" : ""}">Profile</a>
        <a href="internships.html" class="${active === "internships" ? "active" : ""}">Find Internships</a>
        <a href="saved-internships.html" class="${active === "saved" ? "active" : ""}">Saved</a>
        <a href="applications.html" class="${active === "applications" ? "active" : ""}">My Applications</a>
        <a href="notifications.html" class="${active === "notifications" ? "active" : ""}">Notifications</a>
        <a href="linkedin-internships.html" class="${active === "linkedin" ? "active" : ""}">LinkedIn</a>
        <a href="#" id="logout-link">Logout</a>
      </nav>
    </aside>
  `;
}

function mountAppShell(active, title, contentHtml) {
  document.body.innerHTML = `
    <div class="app-shell">
      ${renderSidebar(active)}
      <main class="main-content">
        <div class="topbar">
          <div>
            <button class="mobile-toggle" id="menu-toggle" aria-label="Open menu">☰</button>
            <h1 class="page-title">${title}</h1>
          </div>
        </div>
        ${contentHtml}
      </main>
    </div>
  `;
  document.getElementById("logout-link")?.addEventListener("click", (e) => {
    e.preventDefault();
    logout();
  });
  document.getElementById("menu-toggle")?.addEventListener("click", () => {
    document.getElementById("sidebar")?.classList.toggle("open");
  });
}

function internshipCard(item, options = {}) {
  const savedBtn = options.showUnsave
    ? `<button class="btn btn-danger btn-sm" data-unsave="${item.id}">Remove</button>`
    : `<button class="btn btn-secondary btn-sm" data-save="${item.id}">Save</button>`;
  return `
    <article class="card internship-card">
      <div class="internship-meta">
        ${workModeBadge(item.work_mode)}
        <span class="badge">${item.application_method || "internal"}</span>
      </div>
      <h3>${item.title}</h3>
      <p><strong>${item.company_name}</strong></p>
      <p>${item.location || "Location not specified"} · ${item.duration || "Duration N/A"}</p>
      <p style="color:var(--muted);font-size:0.92rem">${(item.description || "").slice(0, 120)}...</p>
      <div style="margin-top:auto;display:flex;gap:0.5rem;flex-wrap:wrap">
        <a class="btn btn-primary btn-sm" href="internship-details.html?id=${item.id}">View Details</a>
        ${options.hideSave ? "" : savedBtn}
      </div>
    </article>
  `;
}

window.Utils = {
  showToast,
  requireAuth,
  redirectIfAuthed,
  logout,
  formatDate,
  statusBadge,
  workModeBadge,
  mountAppShell,
  internshipCard,
};
