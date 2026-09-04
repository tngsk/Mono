class MonoPresenter extends MonoBaseElement {
    constructor() {
        super();
        this.channel = null;
        this.slides = [];
        this.currentSlideIndex = 0;
        this.notes = {};
        this.isPresenterMode = false;
        this.boundHandleKeyDown = this.handleKeyDown.bind(this);
        this.boundHandleScroll = this.handleScroll.bind(this);
        this.boundHandleHashChange = this.handleHashChange.bind(this);
        this.scrollTicking = false;
    }

    connectedCallback() {
        super.mountTemplate('mono-presenter-template');
        this.loadNotes();
        this.extractSlides();
        this.setupChannel();
        this.checkPresenterMode();
        this.setupEventListeners();
    }

    disconnectedCallback() {
        document.removeEventListener('keydown', this.boundHandleKeyDown);
        window.removeEventListener('scroll', this.boundHandleScroll);
        window.removeEventListener('hashchange', this.boundHandleHashChange);
        if (this.channel) {
            this.channel.close();
            this.channel = null;
        }
    }

    loadNotes() {
        const notesScript = document.getElementById('mono-speaker-notes');
        if (notesScript) {
            try {
                this.notes = JSON.parse(notesScript.textContent || '{}');
            } catch (e) {
                this.notes = {};
            }
        }
    }

    extractSlides() {
        const ignoredTags = new Set(['SCRIPT', 'TEMPLATE', 'STYLE', 'MONO-ZOOM', 'MONO-PRESENTER', 'MONO-BRUSH', 'MONO-SYNC']);
        const elements = Array.from(document.body.children).filter(el => !ignoredTags.has(el.tagName));
        if (elements.length === 0) return;

        const hasExplicitHr = elements.some(el => el.tagName === 'HR');

        this.slides = [];
        let currentElements = [];
        let currentTitle = "スライド 1";
        let foundTitleForSlide = false;
        let slideIndex = 0;

        elements.forEach(el => {
            const tag = el.tagName;
            const isHr = (tag === 'HR');
            const isHeading = (!hasExplicitHr) && (tag === 'H1' || tag === 'H2');

            if (isHr || isHeading) {
                if (currentElements.length > 0) {
                    this.slides.push({
                        index: slideIndex,
                        title: currentTitle,
                        firstElement: currentElements[0],
                        note: this.notes[slideIndex] || this.notes[String(slideIndex)] || ''
                    });
                    slideIndex++;
                    currentElements = [];
                    currentTitle = `スライド ${slideIndex + 1}`;
                    foundTitleForSlide = false;
                }
                if (isHr) {
                    return;
                }
            }

            if (!foundTitleForSlide && (tag === 'H1' || tag === 'H2' || tag === 'H3' || tag === 'H4')) {
                currentTitle = el.textContent ? el.textContent.trim() : currentTitle;
                foundTitleForSlide = true;
            }

            currentElements.push(el);
        });

        if (currentElements.length > 0) {
            this.slides.push({
                index: slideIndex,
                title: currentTitle,
                firstElement: currentElements[0],
                note: this.notes[slideIndex] || this.notes[String(slideIndex)] || ''
            });
        }
    }

    checkPresenterMode() {
        const isPresenter = window.location.hash === '#presenter';
        this.isPresenterMode = isPresenter;

        if (isPresenter) {
            this.setAttribute('active', '');
            document.documentElement.setAttribute('data-mono-presenter-mode', 'true');
            this.updatePresenterPanel();
            // 親画面へ最新状態の初期同期を要求
            if (this.channel) {
                this.channel.postMessage({ type: 'request-init' });
            }
        } else {
            this.removeAttribute('active');
            document.documentElement.removeAttribute('data-mono-presenter-mode');
        }
    }

    handleHashChange() {
        this.checkPresenterMode();
    }

    setupChannel() {
        this.boundHandleIncomingMessage = (event) => {
            const data = event.data;
            if (!data) return;

            if (data.type === 'navigate') {
                this.navigateToSlide(data.index, false);
            } else if (data.type === 'state-sync') {
                if (this.isPresenterMode && data.currentIndex !== undefined) {
                    this.currentSlideIndex = data.currentIndex;
                    this.updatePresenterPanel();
                    const slide = this.slides[this.currentSlideIndex];
                    if (slide && slide.firstElement) {
                        slide.firstElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
                    }
                }
            } else if (data.type === 'request-init') {
                if (!this.isPresenterMode) {
                    this.syncToPresenter();
                }
            }
        };

        try {
            this.channel = new BroadcastChannel('mono-presenter-channel');
            this.channel.onmessage = this.boundHandleIncomingMessage;
        } catch (e) {
            // BroadcastChannel非対応環境
        }

        window.addEventListener('message', this.boundHandleIncomingMessage);
    }

    setupEventListeners() {
        const btn = this.shadowRoot.getElementById('presenter-btn');
        if (btn) {
            btn.addEventListener('click', () => this.openPresenterWindow());
        }
        document.addEventListener('keydown', this.boundHandleKeyDown);
        window.addEventListener('scroll', this.boundHandleScroll, { passive: true });
        window.addEventListener('hashchange', this.boundHandleHashChange);
    }

    handleScroll() {
        if (this.isPresenterMode) return;
        if (this.scrollTicking) return;
        this.scrollTicking = true;
        requestAnimationFrame(() => {
            this.updateActiveSlideFromScroll();
            this.scrollTicking = false;
        });
    }

    updateActiveSlideFromScroll() {
        if (this.slides.length === 0) return;
        const scrollY = window.scrollY;
        const viewportHeight = window.innerHeight;
        const focalPoint = viewportHeight * 0.35;

        let bestIndex = 0;
        let minDistance = Infinity;

        this.slides.forEach((slide, idx) => {
            if (!slide.firstElement) return;
            const rect = slide.firstElement.getBoundingClientRect();
            const dist = Math.abs(rect.top - focalPoint);
            if (rect.top <= focalPoint + 120 && dist < minDistance) {
                minDistance = dist;
                bestIndex = idx;
            }
        });

        if (scrollY < 60) {
            bestIndex = 0;
        }

        if (bestIndex !== this.currentSlideIndex) {
            this.currentSlideIndex = Math.min(bestIndex, this.slides.length - 1);
            this.syncToPresenter();
        }
    }

    handleKeyDown(e) {
        const activeEl = document.activeElement;
        const isEditable = activeEl && (
            activeEl.tagName === 'INPUT' ||
            activeEl.tagName === 'TEXTAREA' ||
            activeEl.isContentEditable
        );
        if (isEditable) return;

        if (this.isPresenterMode) {
            // プレゼンターウィンドウ内のスライド移動
            if (e.key === 'ArrowRight' || e.key === 'ArrowDown' || e.key === ' ' || e.key === 'PageDown' || e.key === 'j' || e.key === 'J') {
                this.nextSlide();
                e.preventDefault();
            } else if (e.key === 'ArrowLeft' || e.key === 'ArrowUp' || e.key === 'PageUp' || e.key === 'k' || e.key === 'K') {
                this.prevSlide();
                e.preventDefault();
            }
        } else {
            // 投射画面でのプレゼンターウィンドウ起動
            if (e.key === 'p' || e.key === 'P') {
                this.openPresenterWindow();
                e.preventDefault();
            }
        }
    }

    nextSlide() {
        if (this.currentSlideIndex < this.slides.length - 1) {
            this.navigateToSlide(this.currentSlideIndex + 1, true);
        }
    }

    prevSlide() {
        if (this.currentSlideIndex > 0) {
            this.navigateToSlide(this.currentSlideIndex - 1, true);
        }
    }

    navigateToSlide(targetIndex, broadcast = true) {
        if (targetIndex < 0 || targetIndex >= this.slides.length) return;
        this.currentSlideIndex = targetIndex;

        const targetSlide = this.slides[targetIndex];
        if (targetSlide && targetSlide.firstElement) {
            targetSlide.firstElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }

        if (this.isPresenterMode) {
            this.updatePresenterPanel();
        }

        if (broadcast) {
            const payload = {
                type: 'navigate',
                index: targetIndex
            };
            if (this.channel) {
                try { this.channel.postMessage(payload); } catch (e) {}
            }
            if (window.opener && !window.opener.closed) {
                try { window.opener.postMessage(payload, '*'); } catch (e) {}
            }
        }
    }

    syncToPresenter() {
        const payload = {
            type: 'state-sync',
            currentIndex: this.currentSlideIndex,
            totalSlides: this.slides.length
        };

        if (this.channel) {
            try { this.channel.postMessage(payload); } catch (e) {}
        }
    }

    updatePresenterPanel() {
        const indicator = this.shadowRoot.getElementById('slide-indicator');
        const content = this.shadowRoot.getElementById('script-content');
        if (!indicator || !content) return;

        const total = this.slides.length || 1;
        const current = this.currentSlideIndex + 1;
        indicator.textContent = `スライド ${current} / ${total}`;

        const slide = this.slides[this.currentSlideIndex];
        const noteText = slide && slide.note ? slide.note.trim() : '';

        if (noteText) {
            content.textContent = noteText;
            content.classList.remove('script-empty');
        } else {
            content.textContent = '（トークスクリプトはありません）';
            content.classList.add('script-empty');
        }
    }

    openPresenterWindow() {
        const baseHref = window.location.href.split('#')[0];
        const presenterUrl = `${baseHref}#presenter`;

        const width = 1200;
        const height = 800;
        const left = window.screen.width ? (window.screen.width - width) / 2 : 50;
        const top = window.screen.height ? (window.screen.height - height) / 2 : 50;

        const win = window.open(
            presenterUrl,
            'mono_presenter_view',
            `width=${width},height=${height},left=${left},top=${top},menubar=no,toolbar=no,location=no,status=no,resizable=yes`
        );

        if (!win) {
            alert('ポップアップウィンドウが開けませんでした。ブラウザのポップアップブロックを許可してください。');
            return;
        }

        win.focus();
        setTimeout(() => this.syncToPresenter(), 300);
    }
}

if (!customElements.get('mono-presenter')) {
    customElements.define('mono-presenter', MonoPresenter);
}

// DOM読み込み完了時に自動配置
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        if (!document.querySelector('mono-presenter')) {
            document.body.appendChild(document.createElement('mono-presenter'));
        }
    });
} else {
    if (!document.querySelector('mono-presenter')) {
        document.body.appendChild(document.createElement('mono-presenter'));
    }
}
