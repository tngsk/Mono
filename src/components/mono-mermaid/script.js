class MonoMermaid extends MonoBaseElement {
    constructor() {
        super({ shadowMode: 'open' }); this.mountTemplate('mono-mermaid-template');
    }
}
customElements.define('mono-mermaid', MonoMermaid);
