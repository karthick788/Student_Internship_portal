const API_HOST = window.location.hostname === "127.0.0.1" ? "127.0.0.1" : "localhost";
const API_BASE = `http://${API_HOST}:5000/api`;

function getToken() {
  return localStorage.getItem("token");
}

function isAuthed() {
  return !!getToken() || !!getStudent();
}

function setSession(token, student) {
  if (token) {
    localStorage.setItem("token", token);
  }
  if (student) {
    localStorage.setItem("student", JSON.stringify(student));
  }
}

function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("student");
  localStorage.removeItem("authed");
}

function getStudent() {
  const raw = localStorage.getItem("student");
  return raw ? JSON.parse(raw) : null;
}

async function apiRequest(path, options = {}) {
  const headers = { ...(options.headers || {}) };
  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  if (!(options.body instanceof FormData) && options.body && !headers["Content-Type"]) {
    headers["Content-Type"] = "application/json";
  }

  let response;
  try {
    response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers,
      credentials: "include",
    });
  } catch {
    throw new Error("Cannot reach the API at " + API_BASE + ". Start Flask: python app.py in the server folder.");
  }

  let data = null;
  const text = await response.text();
  if (text) {
    try {
      data = JSON.parse(text);
    } catch {
      data = { message: text };
    }
  }

  if (!response.ok) {
    const isAuthForm =
      path.startsWith("/auth/login") ||
      path.startsWith("/auth/register") ||
      path.startsWith("/auth/google");
    if (response.status === 401 && !isAuthForm) {
      clearSession();
      const path = window.location.pathname;
      if (path.includes("/admin/")) {
        window.location.href = "login.html";
        return;
      }
      const isInPages = path.includes("/pages/");
      window.location.href = isInPages ? "../login.html" : "login.html";
      return;
    }
    const message = data?.error || data?.message || "Request failed";
    throw new Error(message);
  }

  return data;
}

window.API = {
  base: API_BASE,
  getToken,
  isAuthed,
  setSession,
  clearSession,
  getStudent,
  apiRequest,
};
