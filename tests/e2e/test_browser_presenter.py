import pytest
from pathlib import Path
from src.converter import MarkdownToHTMLConverter
from src.config import ConversionConfig
import logging


def test_presenter_view_dom_and_notes(tmp_path):
    logger = logging.getLogger("test")
    input_file = tmp_path / "slides.md"
    output_file = tmp_path / "slides.html"
    
    input_file.write_text("""# 導入スライド
<!-- 導入のトークスクリプトです -->
本文1

---

## 詳細スライド
<!-- 詳細のトークスクリプトです -->
本文2
""", encoding="utf-8")
    
    config = ConversionConfig(
        input_file=input_file,
        output_file=output_file,
        css_files=None,
        profile="presentation",
        force=True
    )
    
    converter = MarkdownToHTMLConverter(config, logger)
    assert converter.convert() is True
    
    html = output_file.read_text(encoding="utf-8")
    assert "mono-presenter" in html
    assert '<script type="application/json" id="mono-speaker-notes">' in html
    assert "導入のトークスクリプトです" in html
    assert "詳細のトークスクリプトです" in html


def test_presenter_browser_interaction(tmp_path):
    from playwright.sync_api import sync_playwright
    
    logger = logging.getLogger("test")
    input_file = tmp_path / "pres.md"
    output_file = tmp_path / "pres.html"
    
    input_file.write_text("""# スライド1
<!-- スクリプト1 -->
内容1-1

内容1-2

内容1-3

---

# スライド2
<!-- スクリプト2 -->
内容2-1

内容2-2

内容2-3
""", encoding="utf-8")
    
    config = ConversionConfig(
        input_file=input_file,
        output_file=output_file,
        css_files=None,
        profile="presentation",
        force=True
    )
    MarkdownToHTMLConverter(config, logger).convert()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f"file://{output_file.resolve()}")
        
        # mono-presenter がDOM内に存在することを確認
        presenter = page.locator("mono-presenter")
        assert presenter.count() == 1
        
        # スピーカーノートデータが正しくパース可能であることを確認
        notes_data = page.evaluate("JSON.parse(document.getElementById('mono-speaker-notes').textContent)")
        assert len(notes_data) >= 2
        assert "スクリプト1" in notes_data["0"]
        assert "スクリプト2" in notes_data["1"]
        
        # #presenter ハッシュモードのテスト
        page.goto(f"file://{output_file.resolve()}#presenter")
        page.wait_for_timeout(300)
        
        is_presenter_mode = page.evaluate("document.documentElement.getAttribute('data-mono-presenter-mode')")
        assert is_presenter_mode == "true"
        
        indicator_text = page.evaluate("document.querySelector('mono-presenter').shadowRoot.getElementById('slide-indicator').textContent")
        assert "スライド 1" in indicator_text
        
        content_text = page.evaluate("document.querySelector('mono-presenter').shadowRoot.getElementById('script-content').textContent")
        assert "スクリプト1" in content_text
        
        # 矢印キー（Right）で次スライドへ遷移
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(300)
        
        indicator_text_after = page.evaluate("document.querySelector('mono-presenter').shadowRoot.getElementById('slide-indicator').textContent")
        assert "スライド 2" in indicator_text_after
        
        content_text_after = page.evaluate("document.querySelector('mono-presenter').shadowRoot.getElementById('script-content').textContent")
        assert "スクリプト2" in content_text_after
        
        browser.close()


def test_presenter_dual_window_sync(tmp_path):
    from playwright.sync_api import sync_playwright
    
    logger = logging.getLogger("test")
    input_file = tmp_path / "sync.md"
    output_file = tmp_path / "sync.html"
    
    input_file.write_text("""# スライドA
<!-- ノートA -->
スライドAの内容1

スライドAの内容2

スライドAの内容3

---

# スライドB
<!-- ノートB -->
スライドBの内容1

スライドBの内容2

スライドBの内容3
""", encoding="utf-8")
    
    config = ConversionConfig(
        input_file=input_file,
        output_file=output_file,
        css_files=None,
        profile="presentation",
        force=True
    )
    MarkdownToHTMLConverter(config, logger).convert()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        
        # 投射画面（メイン: 大画面 1920x1080）
        main_page = context.new_page()
        main_page.set_viewport_size({"width": 1920, "height": 1080})
        main_page.goto(f"file://{output_file.resolve()}")
        main_page.wait_for_timeout(300)
        
        # プレゼンター画面（子: ノートPC/ウィンドウ 1150x750）
        pres_page = context.new_page()
        pres_page.set_viewport_size({"width": 1150, "height": 750})
        pres_page.goto(f"file://{output_file.resolve()}#presenter")
        pres_page.wait_for_timeout(300)
        
        # プレゼンター側で次へ移動（ArrowRight）
        pres_page.keyboard.press("ArrowRight")
        pres_page.wait_for_timeout(400)
        
        # メイン側のスライドインデックスが追従したことを確認
        main_index = main_page.evaluate("document.querySelector('mono-presenter').currentSlideIndex")
        assert main_index == 1
        
        # プレゼンター側のノートが更新されたことを確認
        note = pres_page.evaluate("document.querySelector('mono-presenter').shadowRoot.getElementById('script-content').textContent")
        assert "ノートB" in note
        
        # プレゼンター側で前へ移動（ArrowLeft）
        pres_page.keyboard.press("ArrowLeft")
        pres_page.wait_for_timeout(400)
        
        main_index_back = main_page.evaluate("document.querySelector('mono-presenter').currentSlideIndex")
        assert main_index_back == 0
        
        browser.close()


def test_presenter_panel_scroll_isolation(tmp_path):
    from playwright.sync_api import sync_playwright

    logger = logging.getLogger("test")
    input_file = tmp_path / "long_pres.md"
    output_file = tmp_path / "long_pres.html"

    # 長文スクリプトを含むスライド
    long_script = "\\n\\n".join([f"トークスクリプト段落{i}: 詳細な説明文がここに入ります。" for i in range(30)])

    input_file.write_text(f"""# スライド1
<!-- {long_script} -->
スライド1本文

---

# スライド2
<!-- 短いノート -->
スライド2本文
""", encoding="utf-8")

    config = ConversionConfig(
        input_file=input_file,
        output_file=output_file,
        css_files=None,
        profile="presentation",
        force=True
    )
    MarkdownToHTMLConverter(config, logger).convert()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": 1200, "height": 800})
        page.goto(f"file://{output_file.resolve()}#presenter")
        page.wait_for_timeout(400)

        # パネルのスクロール可能性を検証
        metrics = page.evaluate('''() => {
            const presenter = document.querySelector('mono-presenter');
            const body = presenter.shadowRoot.querySelector('.panel-body');
            return {
                scrollHeight: body.scrollHeight,
                clientHeight: body.clientHeight,
                scrollTop: body.scrollTop,
                windowY: window.scrollY
            };
        }''')
        assert metrics["scrollHeight"] > metrics["clientHeight"]
        assert metrics["scrollTop"] == 0
        assert metrics["windowY"] == 0

        # パネル中央の座標を特定
        box = page.evaluate('''() => {
            const presenter = document.querySelector('mono-presenter');
            const panelBody = presenter.shadowRoot.querySelector('.panel-body');
            const rect = panelBody.getBoundingClientRect();
            return { x: rect.x + rect.width / 2, y: rect.y + rect.height / 2 };
        }''')

        # パネル上でホイールスクロールを実行
        page.mouse.move(box["x"], box["y"])
        page.mouse.wheel(0, 200)
        page.wait_for_timeout(300)

        after_wheel = page.evaluate('''() => {
            const presenter = document.querySelector('mono-presenter');
            const body = presenter.shadowRoot.querySelector('.panel-body');
            return {
                scrollTop: body.scrollTop,
                windowY: window.scrollY
            };
        }''')
        # パネル本体のみがスクロールし、親ウィンドウは一切スクロールしていないことを検証
        assert after_wheel["scrollTop"] > 0
        assert after_wheel["windowY"] == 0

        # 端まで過剰にスクロール（overscroll）しても親がスクロールしないことを検証
        page.mouse.wheel(0, 5000)
        page.wait_for_timeout(300)

        overscroll_metrics = page.evaluate('''() => {
            const presenter = document.querySelector('mono-presenter');
            const body = presenter.shadowRoot.querySelector('.panel-body');
            return {
                scrollTop: body.scrollTop,
                windowY: window.scrollY
            };
        }''')
        assert overscroll_metrics["scrollTop"] >= metrics["scrollHeight"] - metrics["clientHeight"] - 2
        assert overscroll_metrics["windowY"] == 0

        # スライド切り替え時にスクロール位置が先頭にリセットされることを検証
        page.keyboard.press("ArrowRight")
        page.wait_for_timeout(400)

        reset_metrics = page.evaluate('''() => {
            const presenter = document.querySelector('mono-presenter');
            const body = presenter.shadowRoot.querySelector('.panel-body');
            return {
                currentSlide: presenter.currentSlideIndex,
                scrollTop: body.scrollTop
            };
        }''')
        assert reset_metrics["currentSlide"] == 1
        assert reset_metrics["scrollTop"] == 0

        browser.close()

