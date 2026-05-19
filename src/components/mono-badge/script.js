class MonoBadge extends MonoBaseElement {
    constructor() {
        super();

        this.mountTemplate('mono-badge-template');
    }

    connectedCallback() {
        this.render();
    }

    static get observedAttributes() {
        return ['color', 'soft', 'outline'];
    }

    attributeChangedCallback() {
        this.render();
    }

    render() {
        // apply classes based on attributes to the wrapper inside the template
        const wrapper = this.shadowRoot.querySelector('.mono-badge');
        if (!wrapper) return;

        // Reset classes and styles
        wrapper.className = 'mono-badge';
        wrapper.style.removeProperty('--custom-badge-color');

        const color = this.getAttribute('color');
        if (color) {
            const predefinedColors = ['primary', 'secondary', 'accent', 'info', 'success', 'warning', 'error'];
            if (predefinedColors.includes(color)) {
                wrapper.classList.add(`mono-badge-${color}`);
            } else {
                wrapper.classList.add('mono-badge-custom');
                wrapper.style.setProperty('--custom-badge-color', color);
            }
        }

        if (this.hasAttribute('soft')) {
            wrapper.classList.add('mono-badge-soft');
        }

        if (this.hasAttribute('outline')) {
            wrapper.classList.add('mono-badge-outline');
        }
    }
}

customElements.define('mono-badge', MonoBadge);
