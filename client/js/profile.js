if (!requireAuth()) throw new Error("Auth required");

mountAppShell(
  "profile",
  "Profile",
  `
  <section class="card profile-section">
    <h2>Personal Information</h2>
    <form id="profile-form" class="form-grid">
      <div class="form-row">
        <div class="form-group"><label>Full Name</label><input name="full_name" required></div>
        <div class="form-group"><label>Phone</label><input name="phone"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>College</label><input name="college"></div>
        <div class="form-group"><label>Course</label><input name="course"></div>
      </div>
      <div class="form-row">
        <div class="form-group"><label>Year of Study</label><input name="year_of_study"></div>
        <div class="form-group"><label>City</label><input name="city"></div>
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
      <button class="btn btn-secondary" type="submit">Add Education</button>
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

async function loadProfile() {
  const profile = await API.apiRequest("/student/profile");
  Object.keys(profileForm.elements).forEach((name) => {
    if (profileForm.elements[name] && profile[name] != null) {
      profileForm.elements[name].value = profile[name] || "";
    }
  });
  renderEducation(profile.education || []);
  renderSkills(profile.skills || []);
  const resume = await API.apiRequest("/student/resume");
  if (resume?.original_name) {
    document.getElementById("resume-info").textContent =
      `Latest: ${resume.original_name} (${Math.round(resume.file_size / 1024)} KB)`;
  }
}

function renderEducation(items) {
  document.getElementById("education-list").innerHTML = items.length
    ? items
        .map(
          (e) => `
      <div class="education-row">
        <div>
          <strong>${e.degree}</strong> · ${e.institution}<br>
          <small>${e.field_of_study || ""} ${e.start_year || ""}-${e.end_year || ""}</small>
        </div>
        <button class="btn btn-danger btn-sm" data-delete-edu="${e.id}">Delete</button>
      </div>`
        )
        .join("")
    : `<p class="empty-state">No education added yet.</p>`;

  document.querySelectorAll("[data-delete-edu]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await API.apiRequest(`/student/education/${btn.dataset.deleteEdu}`, { method: "DELETE" });
      showToast("Education removed", "success");
      loadProfile();
    });
  });
}

function renderSkills(items) {
  document.getElementById("skills-list").innerHTML = items.length
    ? `<div class="chip-list">${items.map((s) => `<span class="chip">${s.name} <button data-delete-skill="${s.id}" style="border:none;background:none;cursor:pointer">×</button></span>`).join("")}</div>`
    : `<p class="empty-state">No skills added yet.</p>`;

  document.querySelectorAll("[data-delete-skill]").forEach((btn) => {
    btn.addEventListener("click", async () => {
      await API.apiRequest(`/student/skills/${btn.dataset.deleteSkill}`, { method: "DELETE" });
      showToast("Skill removed", "success");
      loadProfile();
    });
  });
}

profileForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(profileForm).entries());
  await API.apiRequest("/student/profile", { method: "PUT", body: JSON.stringify(payload) });
  showToast("Profile updated", "success");
});

document.getElementById("education-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(e.target).entries());
  await API.apiRequest("/student/education", { method: "POST", body: JSON.stringify(payload) });
  e.target.reset();
  showToast("Education added", "success");
  loadProfile();
});

document.getElementById("skill-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = Object.fromEntries(new FormData(e.target).entries());
  await API.apiRequest("/student/skills", { method: "POST", body: JSON.stringify(payload) });
  e.target.reset();
  showToast("Skill added", "success");
  loadProfile();
});

document.getElementById("resume-form").addEventListener("submit", async (e) => {
  e.preventDefault();
  const formData = new FormData(e.target);
  await API.apiRequest("/student/resume", { method: "POST", body: formData });
  showToast("Resume uploaded", "success");
  loadProfile();
});

loadProfile().catch((err) => showToast(err.message, "error"));
