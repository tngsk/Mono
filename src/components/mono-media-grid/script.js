class MonoMediaGrid extends MonoBaseElement {
    constructor() {
        super();
        this.mountTemplate('mono-media-grid-template');
        this.wrapper = this.shadowRoot.querySelector('.grid-wrapper');
    }

    connectedCallback() {
        this.updateStyles();
    }

    static get observedAttributes() {
        return ['columns', 'rows', 'gap', 'fit'];
    }

    attributeChangedCallback() {
        this.updateStyles();
    }

    updateStyles() {
        const columns = this.getAttribute('columns');
        if (columns) {
            this.wrapper.style.gridTemplateColumns = `repeat(${columns}, 1fr)`;
        } else {
            // Default: auto-fit with min-width
            this.wrapper.style.gridTemplateColumns = 'repeat(auto-fit, minmax(150px, 1fr))';
        }

        const rows = this.getAttribute('rows');
        if (rows) {
            this.wrapper.style.gridTemplateRows = `repeat(${rows}, 1fr)`;
        } else {
            this.wrapper.style.gridTemplateRows = 'auto';
        }

        const gap = this.getAttribute('gap');
        if (gap) {
            this.wrapper.style.gap = gap;
        }

        // Apply object-fit to host to allow content.css to pick it up
        const fit = this.getAttribute('fit') || 'cover';
        this.dataset.fit = fit;
        this.style.setProperty('--fit', fit);
    }
}

customElements.define("mono-media-grid", MonoMediaGrid);
