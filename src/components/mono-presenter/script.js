class MonoPresenter extends MonoBaseElement {
    constructor() {
        super();
        this.channel = null;
        this.presenterWindow = null;
        this.slides = []; // Array of { index: number, title: string, html: string, note: string }
        this.currentSlideIndex = 0;
        this.notes = {};
        this.boundHandleKeyDown = this.handleKeyDown.bind(this);
        this.boundHandleScroll = this.handleScroll.bind(this);
        this.scrollTicking = false;
    }

    connectedCallback() {
        super.mountTemplate('mono-presenter-template');
        this.loadNotes();
        this.extractSlides();
        this.setupChannel();
        this.setupEventListeners();
    }

    disconnectedCallback() {
        document.removeEventListener('keydown', this.boundHandleKeyDown);
        window.removeEventListener('scroll', this.boundHandleScroll);
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

        this.slides = [];
        let currentElements = [];
        let currentTitle = "スライド 1";
        let slideIndex = 0;

        elements.forEach(el => {
            const tag = el.tagName;
            if (tag === 'HR') {
                if (currentElements.length > 0) {
                    this.slides.push({
                        index: slideIndex,
                        title: currentTitle,
                        firstElement: currentElements[0],
                        html: currentElements.map(e => e.outerHTML).join('\n'),
                        note: this.notes[slideIndex] || this.notes[String(slideIndex)] || '（トークスクリプトはありません）'
                    });
                    slideIndex++;
                    currentElements = [];
                    currentTitle = `スライド ${slideIndex + 1}`;
                }
            } else if (tag === 'H1' || tag === 'H2') {
                if (currentElements.length > 0) {
                    this.slides.push({
                        index: slideIndex,
                        title: currentTitle,
                        firstElement: currentElements[0],
                        html: currentElements.map(e => e.outerHTML).join('\n'),
                        note: this.notes[slideIndex] || this.notes[String(slideIndex)] || '（トークスクリプトはありません）'
                    });
                    slideIndex++;
                    currentElements = [];
                }
                currentTitle = el.textContent ? el.textContent.trim() : `スライド ${slideIndex + 1}`;
                currentElements.push(el);
            } else {
                currentElements.push(el);
            }
        });

        if (currentElements.length > 0) {
            this.slides.push({
                index: slideIndex,
                title: currentTitle,
                firstElement: currentElements[0],
                html: currentElements.map(e => e.outerHTML).join('\n'),
                note: this.notes[slideIndex] || this.notes[String(slideIndex)] || '（トークスクリプトはありません）'
            });
        }
    }

    setupChannel() {
        try {
            this.channel = new BroadcastChannel('mono-presenter-channel');
            this.channel.onmessage = (event) => {
                const data = event.data;
                if (!data) return;

                if (data.type === 'navigate') {
                    this.navigateToSlide(data.index);
                } else if (data.type === 'request-init') {
                    this.syncToPresenter();
                }
            };
        } catch (e) {
            // BroadcastChannel非対応環境のフォールバック
        }
    }

    setupEventListeners() {
        const btn = this.shadowRoot.getElementById('presenter-btn');
        if (btn) {
            btn.addEventListener('click', () => this.openPresenterWindow());
        }
        document.addEventListener('keydown', this.boundHandleKeyDown);
        window.addEventListener('scroll', this.boundHandleScroll, { passive: true });
    }

    handleScroll() {
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

        // 'P' キーでプレゼンターウィンドウを開く
        if (e.key === 'p' || e.key === 'P') {
            this.openPresenterWindow();
            e.preventDefault();
        }
    }

    navigateToSlide(targetIndex) {
        if (targetIndex < 0 || targetIndex >= this.slides.length) return;
        this.currentSlideIndex = targetIndex;
        
        const targetSlide = this.slides[targetIndex];
        if (targetSlide && targetSlide.firstElement) {
            targetSlide.firstElement.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
        this.syncToPresenter();
    }

    syncToPresenter() {
        if (!this.channel) return;
        const current = this.slides[this.currentSlideIndex] ? {
            index: this.slides[this.currentSlideIndex].index,
            title: this.slides[this.currentSlideIndex].title,
            html: this.slides[this.currentSlideIndex].html,
            note: this.slides[this.currentSlideIndex].note
        } : null;
        const next = this.slides[this.currentSlideIndex + 1] ? {
            index: this.slides[this.currentSlideIndex + 1].index,
            title: this.slides[this.currentSlideIndex + 1].title,
            html: this.slides[this.currentSlideIndex + 1].html,
            note: this.slides[this.currentSlideIndex + 1].note
        } : null;

        this.channel.postMessage({
            type: 'state-sync',
            currentIndex: this.currentSlideIndex,
            totalSlides: this.slides.length,
            currentSlide: current,
            nextSlide: next
        });
    }

    openPresenterWindow() {
        if (this.presenterWindow && !this.presenterWindow.closed) {
            this.presenterWindow.focus();
            this.syncToPresenter();
            return;
        }

        const width = 1150;
        const height = 750;
        const left = window.screen.width ? (window.screen.width - width) / 2 : 50;
        const top = window.screen.height ? (window.screen.height - height) / 2 : 50;

        this.presenterWindow = window.open(
            '',
            'mono_presenter_view',
            `width=${width},height=${height},left=${left},top=${top},menubar=no,toolbar=no,location=no,status=no,resizable=yes`
        );

        if (!this.presenterWindow) {
            alert('ポップアップウィンドウが開けませんでした。ブラウザのポップアップブロックを許可してください。');
            return;
        }

        // プレゼンターウィンドウ用HTML
        const presenterHtml = `<!DOCTYPE html>
<html lang="ja">
<head>
  <meta charset="UTF-8">
  <title>Mono プレゼンタービュー</title>
  <style>
    :root {
      --bg-color: #0f172a;
      --panel-bg: #1e293b;
      --text-color: #f8fafc;
      --text-muted: #94a3b8;
      --border-color: #334155;
      --accent-color: #38bdf8;
    }
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body {
      background-color: var(--bg-color);
      color: var(--text-color);
      font-family: system-ui, -apple-system, sans-serif;
      height: 100vh;
      display: grid;
      grid-template-rows: 56px 1fr;
      overflow: hidden;
    }
    header {
      background-color: var(--panel-bg);
      border-bottom: 1px solid var(--border-color);
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0 1.5rem;
    }
    .header-left { display: flex; align-items: center; gap: 1rem; font-weight: 600; font-size: 1.1rem; }
    .timer-panel { display: flex; align-items: center; gap: 1.25rem; font-family: monospace; font-size: 1.25rem; }
    .timer-display { font-weight: bold; color: var(--accent-color); }
    .btn {
      background: var(--border-color);
      color: var(--text-color);
      border: none;
      padding: 0.35rem 0.75rem;
      border-radius: 4px;
      cursor: pointer;
      font-size: 0.9rem;
    }
    .btn:hover { background: #475569; }
    main {
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 1rem;
      padding: 1rem;
      height: calc(100vh - 56px);
    }
    .column-left { display: grid; grid-template-rows: 1fr 1fr; gap: 1rem; height: 100%; }
    .card {
      background-color: var(--panel-bg);
      border: 1px solid var(--border-color);
      border-radius: 8px;
      display: flex;
      flex-direction: column;
      overflow: hidden;
    }
    .card-header {
      background-color: rgba(0, 0, 0, 0.2);
      padding: 0.5rem 1rem;
      font-size: 0.85rem;
      color: var(--text-muted);
      display: flex;
      justify-content: space-between;
      align-items: center;
      font-weight: 500;
    }
    .preview-container {
      flex: 1;
      padding: 1rem;
      overflow-y: auto;
      background: #ffffff;
      color: #1f2937;
      font-size: 0.85rem;
      line-height: 1.5;
    }
    .notes-container {
      flex: 1;
      padding: 1.5rem;
      overflow-y: auto;
      font-size: 1.25rem;
      line-height: 1.8;
      white-space: pre-wrap;
      word-break: break-word;
    }
    .nav-controls {
      display: flex;
      gap: 0.5rem;
    }
  </style>
</head>
<body>
  <header>
    <div class="header-left">
      <span>Mono Presenter</span>
      <span id="slide-counter" style="color: var(--text-muted); font-size: 0.95rem;">- / -</span>
    </div>
    <div class="timer-panel">
      <div>経過時間: <span id="timer" class="timer-display">00:00:00</span></div>
      <button id="btn-timer-toggle" class="btn">一時停止</button>
      <button id="btn-timer-reset" class="btn">リセット</button>
      <div style="font-size: 1rem; color: var(--text-muted);">現在時刻: <span id="clock">00:00</span></div>
    </div>
  </header>
  <main>
    <div class="column-left">
      <div class="card">
        <div class="card-header">
          <span>現在のスライド</span>
          <div class="nav-controls">
            <button id="btn-prev" class="btn">◀ 前へ (K)</button>
            <button id="btn-next" class="btn">次へ (J/Space) ▶</button>
          </div>
        </div>
        <div id="current-preview" class="preview-container">読み込み中...</div>
      </div>
      <div class="card">
        <div class="card-header">次のスライド（先読み）</div>
        <div id="next-preview" class="preview-container">（次のスライドはありません）</div>
      </div>
    </div>
    <div class="card">
      <div class="card-header">
        <span>トークスクリプト（スピーカーノート）</span>
        <div>
          <button id="btn-font-dec" class="btn">A-</button>
          <button id="btn-font-inc" class="btn">A+</button>
        </div>
      </div>
      <div id="notes-content" class="notes-container">トークスクリプトを読み込んでいます...</div>
    </div>
  </main>
  <script>
    const channel = new BroadcastChannel('mono-presenter-channel');
    let currentIndex = 0;
    let totalSlides = 1;
    let noteFontSize = 1.25;

    // タイマー管理
    let timerSeconds = 0;
    let timerInterval = null;
    let isTimerRunning = true;

    function startTimer() {
      if (timerInterval) clearInterval(timerInterval);
      timerInterval = setInterval(() => {
        if (isTimerRunning) {
          timerSeconds++;
          updateTimerDisplay();
        }
      }, 1000);
    }

    function updateTimerDisplay() {
      const h = String(Math.floor(timerSeconds / 3600)).padStart(2, '0');
      const m = String(Math.floor((timerSeconds % 3600) / 60)).padStart(2, '0');
      const s = String(timerSeconds % 60).padStart(2, '0');
      document.getElementById('timer').textContent = \`\${h}:\${m}:\${s}\`;
    }

    function updateClock() {
      const now = new Date();
      const h = String(now.getHours()).padStart(2, '0');
      const m = String(now.getMinutes()).padStart(2, '0');
      document.getElementById('clock').textContent = \`\${h}:\${m}\`;
    }
    setInterval(updateClock, 1000);
    updateClock();
    startTimer();

    document.getElementById('btn-timer-toggle').addEventListener('click', () => {
      isTimerRunning = !isTimerRunning;
      document.getElementById('btn-timer-toggle').textContent = isTimerRunning ? '一時停止' : '再開';
    });
    document.getElementById('btn-timer-reset').addEventListener('click', () => {
      timerSeconds = 0;
      updateTimerDisplay();
    });

    // フォントサイズ調整
    document.getElementById('btn-font-inc').addEventListener('click', () => {
      noteFontSize = Math.min(noteFontSize + 0.15, 2.5);
      document.getElementById('notes-content').style.fontSize = \`\${noteFontSize}rem\`;
    });
    document.getElementById('btn-font-dec').addEventListener('click', () => {
      noteFontSize = Math.max(noteFontSize - 0.15, 0.9);
      document.getElementById('notes-content').style.fontSize = \`\${noteFontSize}rem\`;
    });

    // ナビゲーション
    function goPrev() {
      if (currentIndex > 0) {
        channel.postMessage({ type: 'navigate', index: currentIndex - 1 });
      }
    }
    function goNext() {
      if (currentIndex < totalSlides - 1) {
        channel.postMessage({ type: 'navigate', index: currentIndex + 1 });
      }
    }
    document.getElementById('btn-prev').addEventListener('click', goPrev);
    document.getElementById('btn-next').addEventListener('click', goNext);

    document.addEventListener('keydown', (e) => {
      if (e.key === 'j' || e.key === 'J' || e.key === ' ' || e.key === 'ArrowRight' || e.key === 'ArrowDown') {
        goNext();
        e.preventDefault();
      } else if (e.key === 'k' || e.key === 'K' || e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
        goPrev();
        e.preventDefault();
      }
    });

    channel.onmessage = (event) => {
      const data = event.data;
      if (!data || data.type !== 'state-sync') return;

      currentIndex = data.currentIndex;
      totalSlides = data.totalSlides;

      document.getElementById('slide-counter').textContent = \`スライド \${currentIndex + 1} / \${totalSlides}\`;
      
      const currentEl = document.getElementById('current-preview');
      const nextEl = document.getElementById('next-preview');
      const notesEl = document.getElementById('notes-content');

      if (data.currentSlide) {
        currentEl.innerHTML = data.currentSlide.html;
        notesEl.textContent = data.currentSlide.note || '（トークスクリプトはありません）';
      } else {
        currentEl.innerHTML = 'スライドがありません';
        notesEl.textContent = '';
      }

      if (data.nextSlide) {
        nextEl.innerHTML = data.nextSlide.html;
      } else {
        nextEl.innerHTML = '<span style="color: #64748b;">（最後のスライドです）</span>';
      }
    };

    // 親画面へ初期化同期を要求
    channel.postMessage({ type: 'request-init' });
  ${'<'}/script>
</body>
</html>`;

        this.presenterWindow.document.open();
        this.presenterWindow.document.write(presenterHtml);
        this.presenterWindow.document.close();

        // 描画完了後に即時同期
        setTimeout(() => this.syncToPresenter(), 200);
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
