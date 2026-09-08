if (!requireAuth()) {
  throw new Error("Auth required");
}

mountAppShell(
  "dashboard",
  "Dashboard",
  `
  <section class="dashboard-cards" id="stats"></section>
  <section class="card" style="padding:1.2rem">
    <h2>Quick Actions</h2>
    <div style="display:flex;gap:0.7rem;flex-wrap:wrap;margin-top:0.8rem">
      <a class="btn btn-primary" href="internships.html">Browse Internships</a>
      <a class="btn btn-secondary" href="profile.html">Update Profile</a>
      <a class="btn btn-secondary" href="applications.html">View Applications</a>
      <button class="btn btn-outline" id="sync-btn">Sync External Internships</button>
    </div>
  </section>
  `
);

async function loadDashboard() {
  try {
    const stats = await API.apiRequest("/student/dashboard");
    document.getElementById("stats").innerHTML = `
      <article class="card stat-card"><h3>${stats.internships}</h3><p>Available Internships</p></article>
      <article class="card stat-card"><h3>${stats.applications}</h3><p>My Applications</p></article>
      <article class="card stat-card"><h3>${stats.saved}</h3><p>Saved Internships</p></article>
      <article class="card stat-card"><h3>${stats.notifications_unread}</h3><p>Unread Notifications</p></article>
    `;
    if (!stats.has_resume) {
      showToast("Upload your resume to strengthen applications.", "info");
    }
  } catch (err) {
    showToast(err.message, "error");
  }
}

document.getElementById("sync-btn").addEventListener("click", async () => {
  try {
    const result = await API.apiRequest("/internships/sync", { method: "POST" });
    showToast(`Synced ${result.fetched} listings (${result.inserted} new)`, "success");
    loadDashboard();
  } catch (err) {
    showToast(err.message, "error");
  }
});

loadDashboard();
