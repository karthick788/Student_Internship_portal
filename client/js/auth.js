document.addEventListener("DOMContentLoaded", () => {
  redirectIfAuthed("pages/dashboard.html");

  document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    const payload = {
      email: form.email.value.trim(),
      password: form.password.value,
    };
    try {
      const data = await API.apiRequest("/auth/login", {
        method: "POST",
        body: JSON.stringify(payload),
      });
      API.setSession(data.token, data.student);
      showToast("Welcome back!", "success");
      window.location.href = "pages/dashboard.html";
    } catch (err) {
      showToast(err.message, "error");
    }
  });
});
