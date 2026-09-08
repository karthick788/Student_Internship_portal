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
        <th>Applied On</th>
      </tr>
    </thead>
    <tbody id="apps-body"><tr><td colspan="6">Loading...</td></tr></tbody>
  </table></div>`
);

async function loadApplications() {
  const body = document.getElementById("apps-body");
  try {
    const items = await API.apiRequest("/applications");
    if (!items.length) {
      body.innerHTML = `<tr><td colspan="6">No applications yet. Browse internships to apply.</td></tr>`;
      return;
    }
    body.innerHTML = items
      .map(
        (a) => `
      <tr>
        <td><strong>${a.application_code}</strong></td>
        <td>${a.title}</td>
        <td>${a.company_name}</td>
        <td>${a.location || "N/A"}</td>
        <td>${statusBadge(a.status)}</td>
        <td>${formatDate(a.created_at)}</td>
      </tr>`
      )
      .join("");
  } catch (err) {
    body.innerHTML = `<tr><td colspan="6">${err.message}</td></tr>`;
  }
}

loadApplications();
