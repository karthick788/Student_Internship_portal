if (!requireAuth()) throw new Error("Auth required");

mountAppShell(
  "applications",
  "My Applications",
  `<div class="card table-wrap"><table>
    <thead>
      <tr>
        <th>Application ID</th>
        <th>Internship</th>
        <th>Company</th>
        <th>Location</th>
        <th>Status</th>
        <th>Cover Note</th>
        <th>Applied On</th>
      </tr>
    </thead>
    <tbody id="apps-body"><tr><td colspan="7">Loading...</td></tr></tbody>
  </table></div>`
);

const body = document.getElementById("apps-body");

function coverNotePreview(note) {
  if (!note || !String(note).trim()) return "—";
  const text = String(note);
  return escapeHtml(text.length > 60 ? `${text.slice(0, 60)}…` : text);
}

async function loadApplications() {
  body.innerHTML = `<tr><td colspan="7">Loading...</td></tr>`;
  try {
    const items = await API.apiRequest("/applications");
    if (!items.length) {
      body.innerHTML = `<tr><td colspan="7">No applications yet. <a href="internships.html">Browse Internships →</a></td></tr>`;
      return;
    }
    body.innerHTML = items
      .map(
        (a) => `
      <tr>
        <td><strong>${escapeHtml(a.application_code)}</strong></td>
        <td>${escapeHtml(a.title)}</td>
        <td>${escapeHtml(a.company_name)}</td>
        <td>${escapeHtml(a.location) || "N/A"}</td>
        <td>
          ${statusBadge(a.status)}
          <div style="margin-top: 5px;">
            <select class="status-update-select" data-appid="${a.id}" style="font-size: 0.8rem; padding: 2px;">
              <option value="">Update Status...</option>
              <option value="student_selected_next_round">Selected for next round</option>
              <option value="student_rejected">Rejected</option>
              <option value="student_applied">Applied</option>
            </select>
          </div>
        </td>
        <td>${coverNotePreview(a.cover_note)}</td>
        <td>${formatDate(a.created_at)}</td>
      </tr>`
      )
      .join("");
      
      document.querySelectorAll(".status-update-select").forEach(select => {
          select.addEventListener("change", async (e) => {
              const status = e.target.value;
              if (!status) return;
              const appId = e.target.dataset.appid;
              try {
                  await API.apiRequest(`/applications/${appId}/status`, {
                      method: "PATCH",
                      body: JSON.stringify({ status })
                  });
                  showToast("Status updated successfully", "success");
                  loadApplications();
              } catch(err) {
                  showToast(err.message, "error");
                  e.target.value = "";
              }
          });
      });
  } catch (err) {
    body.innerHTML = `<tr><td colspan="7">${escapeHtml(err.message)}</td></tr>`;
  }
}

loadApplications();
