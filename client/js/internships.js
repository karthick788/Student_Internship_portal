if (!requireAuth()) throw new Error("Auth required");

mountAppShell(
  "internships",
  "Find Internships",
  `
  <form id="filters" class="card filters-panel">
    <div class="form-group"><label>Search</label><input name="search" placeholder="Python, design..."></div>
    <div class="form-group"><label>Location</label><input name="location" placeholder="Bangalore"></div>
    <div class="form-group"><label>Skills</label><input name="skills" placeholder="Python"></div>
    <div class="form-group">
      <label>Work Mode</label>
      <select name="work_mode">
        <option value="">Any</option>
        <option value="remote">Remote</option>
        <option value="onsite">Onsite</option>
        <option value="hybrid">Hybrid</option>
      </select>
    </div>
    <div class="form-group"><label>Duration</label><input name="duration"></div>
    <div class="form-group" style="align-self:end"><button class="btn btn-primary" type="submit">Apply Filters</button></div>
  </form>
  <div id="internship-list" class="internship-grid loading-state">Loading internships...</div>
  `
);

const listEl = document.getElementById("internship-list");
const filtersForm = document.getElementById("filters");

async function loadInternships(params = {}) {
  listEl.className = "internship-grid loading-state";
  listEl.textContent = "Loading internships...";
  const query = new URLSearchParams(Object.entries(params).filter(([, v]) => v)).toString();
  try {
    const items = await API.apiRequest(`/internships${query ? `?${query}` : ""}`);
    if (!items.length) {
      listEl.className = "empty-state";
      listEl.textContent = "No internships found. Try syncing from dashboard.";
      return;
    }
    listEl.className = "internship-grid";
    listEl.innerHTML = items.map((item) => internshipCard(item)).join("");
    bindSaveButtons();
  } catch (err) {
    listEl.className = "error-state";
    listEl.textContent = err.message;
  }
}

function bindSaveButtons() {
  document.querySelectorAll("[data-save]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await API.apiRequest(`/saved-internships/${btn.dataset.save}`, { method: "POST" });
        showToast("Internship saved", "success");
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  });
}

filtersForm.addEventListener("submit", (e) => {
  e.preventDefault();
  const params = Object.fromEntries(new FormData(filtersForm).entries());
  loadInternships(params);
});

loadInternships();
