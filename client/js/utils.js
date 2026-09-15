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
  if (!API.isAuthed()) {
    window.location.href = "../login.html";
    return false;
  }
  return true;
}

function redirectIfAuthed(target = "pages/dashboard.html") {
  if (API.isAuthed()) {
    window.location.href = target;
  }
}

async function logout() {
  try {
    await fetch(`${API.base}/auth/logout`, { method: "POST", credentials: "include" });
  } catch (_) {}
  API.clearSession();
  const path = window.location.pathname;
  if (path.includes("/admin/")) {
    window.location.href = "login.html";
    return;
  }
  const isInPages = path.includes("/pages/");
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
        <a href="linkedin-internships.html" class="${active === "linkedin" ? "active" : ""}">LinkedIn</a>
        <a href="#" id="logout-link">Logout</a>
      </nav>
    </aside>
  `;
}

function mountAppShell(active, title, contentHtml, sidebarHtml) {
  document.body.innerHTML = `
    <div class="app-shell">
      ${sidebarHtml || renderSidebar(active)}
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

function hideBusy() {
  document.getElementById("app-busy")?.classList.add("hidden");
}

function showBusy(text = "Please wait...") {
  let el = document.getElementById("app-busy");
  if (!el) {
    el = document.createElement("div");
    el.id = "app-busy";
    el.className = "app-busy";
    el.innerHTML = `<div class="app-busy-card"><div class="spinner"></div><p id="app-busy-text"></p></div>`;
    document.body.appendChild(el);
  }
  const label = document.getElementById("app-busy-text");
  if (label) label.textContent = text;
  el.classList.remove("hidden");
}

async function withBusy(button, label, fn) {
  const original = button ? button.textContent : "";
  if (button) {
    button.disabled = true;
    button.textContent = label;
  }
  showBusy(label);
  try {
    return await fn();
  } finally {
    hideBusy();
    if (button) {
      button.disabled = false;
      button.textContent = original;
    }
  }
}

function setFieldError(input, message) {
  const group = input.closest(".form-group") || input.parentElement;
  group.classList.toggle("has-error", !!message);
  let hint = group.querySelector(".field-error");
  if (!hint) {
    hint = document.createElement("small");
    hint.className = "field-error";
    group.appendChild(hint);
  }
  hint.textContent = message || "";
}

function clearFormErrors(form) {
  form.querySelectorAll(".field-error").forEach((el) => {
    el.textContent = "";
  });
  form.querySelectorAll(".has-error").forEach((el) => el.classList.remove("has-error"));
}

function validateRegisterForm(form) {
  clearFormErrors(form);
  let ok = true;
  const name = form.full_name.value.trim();
  if (name.length < 2 || !/^[A-Za-z][A-Za-z .'-]{1,79}$/.test(name)) {
    setFieldError(form.full_name, "Use your real name (letters only, min 2 characters).");
    ok = false;
  }
  const email = form.email.value.trim();
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    setFieldError(form.email, "Enter a valid email address.");
    ok = false;
  }
  const phone = form.phone.value.trim();
  if (phone) {
    const digits = phone.replace(/\D/g, "");
    if (digits.length < 10 || digits.length > 15) {
      setFieldError(form.phone, "Phone must have 10–15 digits.");
      ok = false;
    }
  }
  const password = form.password.value;
  if (!/^(?=.*[A-Za-z])(?=.*\d).{8,}$/.test(password)) {
    setFieldError(form.password, "Min 8 characters, with at least one letter and one number.");
    ok = false;
  }
  if (form.confirm_password && form.confirm_password.value !== password) {
    setFieldError(form.confirm_password, "Passwords do not match.");
    ok = false;
  }
  return ok;
}

function validateLoginForm(form) {
  clearFormErrors(form);
  let ok = true;
  if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email.value.trim())) {
    setFieldError(form.email, "Enter a valid email address.");
    ok = false;
  }
  if (!form.password.value) {
    setFieldError(form.password, "Password is required.");
    ok = false;
  }
  return ok;
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
  showBusy,
  hideBusy,
  withBusy,
  validateRegisterForm,
  validateLoginForm,
};
