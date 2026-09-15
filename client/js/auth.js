document.addEventListener("DOMContentLoaded", () => {
  redirectIfAuthed("pages/dashboard.html");
  mountGoogleButton("google-btn");

  document.getElementById("login-form")?.addEventListener("submit", async (e) => {
    e.preventDefault();
    const form = e.target;
    if (!validateLoginForm(form)) return;
    const payload = {
      email: form.email.value.trim(),
      password: form.password.value,
    };
    const btn = form.querySelector("button[type='submit']");
    try {
      await withBusy(btn, "Signing in...", async () => {
        const data = await API.apiRequest("/auth/login", {
          method: "POST",
          body: JSON.stringify(payload),
        });
        if (!data?.token) throw new Error("Restart the Flask server (uv run python app.py).");
        API.setSession(data.token, data.student);
      });
      showToast("Welcome back!", "success");
      window.location.href = "pages/dashboard.html";
    } catch (err) {
      showToast(err.message, "error");
    }
  });
});
