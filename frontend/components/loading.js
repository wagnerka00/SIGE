const Loading = {
  overlay: null,

  init() {
    if (this.overlay) return;
    this.overlay = document.createElement("div");
    this.overlay.className = "loading-overlay";
    this.overlay.innerHTML = '<div class="spinner" aria-label="Carregando"></div>';
    document.body.appendChild(this.overlay);
  },

  show() {
    this.init();
    this.overlay.classList.add("active");
  },

  hide() {
    if (!this.overlay) return;
    this.overlay.classList.remove("active");
  },
};

