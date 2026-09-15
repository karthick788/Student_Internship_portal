if (!requireAuth()) throw new Error("Auth required");

let currentPage = 1;
let currentFilters = {};

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
  <div id="internship-list" class="internship-grid"></div>
  <div id="pagination"></div>
  `
);

const listEl = document.getElementById("internship-list");
const paginationEl = document.getElementById("pagination");
const filtersForm = document.getElementById("filters");

async function loadInternships(page = currentPage) {
  currentPage = page;
  listEl.className = "internship-grid";
  listEl.innerHTML = renderSkeleton(6);
  paginationEl.innerHTML = "";

  const params = { ...currentFilters, page: currentPage };
  const query = new URLSearchParams(Object.entries(params).filter(([, v]) => v)).toString();

  try {
    const data = await API.apiRequest(`/internships?${query}`);
    const items = data.items || [];
    if (!items.length) {
      listEl.className = "empty-state";
      listEl.textContent = "No internships found. Try syncing from dashboard.";
      return;
    }
    listEl.innerHTML = items.map((item) => internshipCard(item)).join("");
    paginationEl.innerHTML = renderPagination(data.page, data.pages);
    bindSaveButtons();
    bindPagination();
  } catch (err) {
    listEl.className = "error-state";
    listEl.innerHTML = `<p>${escapeHtml(err.message)}</p><button class="btn btn-primary" id="retry-btn">Retry</button>`;
    document.getElementById("retry-btn")?.addEventListener("click", () => loadInternships(currentPage));
  }
}

function bindSaveButtons() {
  listEl.querySelectorAll("[data-save]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      try {
        await withBusy(btn, "Saving...", async () => {
          await API.apiRequest(`/saved-internships/${btn.dataset.save}`, { method: "POST" });
        });
        showToast("Internship saved", "success");
      } catch (err) {
        showToast(err.message, "error");
      }
    });
  });
}

function bindPagination() {
  paginationEl.querySelectorAll("[data-page]").forEach((btn) => {
    btn.addEventListener("click", () => {
      if (btn.disabled) return;
      const page = Number(btn.dataset.page);
      if (page !== currentPage) loadInternships(page);
    });
  });
}

filtersForm.addEventListener("submit", (e) => {
  e.preventDefault();
  currentFilters = Object.fromEntries(new FormData(filtersForm).entries());
  loadInternships(1);
});

loadInternships(1);
