from pathlib import Path
import subprocess

tuner_markdown = """# Mono Component Live Visual Tuner

このツールは、各コンポーネントの余白・フォントサイズ・角丸・シャドウ・配置をブラウザ上でリアルタイムにスライダー調整するためのGUIです。

---

## プレビュー対象コンポーネント

<div id="component-gallery">

<div class="component-card" data-component="mono-badge">
  <h3>mono-badge</h3>
  <div class="component-preview">
    @[badge: 重要](type: "error")
    @[badge: 新機能](type: "info")
    @[badge: 完了](type: "success")
    @[badge: 警告](type: "warning")
  </div>
</div>

<div class="component-card" data-component="mono-link">
  <h3>mono-link</h3>
  <div class="component-preview">
    @[link: Google](url: "https://google.com", description: "世界最大の検索エンジン", image: "https://www.google.com/favicon.ico")
  </div>
</div>

<div class="component-card" data-component="mono-flipcard">
  <h3>mono-flipcard</h3>
  <div class="component-preview">
    @[flipcard: 表面の質問テキスト](back: "裏面の解答テキスト・詳細情報")
  </div>
</div>

<div class="component-card" data-component="mono-poll">
  <h3>mono-poll</h3>
  <div class="component-preview">
    @[poll: プレゼンテーションで最も重要な要素は？](options: "視覚的明瞭さ, 余白の美しさ, インタラクション, テンポ")
  </div>
</div>

<div class="component-card" data-component="mono-dice">
  <h3>mono-dice</h3>
  <div class="component-preview">
    @[dice](sides: "6")
  </div>
</div>

<div class="component-card" data-component="mono-clock">
  <h3>mono-clock</h3>
  <div class="component-preview">
    @[clock](format: "24h")
  </div>
</div>

<div class="component-card" data-component="mono-countdown">
  <h3>mono-countdown</h3>
  <div class="component-preview">
    @[countdown](minutes: "5")
  </div>
</div>

<div class="component-card" data-component="mono-textfield-input">
  <h3>mono-textfield-input</h3>
  <div class="component-preview">
    @[textfield-input: アイデア入力](placeholder: "ここにアイデアを入力してください...")
  </div>
</div>

<div class="component-card" data-component="mono-notebook">
  <h3>mono-notebook</h3>
  <div class="component-preview">
    @[notebook: 講義ノート](id: "tuner-note-1", placeholder: "メモを入力...")
  </div>
</div>

<div class="component-card" data-component="mono-reaction">
  <h3>mono-reaction</h3>
  <div class="component-preview">
    @[reaction](emojis: "👍,🎉,❤️,🚀,🔥")
  </div>
</div>

<div class="component-card" data-component="mono-drawer">
  <h3>mono-drawer</h3>
  <div class="component-preview">
    @[drawer: サイドメニュー]()
    - 項目 1: 概要
    - 項目 2: 仕様
    - 項目 3: 設定
    @[/drawer]
  </div>
</div>

<div class="component-card" data-component="mono-section">
  <h3>mono-section</h3>
  <div class="component-preview">
    @[section: セクションタイトル](padding: "md")
    セクション内のコンテンツ領域です。
    @[/section]
  </div>
</div>

</div>
"""

tools_dir = Path("/Users/ngsklab/Code/Mono/tools")
tools_dir.mkdir(parents=True, exist_ok=True)
md_file = tools_dir / "tuner_base.md"
md_file.write_text(tuner_markdown, encoding="utf-8")

temp_html = tools_dir / "tuner_temp.html"

# Run main.py via subprocess
cmd = ["uv", "run", "main.py", str(md_file), "-o", str(temp_html), "--force"]
subprocess.run(cmd, check=True)

built_html = temp_html.read_text(encoding="utf-8")

# Inject Tuner GUI
tuner_gui_html = """
<!-- ================= MONO VISUAL TUNER PANEL ================= -->
<style>
#tuner-panel-toggle {
  position: fixed;
  bottom: 24px;
  right: 24px;
  z-index: 10000;
  background: #111827;
  color: #fff;
  border: 1px solid #374151;
  padding: 12px 20px;
  border-radius: 30px;
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  box-shadow: 0 10px 25px rgba(0,0,0,0.3);
  display: flex;
  align-items: center;
  gap: 8px;
  transition: transform 0.2s ease, background 0.2s ease;
}
#tuner-panel-toggle:hover {
  transform: scale(1.05);
  background: #2563eb;
}

#tuner-panel {
  position: fixed;
  top: 20px;
  right: 20px;
  width: 380px;
  max-height: calc(100vh - 40px);
  background: rgba(17, 24, 39, 0.96);
  backdrop-filter: blur(16px);
  color: #f3f4f6;
  border: 1px solid #374151;
  border-radius: 12px;
  box-shadow: 0 20px 40px rgba(0,0,0,0.5);
  z-index: 10001;
  display: flex;
  flex-direction: column;
  font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
  font-size: 13px;
  overflow: hidden;
}

#tuner-panel.hidden {
  display: none;
}

.tuner-header {
  padding: 14px 18px;
  background: #1f2937;
  border-bottom: 1px solid #374151;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.tuner-header h2 {
  font-size: 15px;
  font-weight: 700;
  color: #fff;
  margin: 0;
  display: flex;
  align-items: center;
  gap: 6px;
}
.tuner-close-btn {
  background: transparent;
  border: none;
  color: #9ca3af;
  font-size: 20px;
  cursor: pointer;
}
.tuner-close-btn:hover { color: #fff; }

.tuner-body {
  padding: 16px 18px;
  overflow-y: auto;
  flex-grow: 1;
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.tuner-section-title {
  font-size: 11px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: #60a5fa;
  margin-bottom: 8px;
  border-bottom: 1px solid #374151;
  padding-bottom: 4px;
}

.tuner-control-group {
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.tuner-control-label {
  display: flex;
  justify-content: space-between;
  color: #d1d5db;
}
.tuner-control-value {
  font-family: monospace;
  color: #38bdf8;
  font-weight: 600;
}

.tuner-slider {
  width: 100%;
  accent-color: #3b82f6;
  cursor: pointer;
}

.tuner-select {
  width: 100%;
  background: #374151;
  color: #fff;
  border: 1px solid #4b5563;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}

.tuner-footer {
  padding: 14px 18px;
  background: #1f2937;
  border-top: 1px solid #374151;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tuner-btn-primary {
  width: 100%;
  background: #2563eb;
  color: #fff;
  border: none;
  padding: 10px;
  border-radius: 6px;
  font-weight: 700;
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 6px;
  transition: background 0.2s ease;
}
.tuner-btn-primary:hover { background: #1d4ed8; }

.tuner-btn-secondary {
  width: 100%;
  background: #374151;
  color: #d1d5db;
  border: 1px solid #4b5563;
  padding: 6px;
  border-radius: 6px;
  font-size: 12px;
  cursor: pointer;
}
.tuner-btn-secondary:hover { background: #4b5563; color: #fff; }

.component-card {
  margin-bottom: 2rem;
  padding: 1.5rem;
  background: var(--color-base-100, #ffffff);
  border: 1px solid var(--border-color, #e5e7eb);
  border-radius: var(--radius-lg, 0.5rem);
  box-shadow: var(--shadow-sm);
  transition: border-color 0.2s ease;
}
.component-card:hover {
  border-color: #3b82f6;
}
.component-card h3 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.1rem;
  color: var(--color-base-content-muted, #6b7280);
  border-bottom: 1px dashed var(--border-color, #e5e7eb);
  padding-bottom: 0.5rem;
}
.component-preview {
  padding: 0.5rem 0;
}
</style>

<button id="tuner-panel-toggle">🎛️ Live Tuner 開く</button>

<div id="tuner-panel" class="hidden">
  <div class="tuner-header">
    <h2>🎛️ Mono Live Tuner</h2>
    <button class="tuner-close-btn" id="tuner-close">&times;</button>
  </div>
  <div class="tuner-body">
    
    <div>
      <div class="tuner-section-title">プレビュー環境設定</div>
      <div class="tuner-control-group">
        <label class="tuner-control-label">テーマ切り替え</label>
        <select id="theme-select" class="tuner-select">
          <option value="light">Light (標準)</option>
          <option value="dark">Dark (暗色)</option>
          <option value="corporate">Corporate (企業向)</option>
          <option value="calm-study">Calm Study (学習向)</option>
        </select>
      </div>
      <div class="tuner-control-group" style="margin-top: 8px;">
        <label class="tuner-control-label">表示幅シミュレート</label>
        <select id="viewport-select" class="tuner-select">
          <option value="100%">100% (画面いっぱい)</option>
          <option value="1750px">1750px (FHDプロジェクター)</option>
          <option value="1280px">1280px (ノートPC)</option>
          <option value="768px">768px (タブレット)</option>
          <option value="375px">375px (スマートフォン)</option>
        </select>
      </div>
    </div>

    <div>
      <div class="tuner-section-title">角丸トークン (Border Radius)</div>
      
      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--radius-sm (小)</span>
          <span id="val-radius-sm" class="tuner-control-value">0.125rem</span>
        </div>
        <input type="range" id="slider-radius-sm" class="tuner-slider" min="0" max="0.5" step="0.03125" value="0.125">
      </div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--radius-md (中)</span>
          <span id="val-radius-md" class="tuner-control-value">0.25rem</span>
        </div>
        <input type="range" id="slider-radius-md" class="tuner-slider" min="0" max="1.0" step="0.0625" value="0.25">
      </div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--radius-lg (大)</span>
          <span id="val-radius-lg" class="tuner-control-value">0.5rem</span>
        </div>
        <input type="range" id="slider-radius-lg" class="tuner-slider" min="0" max="2.0" step="0.125" value="0.5">
      </div>
    </div>

    <div>
      <div class="tuner-section-title">余白・パディング (Spacing & Padding)</div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--spacing-flow (共通タグマージン: デフォルトlg)</span>
          <span id="val-spacing-flow" class="tuner-control-value">3.5rem</span>
        </div>
        <input type="range" id="slider-spacing-flow" class="tuner-slider" min="0.5" max="6.0" step="0.25" value="3.5">
      </div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--spacing-lg (大余白)</span>
          <span id="val-spacing-lg" class="tuner-control-value">3.5rem</span>
        </div>
        <input type="range" id="slider-spacing-lg" class="tuner-slider" min="1.0" max="6.0" step="0.25" value="3.5">
      </div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--spacing-md (中余白)</span>
          <span id="val-spacing-md" class="tuner-control-value">2rem</span>
        </div>
        <input type="range" id="slider-spacing-md" class="tuner-slider" min="0.5" max="4.0" step="0.25" value="2">
      </div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--padding-lg (大パディング)</span>
          <span id="val-padding-lg" class="tuner-control-value">2.5rem</span>
        </div>
        <input type="range" id="slider-padding-lg" class="tuner-slider" min="0.5" max="5.0" step="0.25" value="2.5">
      </div>
    </div>

    <div>
      <div class="tuner-section-title">コンテナ最大幅 & タイポグラフィ</div>

      <div class="tuner-control-group">
        <div class="tuner-control-label">
          <span>--content-max-width</span>
          <span id="val-max-width" class="tuner-control-value">1800px</span>
        </div>
        <input type="range" id="slider-max-width" class="tuner-slider" min="800" max="2200" step="50" value="1800">
      </div>

      <div class="tuner-control-group" style="margin-top: 8px;">
        <div class="tuner-control-label">
          <span>Base Font Size</span>
          <span id="val-font-size" class="tuner-control-value">18px</span>
        </div>
        <input type="range" id="slider-font-size" class="tuner-slider" min="12" max="24" step="1" value="18">
      </div>
    </div>

  </div>

  <div class="tuner-footer">
    <button id="tuner-export-btn" class="tuner-btn-primary">📋 調整パラメータをJSONコピー</button>
    <button id="tuner-reset-btn" class="tuner-btn-secondary">デフォルト値に戻す</button>
  </div>
</div>

<script>
(() => {
  const toggleBtn = document.getElementById("tuner-panel-toggle");
  const panel = document.getElementById("tuner-panel");
  const closeBtn = document.getElementById("tuner-close");
  const exportBtn = document.getElementById("tuner-export-btn");
  const resetBtn = document.getElementById("tuner-reset-btn");

  const themeSelect = document.getElementById("theme-select");
  const viewportSelect = document.getElementById("viewport-select");

  const sliders = {
    "radius-sm": { el: document.getElementById("slider-radius-sm"), valEl: document.getElementById("val-radius-sm"), unit: "rem", cssVar: "--radius-sm" },
    "radius-md": { el: document.getElementById("slider-radius-md"), valEl: document.getElementById("val-radius-md"), unit: "rem", cssVar: "--radius-md" },
    "radius-lg": { el: document.getElementById("slider-radius-lg"), valEl: document.getElementById("val-radius-lg"), unit: "rem", cssVar: "--radius-lg" },
    "spacing-flow": { el: document.getElementById("slider-spacing-flow"), valEl: document.getElementById("val-spacing-flow"), unit: "rem", cssVar: "--spacing-flow" },
    "spacing-lg": { el: document.getElementById("slider-spacing-lg"), valEl: document.getElementById("val-spacing-lg"), unit: "rem", cssVar: "--spacing-lg" },
    "spacing-md": { el: document.getElementById("slider-spacing-md"), valEl: document.getElementById("val-spacing-md"), unit: "rem", cssVar: "--spacing-md" },
    "padding-lg": { el: document.getElementById("slider-padding-lg"), valEl: document.getElementById("val-padding-lg"), unit: "rem", cssVar: "--padding-lg" },
    "max-width": { el: document.getElementById("slider-max-width"), valEl: document.getElementById("val-max-width"), unit: "px", cssVar: "--content-max-width" },
    "font-size": { el: document.getElementById("slider-font-size"), valEl: document.getElementById("val-font-size"), unit: "px", cssVar: "--tuner-root-font" },
  };

  // Toggle Panel
  toggleBtn.addEventListener("click", () => {
    panel.classList.remove("hidden");
    toggleBtn.style.display = "none";
  });
  closeBtn.addEventListener("click", () => {
    panel.classList.add("hidden");
    toggleBtn.style.display = "flex";
  });

  // Theme Switcher
  themeSelect.addEventListener("change", (e) => {
    document.documentElement.setAttribute("data-theme", e.target.value);
  });

  // Viewport Switcher
  viewportSelect.addEventListener("change", (e) => {
    const val = e.target.value;
    if (val === "100%") {
      document.body.style.maxWidth = "none";
      document.body.style.margin = "0";
    } else {
      document.body.style.maxWidth = val;
      document.body.style.margin = "0 auto";
      document.body.style.boxShadow = "0 0 40px rgba(0,0,0,0.15)";
    }
  });

  // Slider Listeners
  Object.keys(sliders).forEach(key => {
    const conf = sliders[key];
    conf.el.addEventListener("input", (e) => {
      const val = e.target.value + conf.unit;
      conf.valEl.textContent = val;
      if (key === "font-size") {
        document.documentElement.style.fontSize = val;
      } else {
        document.documentElement.style.setProperty(conf.cssVar, val);
      }
    });
  });

  // Export JSON
  exportBtn.addEventListener("click", () => {
    const result = {
      theme: themeSelect.value,
      viewport: viewportSelect.value,
      tokens: {}
    };
    Object.keys(sliders).forEach(key => {
      const conf = sliders[key];
      result.tokens[conf.cssVar] = conf.el.value + conf.unit;
    });

    const jsonStr = JSON.stringify(result, null, 2);
    navigator.clipboard.writeText(jsonStr).then(() => {
      exportBtn.textContent = "✅ クリップボードにコピーしました！";
      setTimeout(() => {
        exportBtn.textContent = "📋 調整パラメータをJSONコピー";
      }, 2500);
    }).catch(() => {
      prompt("以下のパラメータをコピーしてください:", jsonStr);
    });
  });

  // Reset
  resetBtn.addEventListener("click", () => {
    location.reload();
  });

})();
</script>
"""

final_tuner_html = built_html.replace("</body>", f"{tuner_gui_html}\n</body>")
tuner_file = tools_dir / "component_tuner.html"
tuner_file.write_text(final_tuner_html, encoding="utf-8")

if temp_html.exists():
    temp_html.unlink()
if md_file.exists():
    md_file.unlink()

print(f"SUCCESS: Mono Live Visual Tuner successfully built at {tuner_file.absolute()}")
