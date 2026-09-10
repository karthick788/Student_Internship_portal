if (!requireAuth()) throw new Error("Auth required");

mountAppShell("saved", "Saved Internships", `<div id="saved-list" class="internship-grid"></div>`);

const listEl = document.getElementById("saved-list");

async function loadSaved() {
  listEl.className = "internship-grid";
  listEl.innerHTML = renderSkeleton(6);
  try {
    const items = await API.apiRequest("/saved-internships");
    if (!items.length) {
      listEl.className = "empty-state";
      listEl.innerHTML = `You haven't saved any internships yet. <a href="internships.html">Browse Internships</a>`;
      return;
    }
    listEl.innerHTML = items.map((item) => internshipCard(item, { showUnsave: true })).join("");
    listEl.querySelectorAll("[data-unsave]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        if (!confirm("Remove this internship from saved?")) return;
        try {
          await API.apiRequest(`/saved-internships/${btn.dataset.unsave}`, { method: "DELETE" });
          showToast("Removed from saved list", "success");
          loadSaved();
        } catch (err) {
          showToast(err.message, "error");
        }
      });
    });
  } catch (err) {
    listEl.className = "error-state";
    listEl.innerHTML = `<p>${escapeHtml(err.message)}</p><button class="btn btn-primary" id="retry-btn">Retry</button>`;
    document.getElementById("retry-btn")?.addEventListener("click", loadSaved);
  }
}

loadSaved();
