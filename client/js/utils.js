function escapeHtml(str) {
  if (str === null || str === undefined) return "";
  return String(str)
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
}

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

async function logout() {
  try {
    await fetch(`${API.base}/auth/logout`, { method: "POST", credentials: "include" });
  } catch (_) {}
  API.clearSession();
  const isInPages = window.location.pathname.includes("/pages/") || window.location.pathname.includes("/admin/");
  window.location.href = isInPages ? "../login.html" : "login.html";
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
  return `<span class="badge ${map[status] || "badge"}">${escapeHtml((status || "").replaceAll("_", " "))}</span>`;
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
          <small style="color:#94a3b8">${escapeHtml(student?.full_name) || "Student"}</small>
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
            <h1 class="page-title">${escapeHtml(title)}</h1>
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
  const id = escapeHtml(item.id);
  const savedBtn = options.showUnsave
    ? `<button class="btn btn-danger btn-sm" data-unsave="${id}">Remove</button>`
    : `<button class="btn btn-secondary btn-sm" data-save="${id}">Save</button>`;
  return `
    <article class="card internship-card">
      <div class="internship-meta">
        ${workModeBadge(escapeHtml(item.work_mode))}
        <span class="badge">${escapeHtml(item.application_method) || "internal"}</span>
      </div>
      <h3>${escapeHtml(item.title)}</h3>
      <p><strong>${escapeHtml(item.company_name)}</strong></p>
      <p>${escapeHtml(item.location) || "Location not specified"} · ${escapeHtml(item.duration) || "Duration N/A"}</p>
      <p style="color:var(--muted);font-size:0.92rem">${escapeHtml((item.description || "").slice(0, 120))}...</p>
      <div style="margin-top:auto;display:flex;gap:0.5rem;flex-wrap:wrap">
        <a class="btn btn-primary btn-sm" href="internship-details.html?id=${id}">View Details</a>
        ${options.hideSave ? "" : savedBtn}
      </div>
    </article>
  `;
}

function renderSkeleton(count = 6) {
  return Array.from({ length: count }, () => `
    <div class="skeleton-card">
      <div class="skeleton-line short"></div>
      <div class="skeleton-line medium"></div>
      <div class="skeleton-line"></div>
      <div class="skeleton-line tall"></div>
      <div class="skeleton-line short"></div>
    </div>
  `).join("");
}

function renderPagination(currentPage, totalPages, onPageChange) {
  if (totalPages <= 1) return "";
  const buttons = [];
  buttons.push(`<button class="page-btn" ${currentPage === 1 ? "disabled" : ""} data-page="${currentPage - 1}">← Prev</button>`);
  for (let i = 1; i <= totalPages; i++) {
    buttons.push(`<button class="page-btn ${i === currentPage ? "active" : ""}" data-page="${i}">${i}</button>`);
  }
  buttons.push(`<button class="page-btn" ${currentPage === totalPages ? "disabled" : ""} data-page="${currentPage + 1}">Next →</button>`);
  return `<div class="pagination">${buttons.join("")}</div>`;
}

window.Utils = {
  escapeHtml,
  showToast,
  requireAuth,
  redirectIfAuthed,
  logout,
  formatDate,
  statusBadge,
  workModeBadge,
  mountAppShell,
  internshipCard,
  renderSkeleton,
  renderPagination,
};
