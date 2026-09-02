class MonoDrawer extends MonoBaseElement {
  constructor() {
    super();
  }

  connectedCallback() {
    this.mountTemplate('mono-drawer-template');

    const container = this.shadowRoot.getElementById('drawer-container');
    const handle = this.shadowRoot.getElementById('drawer-handle');
    const handleLabel = this.shadowRoot.getElementById('handle-label');

    const label = this.getAttribute('label') || 'Drawer';
    const position = this.getAttribute('position') || 'left';
    const isOpen = this.hasAttribute('open') && this.getAttribute('open') !== 'false';

    // The backend already escapes the HTML attributes during parsing,
    // so we can safely use innerHTML to support basic formatting/icons if they were allowed,
    // but to be absolutely safe against DOM XSS, we use textContent.
    handleLabel.textContent = label;

    container.classList.add(position);
    
    // Add accessibility attributes
    handle.setAttribute('role', 'button');
    handle.setAttribute('tabindex', '0');
    handle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    handle.setAttribute('aria-label', `Toggle ${label} drawer`);

    // Add keyboard support (Enter/Space to toggle)
    handle.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            const isNowOpen = container.classList.toggle('open');
            handle.setAttribute('aria-expanded', isNowOpen ? 'true' : 'false');
        }
    });

    if (isOpen) {
      container.classList.add('open');
    }

    handle.addEventListener('click', () => {
      const isNowOpen = container.classList.toggle('open');
      handle.setAttribute('aria-expanded', isNowOpen ? 'true' : 'false');
    });
  }
}

if (!customElements.get('mono-drawer')) {
    customElements.define('mono-drawer', MonoDrawer);
}
