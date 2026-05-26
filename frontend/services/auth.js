const AuthService = {
  getUser() {
    const raw = localStorage.getItem("sige_user");
    if (!raw) return null;
    try {
      return JSON.parse(raw);
    } catch {
      return null;
    }
  },

  getToken() {
    return localStorage.getItem("sige_token");
  },

  isAuthenticated() {
    return !!this.getToken();
  },

  saveSession(token, user) {
    localStorage.setItem("sige_token", token);
    localStorage.setItem("sige_user", JSON.stringify(user));
  },

  logout() {
    localStorage.removeItem("sige_token");
    localStorage.removeItem("sige_user");
    window.location.href = "./pages/login.html";
  },

  hasRole(...roles) {
    const user = this.getUser();
    return !!user && roles.includes(user.role);
  },

  canWrite() {
    // Técnico e Administrador podem escrever.
    return this.hasRole("administrador", "tecnico");
  },

  isAdmin() {
    return this.hasRole("administrador");
  },

  requireAuth() {
    if (!this.isAuthenticated()) {
      window.location.href = "./pages/login.html";
      return false;
    }
    return true;
  },

  getRoleLabel(role) {
    const labels = {
      administrador: "Administrador",
      tecnico: "Técnico",
      visitante: "Visitante",
    };
    return labels[role] || role || "";
  },
};

