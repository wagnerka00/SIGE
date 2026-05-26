const Utils = {
  initTheme() {
    const saved = localStorage.getItem("sige_theme") || "light";
    document.documentElement.setAttribute("data-theme", saved);
  },

  toggleTheme() {
    const current =
      document.documentElement.getAttribute("data-theme") || "light";
    const next = current === "light" ? "dark" : "light";
    document.documentElement.setAttribute("data-theme", next);
    localStorage.setItem("sige_theme", next);
  },

  debounce(fn, delay = 350) {
    let t;
    return (...args) => {
      clearTimeout(t);
      t = setTimeout(() => fn(...args), delay);
    };
  },

  getApiErrorMessage(err) {
    return (
      err?.response?.data?.message ||
      err?.message ||
      "Erro ao processar solicitação"
    );
  },

  formatDate(iso) {
    if (!iso) return "-";
    try {
      return new Date(iso).toLocaleString("pt-BR");
    } catch {
      return "-";
    }
  },

  statusOptions() {
    return [
      { value: "disponivel", label: "Disponível" },
      { value: "em_uso", label: "Em uso" },
      { value: "em_manutencao", label: "Em manutenção" },
      { value: "descartado", label: "Descartado" },
      { value: "reservado", label: "Reservado" },
    ];
  },

  roleOptions() {
    return [
      { value: "administrador", label: "Administrador" },
      { value: "tecnico", label: "Técnico" },
      { value: "visitante", label: "Visitante" },
    ];
  },
};

Utils.initTheme();

