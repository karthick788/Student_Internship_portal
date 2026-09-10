if (!requireAuth()) throw new Error("Auth required");

mountAppShell(
  "dashboard",
  "Dashboard",
  `
  <div id="resume-banner"></div>
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

const statsEl = document.getElementById("stats");
const bannerEl = document.getElementById("resume-banner");
const syncBtn = document.getElementById("sync-btn");

async function loadDashboard() {
  statsEl.innerHTML = renderSkeleton(4);
  bannerEl.innerHTML = "";
  try {
    const stats = await API.apiRequest("/student/dashboard");
    statsEl.innerHTML = `
      <article class="card stat-card"><h3>${stats.internships}</h3><p>🏢 Available Internships</p></article>
      <article class="card stat-card"><h3>${stats.applications}</h3><p>📝 My Applications</p></article>
      <article class="card stat-card"><h3>${stats.saved}</h3><p>🔖 Saved</p></article>
      <article class="card stat-card"><h3>${stats.notifications_unread}</h3><p>🔔 Unread Notifications</p></article>
    `;
    if (!stats.has_resume) {
      bannerEl.innerHTML =
        '<div class="banner"><p>📄 Upload your resume to strengthen applications.</p><a class="btn btn-primary btn-sm" href="profile.html">Upload Now</a></div>';
    }
  } catch (err) {
    showToast(err.message, "error");
  }
}

syncBtn.addEventListener("click", async () => {
  syncBtn.disabled = true;
  syncBtn.textContent = "Syncing...";
  try {
    const result = await API.apiRequest("/internships/sync", { method: "POST" });
    showToast(`Synced ${result.fetched} listings (${result.inserted} new)`, "success");
    loadDashboard();
  } catch (err) {
    showToast(err.message, "error");
  } finally {
    syncBtn.disabled = false;
    syncBtn.textContent = "Sync External Internships";
  }
});

loadDashboard();
