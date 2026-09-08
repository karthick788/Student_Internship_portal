if (!requireAuth()) throw new Error("Auth required");

mountAppShell("saved", "Saved Internships", `<div id="saved-list" class="internship-grid loading-state">Loading...</div>`);

async function loadSaved() {
  const el = document.getElementById("saved-list");
  try {
    const items = await API.apiRequest("/saved-internships");
    if (!items.length) {
      el.className = "empty-state";
      el.textContent = "You have not saved any internships yet.";
      return;
    }
    el.className = "internship-grid";
    el.innerHTML = items.map((item) => internshipCard(item, { showUnsave: true })).join("");
    document.querySelectorAll("[data-unsave]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        await API.apiRequest(`/saved-internships/${btn.dataset.unsave}`, { method: "DELETE" });
        showToast("Removed from saved list", "success");
        loadSaved();
      });
    });
  } catch (err) {
    el.className = "error-state";
    el.textContent = err.message;
  }
}

loadSaved();
