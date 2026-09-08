const API_BASE = "http://localhost:5000/api";

function getToken() {
  return localStorage.getItem("token");
}

function setSession(token, student) {
  localStorage.setItem("token", token);
  if (student) {
    localStorage.setItem("student", JSON.stringify(student));
  }
}

function clearSession() {
  localStorage.removeItem("token");
  localStorage.removeItem("student");
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

  const response = await fetch(`${API_BASE}${path}`, {
    ...options,
    headers,
  });

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
    const message = data?.error || data?.message || "Request failed";
    throw new Error(message);
  }

  return data;
}

window.API = {
  base: API_BASE,
  getToken,
  setSession,
  clearSession,
  getStudent,
  apiRequest,
};
