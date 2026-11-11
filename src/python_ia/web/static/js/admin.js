const tokenKey = "portfolio_admin_token";

function token() {
  return localStorage.getItem(tokenKey);
}

function authHeaders(json = true) {
  const headers = { Authorization: `Bearer ${token()}` };
  if (json) headers["Content-Type"] = "application/json";
  return headers;
}

function requireToken() {
  if (!token()) window.location.href = "/admin/login";
}

async function api(path, options = {}) {
  const response = await fetch(`/api/v1${path}`, {
    ...options,
    headers: { ...authHeaders(options.body !== undefined), ...(options.headers || {}) },
  });
  if (response.status === 401) {
    localStorage.removeItem(tokenKey);
    window.location.href = "/admin/login";
  }
  return response;
}

async function loadSkills() {
  const response = await api("/skills");
  const skills = await response.json();
  document.querySelector("#skills-list").innerHTML = skills.map((skill) => `
    <span class="badge badge-tech rounded-pill me-2 mb-2 p-2">${skill.name}</span>
  `).join("") || "<span class='text-secondary'>Aucune compétence.</span>";
}

async function loadProjects() {
  const response = await api("/projects");
  const projects = await response.json();
  document.querySelector("#projects-list").innerHTML = projects.map((project) => `
    <div class="list-group-item bg-transparent text-light border-secondary d-flex justify-content-between">
      <span>${project.title}</span><button class="btn btn-sm btn-outline-danger" onclick="removeProject(${project.id})">Supprimer</button>
    </div>
  `).join("") || "<p class='text-secondary'>Aucun projet.</p>";
}

async function removeProject(id) {
  if (!confirm("Supprimer ce projet ?")) return;
  await api(`/projects/${id}`, { method: "DELETE" });
  await loadProjects();
}

document.addEventListener("DOMContentLoaded", () => {
  if (!document.querySelector("#admin-dashboard")) return;
  requireToken();
  loadSkills();
  loadProjects();
  document.querySelector("#logout").onclick = () => {
    localStorage.removeItem(tokenKey);
    window.location.href = "/admin/login";
  };
  document.querySelector("#project-form").onsubmit = async (event) => {
    event.preventDefault();
    const data = Object.fromEntries(new FormData(event.target));
    const response = await api("/projects", { method: "POST", body: JSON.stringify(data) });
    if (response.ok) { event.target.reset(); await loadProjects(); }
  };
});
