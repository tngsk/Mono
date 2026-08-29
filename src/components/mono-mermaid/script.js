class MonoMermaid extends MonoBaseElement {
    constructor() {
        super({ shadowMode: 'open' }); this.mountTemplate('mono-mermaid-template');
    }

    connectedCallback() {
        if (super.connectedCallback) {
            super.connectedCallback();
        }
        
        // Handle max-width via CSS variable
        const maxWidth = this.getAttribute('max-width');
        if (maxWidth) {
            this.style.setProperty('--mermaid-max-width', maxWidth);
        }

        // Handle custom background color if set
        const bgColor = this.getAttribute('bg-color');
        if (bgColor) {
            // Check if it's a semantic theme color or arbitrary value
            if (bgColor.startsWith('var(') || bgColor.startsWith('#') || bgColor.startsWith('rgb')) {
                this.style.setProperty('--mermaid-bg-color', bgColor);
            } else {
                // Try resolving it as a semantic color
                this.style.setProperty('--mermaid-bg-color', `var(--color-${bgColor}, ${bgColor})`);
            }
        }
    }
}
customElements.define('mono-mermaid', MonoMermaid);
