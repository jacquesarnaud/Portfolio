function token() {
  return null;
}

function authHeaders(json = true) {
  const headers = {};
  if (token()) headers.Authorization = `Bearer ${token()}`;
  if (json) headers["Content-Type"] = "application/json";
  return headers;
}

function requireToken() {
  // La page est déjà protégée côté serveur par le cookie HttpOnly.
}

async function api(path, options = {}) {
  const response = await fetch(`/api/v1${path}`, {
    ...options,
    credentials: "same-origin",
    headers: { ...authHeaders(options.body !== undefined), ...(options.headers || {}) },
  });
  if (response.status === 401) {
    window.location.href = "/admin/login";
  }
  return response;
}

function showMessage(message, type = "success") {
  const alert = document.querySelector("#admin-alert");
  alert.textContent = message;
  alert.className = `alert alert-${type}`;
  window.setTimeout(() => alert.classList.add("d-none"), 3500);
}

function escapeHtml(value = "") {
  return String(value).replace(/[&<>'"]/g, (character) => ({
    "&": "&amp;", "<": "&lt;", ">": "&gt;", "'": "&#39;", '"': "&quot;",
  }[character]));
}

function formData(form, booleanFields = []) {
  const data = Object.fromEntries(new FormData(form));
  booleanFields.forEach((field) => { data[field] = form.elements[field].checked; });
  ["display_order", "proficiency"].forEach((field) => {
    if (field in data) data[field] = data[field] === "" ? null : Number(data[field]);
  });
  ["start_date", "end_date"].forEach((field) => {
    if (field in data && data[field] === "") data[field] = null;
  });
  return data;
}

async function submitForm(formId, path, booleanFields, successMessage, callback) {
  const form = document.querySelector(`#${formId}`);
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const response = await api(path, { method: "POST", body: JSON.stringify(formData(form, booleanFields)) });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      showMessage(error.detail || "Impossible d’enregistrer les données.", "danger");
      return;
    }
    form.reset();
    showMessage(successMessage);
    if (callback) await callback();
  });
}

async function loadProfile() {
  const response = await api("/profile");
  if (!response.ok) return;
  const profile = await response.json();
  const form = document.querySelector("#profile-form");
  Object.keys(profile).forEach((key) => {
    if (form.elements[key] && typeof profile[key] !== "boolean") form.elements[key].value = profile[key] || "";
    if (form.elements[key] && typeof profile[key] === "boolean") form.elements[key].checked = profile[key];
  });
}

async function saveProfile() {
  const form = document.querySelector("#profile-form");
  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    const response = await api("/profile", { method: "PUT", body: JSON.stringify(formData(form, ["is_published"])) });
    if (!response.ok) {
      const error = await response.json().catch(() => ({}));
      showMessage(error.detail || "Impossible d’enregistrer le profil.", "danger");
      return;
    }
    showMessage("Profil enregistré. Les informations sont visibles sur le site public.");
  });
}

async function loadSkills() {
  const response = await api("/skills");
  const skills = await response.json();
  document.querySelector("#skills-list").innerHTML = skills.map((skill) => `
    <div class="admin-list-item"><span><strong>${escapeHtml(skill.name)}</strong><small>${escapeHtml(skill.category || "Technologie")}</small></span><button class="btn btn-sm btn-outline-danger" onclick="removeItem('/skills/${skill.id}', loadSkills)">Supprimer</button></div>
  `).join("") || "<p class='text-secondary mb-0'>Aucune compétence.</p>";
}

async function loadProjects() {
  const response = await api("/projects");
  const projects = await response.json();
  document.querySelector("#projects-list").innerHTML = projects.map((project) => `
    <div class="admin-list-item"><span><strong>${escapeHtml(project.title)}</strong><small>${escapeHtml(project.technologies || "Projet")}</small></span><button class="btn btn-sm btn-outline-danger" onclick="removeItem('/projects/${project.id}', loadProjects)">Supprimer</button></div>
  `).join("") || "<p class='text-secondary mb-0'>Aucun projet.</p>";
}

async function loadEducations() {
  const response = await api("/educations");
  const educations = await response.json();
  document.querySelector("#educations-list").innerHTML = educations.map((item) => `
    <div class="admin-list-item"><span><strong>${escapeHtml(item.title)}</strong><small>${escapeHtml(item.institution)}</small></span><button class="btn btn-sm btn-outline-danger" onclick="removeItem('/educations/${item.id}', loadEducations)">Supprimer</button></div>
  `).join("") || "<p class='text-secondary mb-0'>Aucune formation.</p>";
}

async function loadExperiences() {
  const response = await api("/experiences");
  const experiences = await response.json();
  document.querySelector("#experiences-list").innerHTML = experiences.map((item) => `
    <div class="admin-list-item"><span><strong>${escapeHtml(item.position)}</strong><small>${escapeHtml(item.company)}</small></span><button class="btn btn-sm btn-outline-danger" onclick="removeItem('/experiences/${item.id}', loadExperiences)">Supprimer</button></div>
  `).join("") || "<p class='text-secondary mb-0'>Aucune expérience.</p>";
}

async function loadMessages() {
  const response = await api("/contact");
  const list = document.querySelector("#messages-list");
  if (!response.ok) {
    list.innerHTML = "<p class='text-danger mb-0'>Impossible de charger les messages. Vérifiez votre connexion administrateur.</p>";
    return;
  }
  const messages = await response.json();
  list.innerHTML = messages.map((message) => `
    <article class="admin-list-item d-block ${message.is_read ? "" : "border border-info"}">
      <div class="d-flex justify-content-between align-items-start gap-3 flex-wrap">
        <div>
          <strong>${escapeHtml(message.subject || "Sans objet")}</strong>
          <small class="d-block">${escapeHtml(message.sender_name)} · <a href="mailto:${escapeHtml(message.sender_email)}">${escapeHtml(message.sender_email)}</a></small>
          <small class="d-block text-secondary">${escapeHtml(new Date(message.created_at).toLocaleString("fr-FR"))}</small>
        </div>
        <div class="d-flex gap-2">
          ${message.is_read ? "" : `<button class="btn btn-sm btn-outline-info" onclick="markMessageRead(${message.id})">Marquer comme lu</button>`}
          <button class="btn btn-sm btn-outline-danger" onclick="removeItem('/contact/${message.id}', loadMessages)">Supprimer</button>
        </div>
      </div>
      <p class="mb-0 mt-3 text-secondary">${escapeHtml(message.body)}</p>
    </article>
  `).join("") || "<p class='text-secondary mb-0'>Aucun message reçu.</p>";
}

async function markMessageRead(messageId) {
  const response = await api(`/contact/${messageId}/read`, { method: "PATCH" });
  if (response.ok) {
    showMessage("Message marqué comme lu.");
    await loadMessages();
  } else {
    showMessage("Impossible de mettre à jour le message.", "danger");
  }
}

async function removeItem(path, callback) {
  if (!confirm("Supprimer cet élément ?")) return;
  const response = await api(path, { method: "DELETE" });
  if (response.ok) { showMessage("Élément supprimé."); await callback(); }
  else showMessage("Impossible de supprimer cet élément.", "danger");
}

document.addEventListener("DOMContentLoaded", async () => {
  if (!document.querySelector("#admin-dashboard")) return;
  requireToken();
  await Promise.all([loadProfile(), loadSkills(), loadProjects(), loadEducations(), loadExperiences(), loadMessages()]);
  await saveProfile();
  await submitForm("project-form", "/projects", ["is_featured", "is_published"], "Projet ajouté.", loadProjects);
  await submitForm("skill-form", "/skills", ["is_published"], "Compétence ajoutée.", loadSkills);
  await submitForm("education-form", "/educations", ["is_certification", "is_published"], "Formation ajoutée.", loadEducations);
  await submitForm("experience-form", "/experiences", ["is_current", "is_published"], "Expérience ajoutée.", loadExperiences);
  document.querySelector("#logout").onclick = async () => {
    await fetch("/api/v1/auth/logout", { method: "POST", credentials: "same-origin" });
    window.location.href = "/admin/login";
  };
});
