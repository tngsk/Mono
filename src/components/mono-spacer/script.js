class MonoSpacer extends MonoBaseElement {
    constructor() {
        super();
    }

    connectedCallback() {
        this.mountTemplate('mono-spacer-template');

        const width = this.getAttribute("width");
        const height = this.getAttribute("height");

        if (width) {
            if (!isNaN(width)) {
                this.style.width = width + "px";
            } else {
                this.style.width = width;
            }
        }
        if (height) {
            if (!isNaN(height)) {
                this.style.height = height + "px";
            } else {
                this.style.height = height;
            }
        }
    }
}

if (!customElements.get("mono-spacer")) {
    customElements.define("mono-spacer", MonoSpacer);
}
