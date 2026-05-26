function renderSidebar(activePage) {
  const user = AuthService.getUser();
  const isAdmin = AuthService.isAdmin();

  const items = [
    {
      id: "dashboard",
      href: "./dashboard.html",
      label: "Dashboard",
      icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zm10 0a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"/></svg>`,
    },
    {
      id: "equipments",
      href: "./equipments.html",
      label: "Equipamentos",
      icon: `<svg fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"/></svg>`,
    },
  ];

  if (isAdmin) {
    // Para manter o escopo do pedido (login/dashboard/equipamentos),
    // omitimos tela de usuários.
  }

  const navHtml = items
    .map((item) => {
      const active = activePage === item.id ? "active" : "";
      return `<a href="${item.href}" class="nav-item ${active}">
        ${item.icon}<span>${item.label}</span>
      </a>`;
    })
    .join("");

  return `
    <aside class="sidebar" id="sidebar">
      <div class="sidebar-header">
        <div class="sidebar-brand">
          <div class="brand-icon">UF</div>
          <div>
            <h2>SIGE UFPI</h2>
            <span>Gestão de Equipamentos</span>
          </div>
        </div>
      </div>
      <nav class="sidebar-nav">${navHtml}</nav>
      <div class="sidebar-footer">
        <p>${user?.name || ""}</p>
        <p>Universidade Federal do Piauí</p>
      </div>
    </aside>
  `;
}

function renderHeader(pageTitle) {
  const user = AuthService.getUser();
  return `
    <header class="top-header">
      <div class="header-left">
        <button class="menu-toggle" id="menu-toggle" aria-label="Menu">
          <svg width="24" height="24" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16"/>
          </svg>
        </button>
        <h1 class="page-title">${pageTitle}</h1>
      </div>
      <div class="header-right">
        <button class="theme-toggle" id="theme-toggle" title="Alternar tema">🌓</button>
        <div class="user-info">
          <span>${user?.name || ""}</span>
          <span class="user-badge">${AuthService.getRoleLabel(user?.role)}</span>
        </div>
        <button class="btn btn-secondary btn-sm" id="logout-btn">Sair</button>
      </div>
    </header>
  `;
}

function initLayout(activePage, pageTitle) {
  const app = document.getElementById("app");
  app.innerHTML = `
    <div class="app-layout">
      ${renderSidebar(activePage)}
      <main class="main-content">
        ${renderHeader(pageTitle)}
        <div class="page-content" id="page-content"></div>
      </main>
    </div>
  `;

  document.getElementById("logout-btn").onclick = () => AuthService.logout();
  document.getElementById("theme-toggle").onclick = () => Utils.toggleTheme();

  // Toggle do sidebar em telas pequenas.
  const toggleBtn = document.getElementById("menu-toggle");
  const sidebar = document.getElementById("sidebar");
  if (toggleBtn && sidebar) {
    toggleBtn.onclick = () => sidebar.classList.toggle("open");
  }
}

