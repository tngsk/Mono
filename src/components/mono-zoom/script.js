class MonoZoom extends MonoBaseElement {
    constructor() {
        super();
        this.targetSelectors = [
            'h1:not(.no-zoom)',
            'h2:not(.no-zoom)',
            'h3:not(.no-zoom)',
            'h4:not(.no-zoom)',
            'ul:not(.no-zoom)',
            'ol:not(.no-zoom)',
            'blockquote:not(.no-zoom)',
            'table:not(.no-zoom)',
            'mono-mermaid:not(.no-zoom)',
            'mono-flow:not(.no-zoom)',
            'mono-image:not(.no-zoom)',
            'mono-code-block:not(.no-zoom)',
            'img:not(.colab-badge):not(.no-zoom)',
            '.mono-math:not(.no-zoom)',
            'mono-score:not(.no-zoom)',
            'mono-section:not(.no-zoom)',
            'mono-hero:not(.no-zoom)',
            'mono-layout:not(.no-zoom)',
            'mono-media-grid:not(.no-zoom)',
            'mono-drawer:not(.no-zoom)',
            'mono-flipcard:not(.no-zoom)',
            '[data-zoomable]'
        ].join(', ');
        
        this.activeTarget = null;
        this.hoverTimeout = null;
        this.isModalOpen = false;
        this.boundHandleMouseOver = this.handleMouseOver.bind(this);
        this.boundHandleMouseLeave = this.handleMouseLeave.bind(this);
        this.boundHandleScroll = this.handleScroll.bind(this);
        this.boundHandleKeyDown = this.handleKeyDown.bind(this);
    }

    connectedCallback() {
        super.mountTemplate('mono-zoom-template');
        this.setupElements();
        this.setupEventListeners();
    }

    disconnectedCallback() {
        this.removeEventListeners();
        if (this.activeTarget) {
            this.activeTarget.removeEventListener('mouseleave', this.boundHandleMouseLeave);
            this.activeTarget = null;
        }
    }

    setupElements() {
        this.trigger = this.shadowRoot.getElementById('zoom-trigger');
        this.overlay = this.shadowRoot.getElementById('zoom-overlay');
        this.closeBtn = this.shadowRoot.getElementById('zoom-close');
        this.content = this.shadowRoot.getElementById('zoom-content');
    }

    setupEventListeners() {
        document.addEventListener('mouseover', this.boundHandleMouseOver);
        document.addEventListener('scroll', this.boundHandleScroll, { passive: true });
        window.addEventListener('resize', this.boundHandleScroll, { passive: true });
        document.addEventListener('keydown', this.boundHandleKeyDown);
        
        this.trigger.addEventListener('click', () => this.openModal());
        this.trigger.addEventListener('mouseenter', () => this.keepTriggerVisible());
        this.trigger.addEventListener('mouseleave', () => this.hideTriggerDelayed());
        
        this.closeBtn.addEventListener('click', () => this.closeModal());
    }

    removeEventListeners() {
        document.removeEventListener('mouseover', this.boundHandleMouseOver);
        document.removeEventListener('scroll', this.boundHandleScroll);
        window.removeEventListener('resize', this.boundHandleScroll);
        document.removeEventListener('keydown', this.boundHandleKeyDown);
    }

    handleMouseOver(e) {
        if (this.isModalOpen) return;

        const target = e.target.closest(this.targetSelectors);
        if (target) {
            // Check if it's already the active target
            if (this.activeTarget === target) {
                this.keepTriggerVisible();
                return;
            }

            // Remove listener from previous target if any
            if (this.activeTarget) {
                this.activeTarget.removeEventListener('mouseleave', this.boundHandleMouseLeave);
            }

            this.activeTarget = target;
            this.activeTarget.addEventListener('mouseleave', this.boundHandleMouseLeave);
            
            this.positionTrigger();
            this.showTrigger();
        }
    }

    handleMouseLeave(e) {
        // If moving to the trigger itself, don't hide
        if (e.relatedTarget === this || this.shadowRoot.contains(e.relatedTarget)) {
            return;
        }
        this.hideTriggerDelayed();
    }

    handleScroll() {
        if (this.activeTarget && !this.trigger.classList.contains('hidden')) {
            this.positionTrigger();
        }
    }

    positionTrigger() {
        if (!this.activeTarget) return;
        const rect = this.activeTarget.getBoundingClientRect();
        
        // Position at top-right corner of the element
        const top = rect.top;
        const right = rect.right;
        
        this.trigger.style.top = `${top}px`;
        this.trigger.style.left = `${right}px`;
    }

    showTrigger() {
        clearTimeout(this.hoverTimeout);
        this.trigger.classList.remove('hidden');
        // Small delay to allow display:block to apply before adding opacity class for transition
        requestAnimationFrame(() => {
            this.trigger.classList.add('visible');
        });
    }

    keepTriggerVisible() {
        clearTimeout(this.hoverTimeout);
    }

    hideTriggerDelayed() {
        clearTimeout(this.hoverTimeout);
        this.hoverTimeout = setTimeout(() => {
            this.hideTrigger();
        }, 100); // Small delay to allow moving mouse to trigger
    }

    hideTrigger() {
        this.trigger.classList.remove('visible');
        setTimeout(() => {
            if (!this.trigger.classList.contains('visible')) {
                this.trigger.classList.add('hidden');
                if (this.activeTarget) {
                    this.activeTarget.removeEventListener('mouseleave', this.boundHandleMouseLeave);
                    this.activeTarget = null;
                }
            }
        }, 200); // Match CSS transition duration
    }

    openModal(target = null) {
        if (target) {
            this.activeTarget = target;
        }
        if (!this.activeTarget) return;
        
        this.isModalOpen = true;
        this.hideTrigger();
        
        // Clear previous light DOM clones if any
        this.innerHTML = '';
        
        // Special handling for web components or regular elements
        let clone;
        if (typeof this.activeTarget.getZoomElement === 'function') {
            const customZoomEl = this.activeTarget.getZoomElement();
            clone = customZoomEl ? customZoomEl.cloneNode(true) : this.activeTarget.cloneNode(true);
        } else if (this.activeTarget.tagName.startsWith('MONO-')) {
            // Check for [data-zoom-content], SVG, pre, img, table inside shadowRoot OR light DOM
            let innerContent = null;
            if (this.activeTarget.shadowRoot) {
                innerContent = this.activeTarget.shadowRoot.querySelector('[data-zoom-content], svg, pre, img, table');
            }
            if (!innerContent) {
                innerContent = this.activeTarget.querySelector('[data-zoom-content], svg, pre, img, table');
            }

            if (innerContent) {
                clone = innerContent.cloneNode(true);
            } else {
                clone = this.activeTarget.cloneNode(true);
            }
        } else {
            clone = this.activeTarget.cloneNode(true);
        }
        
        // Clean up inline positioning styles that might interfere with modal layout
        if (clone.style) {
            clone.style.position = 'relative';
            clone.style.top = 'auto';
            clone.style.left = 'auto';
            clone.style.margin = '0 auto';
        }

        // Prevent duplicate IDs in the DOM tree
        if (clone.removeAttribute) {
            clone.removeAttribute('id');
        }
        if (clone.querySelectorAll) {
            clone.querySelectorAll('[id]').forEach(el => el.removeAttribute('id'));
        }

        // We append to this to place it in the Light DOM.
        // It will project into the `<slot></slot>` inside `#zoom-content`.
        this.appendChild(clone);
        
        // Show overlay
        this.overlay.classList.remove('hidden');
        
        // Focus management
        this.previousActiveElement = document.activeElement;
        this.closeBtn.focus();
        
        // Prevent body scroll
        document.body.style.overflow = 'hidden';
    }

    closeModal() {
        this.isModalOpen = false;
        this.overlay.classList.add('hidden');
        this.innerHTML = '';
        
        // Restore focus
        if (this.previousActiveElement) {
            this.previousActiveElement.focus();
        }
        
        // Restore body scroll
        document.body.style.overflow = '';
        
        // Reset active target
        this.activeTarget = null;
    }

    handleKeyDown(e) {
        // Ignore shortcut keys when typing inside editable fields
        const activeEl = document.activeElement;
        const isEditable = activeEl && (
            activeEl.tagName === 'INPUT' ||
            activeEl.tagName === 'TEXTAREA' ||
            activeEl.tagName === 'SELECT' ||
            activeEl.isContentEditable
        );

        // Toggle zoom on 'Z' key press
        if (!isEditable && (e.key === 'z' || e.key === 'Z')) {
            if (this.isModalOpen) {
                this.closeModal();
                e.preventDefault();
                return;
            } else if (this.activeTarget) {
                this.openModal();
                e.preventDefault();
                return;
            }
        }

        if (!this.isModalOpen) return;

        if (e.key === 'Escape') {
            this.closeModal();
            e.preventDefault();
            return;
        }
        
        // Focus trap
        if (e.key === 'Tab') {
            const shadowFocusables = Array.from(this.overlay.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'));
            const lightFocusables = Array.from(this.querySelectorAll('button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'));
            const focusableElements = [...shadowFocusables, ...lightFocusables];
            if (focusableElements.length === 0) return;
            
            const firstElement = focusableElements[0];
            const lastElement = focusableElements[focusableElements.length - 1];
            const currentActive = this.shadowRoot.activeElement || document.activeElement;
            
            if (e.shiftKey) {
                if (currentActive === firstElement || currentActive === this) {
                    lastElement.focus();
                    e.preventDefault();
                }
            } else {
                if (currentActive === lastElement) {
                    firstElement.focus();
                    e.preventDefault();
                }
            }
        }
    }
}

if (!customElements.get('mono-zoom')) {
    customElements.define('mono-zoom', MonoZoom);
}

// Automatically inject into page
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!document.querySelector('mono-zoom')) {
            document.body.appendChild(document.createElement('mono-zoom'));
        }
    });
} else {
    if (!document.querySelector('mono-zoom')) {
        document.body.appendChild(document.createElement('mono-zoom'));
    }
}
