if (!requireAuth()) throw new Error("Auth required");

let editingEduId = null;
let lastEducation = [];
const OPTIONAL_FIELDS = ["phone", "college", "course", "year_of_study", "city", "bio", "date_of_birth"];

mountAppShell(
  "profile",
  "Profile",
  `
  <section class="card profile-section">
    <h2>Personal Information</h2>
    <div id="completeness" style="margin-bottom:1rem"></div>
    <form id="profile-form" class="form-grid">
      <div class="form-row">
        <div class="form-group"><label>Full Name</label><input name="full_name" required></div>
        <div class="form-group"><label>WhatsApp / Phone</label><input name="phone" type="tel" placeholder="10-digit mobile number" autocomplete="tel"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>College</label><input name="college"></div>
        <div class="form-group"><label>Course</label><input name="course"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Year of Study</label><input name="year_of_study"></div>
        <div class="form-group"><label>City</label><input name="city"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Date of Birth</label><input name="date_of_birth" type="date"></div>
      </div>
      <div class="form-group"><label>Bio</label><textarea name="bio"></textarea></div>
      <button class="btn btn-primary" type="submit">Save Profile</button>
    </form>
  </section>

  <section class="card profile-section">
    <h2>Education</h2>
    <div id="education-list"></div>
    <form id="education-form" class="form-grid" style="margin-top:1rem">
      <div class="form-row">
        <div class="form-group"><label>Institution</label><input name="institution" required></div>
        <div class="form-group"><label>Degree</label><input name="degree" required></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Field of Study</label><input name="field_of_study"></div>
        <div class="form-group"><label>Grade</label><input name="grade"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Start Year</label><input name="start_year" type="number"></div>
        <div class="form-group"><label>End Year</label><input name="end_year" type="number"></div>
      </div>
      <button class="btn btn-secondary" type="submit" id="edu-submit-btn">Add Education</button>
    </form>
  </section>

  <section class="card profile-section">
    <h2>Skills</h2>
    <div id="skills-list"></div>
    <form id="skill-form" class="form-grid" style="margin-top:1rem">
      <div class="form-group"><label>Skill Name</label><input name="name" required></div>
      <button class="btn btn-secondary" type="submit">Add Skill</button>
    </form>
  </section>

  <section class="card resume-box">
    <h2>Resume Upload</h2>
    <p class="resume-meta">Supported formats: PDF, DOC, DOCX (max 5 MB)</p>
    <div id="resume-info" class="resume-meta">No resume uploaded yet.</div>
    <form id="resume-form">
      <input type="file" name="resume" accept=".pdf,.doc,.docx" required>
      <button class="btn btn-primary" type="submit" style="margin-top:0.8rem">Upload Resume</button>
    </form>
  </section>
  `
);

const profileForm = document.getElementById("profile-form");
const eduForm = document.getElementById("education-form");
const eduSubmitBtn = document.getElementById("edu-submit-btn");

// Profile completeness: optional fields filled / 7
function renderCompleteness(profile) {
  const filled = OPTIONAL_FIELDS.filter((f) => String(profile[f] || "").trim()).length;
  const pct = Math.round((filled / 7) * 100);
  document.getElementById("completeness").innerHTML = `
    <p class="profile-complete-label">${pct}% profile complete</p>
    <div class="progress-bar-wrap"><div class="progress-bar-fill" style="width:${pct}%"></div></div>
  `;
}

function resetEduForm() {
  eduForm.reset();
  editingEduId = null;
  eduSubmitBtn.textContent = "Add Education";
}

function renderEducation(items) {
  lastEducation = items;
  const list = document.getElementById("education-list");
  list.innerHTML = items.length
    ? items
        .map(
          (e) => `
      <div class="education-row">
        <div>
          <strong>${escapeHtml(e.degree)}</strong> · ${escapeHtml(e.institution)}<br>
          <small>${escapeHtml(e.field_of_study || "")} ${escapeHtml(e.start_year || "")}-${escapeHtml(e.end_year || "")}</small>
        </div>
        <div style="display:flex;gap:0.4rem">
          <button class="btn btn-secondary btn-sm" data-edu-id="${escapeHtml(e.id)}">Edit</button>
          <button class="btn btn-danger btn-sm" data-delete-edu="${escapeHtml(e.id)}">Delete</button>
        </div>
      </div>`
        )
        .join("")
    : `<p class="empty-state">No education added yet.</p>`;

  list.querySelectorAll("[data-edu-id]").forEach((btn) => {
    btn.addEventListener("click", () => {
      const e = lastEducation.find((x) => String(x.id) === btn.dataset.eduId);
      if (!e) return;
      editingEduId = e.id;
      ["institution", "degree", "field_of_study", "grade", "start_year", "end_year"].forEach((f) => {
        eduForm.elements[f].value = e[f] ?? "";
      });
      eduSubmitBtn.textContent = "Update";
    });
  });

  list.querySelectorAll("[data-delete-edu]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await API.apiRequest(`/student/education/${btn.dataset.deleteEdu}`, { method: "DELETE" });
      showToast("Education removed", "success");
      resetEduForm();
      loadProfile();
    });
  });
}

function renderSkills(items) {
  const list = document.getElementById("skills-list");
  list.innerHTML = items.length
    ? `<div class="chip-list">${items
        .map(
          (s) =>
            `<span class="chip">${escapeHtml(s.name)} <button data-delete-skill="${escapeHtml(s.id)}" style="border:none;background:none;cursor:pointer">×</button></span>`
        )
        .join("")}</div>`
    : `<p class="empty-state">No skills added yet.</p>`;

  list.querySelectorAll("[data-delete-skill]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await API.apiRequest(`/student/skills/${btn.dataset.deleteSkill}`, { method: "DELETE" });
      showToast("Skill removed", "success");
      loadProfile();
    });
  });
}

function renderResume(resume) {
  const el = document.getElementById("resume-info");
  if (!resume?.original_name) {
    el.textContent = "No resume uploaded yet.";
    return;
  }
  const kb = Math.round((resume.file_size || 0) / 1024);
  el.innerHTML = `${escapeHtml(resume.original_name)} (${kb} KB)
    <button type="button" class="btn btn-outline btn-sm" id="resume-download-btn">Download</button>`;
  document.getElementById("resume-download-btn")?.addEventListener("click", async () => {
    try {
      const token = API.getToken();
      const res = await fetch(`${API.base}/student/resume/file`, {
        credentials: "include",
        headers: token ? { Authorization: `Bearer ${token}` } : {},
      });
      if (!res.ok) throw new Error("Download failed");
      const blob = await res.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = resume.original_name || "resume";
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      showToast(err.message, "error");
    }
  });
}

async function loadProfile() {
  const profile = await API.apiRequest("/student/profile");
  Object.keys(profileForm.elements).forEach((name) => {
    if (profileForm.elements[name] && profile[name] != null) {
      profileForm.elements[name].value = profile[name] || "";
    }
  });
  renderCompleteness(profile);
  renderEducation(profile.education || []);
  renderSkills(profile.skills || []);
  renderResume(await API.apiRequest("/student/resume"));
}

profileForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(profileForm).entries());
  const btn = profileForm.querySelector("button[type='submit']");
  try {
    await withBusy(btn, "Saving profile...", async () => {
      await API.apiRequest("/student/profile", { method: "PUT", body: JSON.stringify(payload) });
      await loadProfile();
    });
    showToast("Profile updated", "success");
  } catch (err) {
    showToast(err.message, "error");
  }
});

eduForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const wasEditing = Boolean(editingEduId);
  const payload = Object.fromEntries(new FormData(eduForm).entries());
  const path = wasEditing ? `/student/education/${editingEduId}` : "/student/education";
  const method = wasEditing ? "PUT" : "POST";
  const btn = eduSubmitBtn;
  try {
    await withBusy(btn, wasEditing ? "Updating..." : "Adding...", async () => {
      await API.apiRequest(path, { method, body: JSON.stringify(payload) });
      await loadProfile();
    });
    resetEduForm();
    showToast(wasEditing ? "Education updated" : "Education added", "success");
  } catch (err) {
    showToast(err.message, "error");
  }
});

document.getElementById("skill-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(e.target).entries());
  const btn = e.target.querySelector("button[type='submit']");
  try {
    await withBusy(btn, "Adding skill...", async () => {
      await API.apiRequest("/student/skills", { method: "POST", body: JSON.stringify(payload) });
      e.target.reset();
      await loadProfile();
    });
    showToast("Skill added", "success");
  } catch (err) {
    showToast(err.message, "error");
  }
});

document.getElementById("resume-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const btn = e.target.querySelector("button[type='submit']");
  try {
    await withBusy(btn, "Uploading resume...", async () => {
      await API.apiRequest("/student/resume", { method: "POST", body: new FormData(e.target) });
      e.target.reset();
      await loadProfile();
    });
    showToast("Resume uploaded", "success");
  } catch (err) {
    showToast(err.message, "error");
  }
});

loadProfile().catch((err) => showToast(err.message, "error"));
