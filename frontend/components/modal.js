const Modal = {
  open(title, bodyHtml, footerHtml = "") {
    this.close();

    const overlay = document.createElement("div");
    overlay.className = "modal-overlay active";
    overlay.id = "app-modal";
    overlay.innerHTML = `
      <div class="modal" role="dialog" aria-modal="true">
        <div class="modal-header">
          <h3>${title}</h3>
          <button class="modal-close" aria-label="Fechar">&times;</button>
        </div>
        <div class="modal-body">${bodyHtml}</div>
        ${footerHtml ? `<div class="modal-footer">${footerHtml}</div>` : ""}
      </div>
    `;

    document.body.appendChild(overlay);

    overlay.querySelector(".modal-close").onclick = () => this.close();
    overlay.addEventListener("click", (e) => {
      if (e.target === overlay) this.close();
    });

    return overlay;
  },

  close() {
    const el = document.getElementById("app-modal");
    if (el) el.remove();
  },
};

