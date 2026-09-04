import logging
from src.converter import MarkdownToHTMLConverter
from src.config import ConversionConfig


def test_presentation_profile_injects_presenter_and_notes(tmp_path):
    logger = logging.getLogger("test")
    input_file = tmp_path / "slides.md"
    output_file = tmp_path / "slides.html"
    
    input_file.write_text("""# タイトルスライド
<!-- ここは導入のトークスクリプトです -->
本文テキスト

---

# 2枚目のスライド
<!-- note: 2枚目の詳細な発表原稿です -->
次の内容
""", encoding="utf-8")
    
    config = ConversionConfig(
        input_file=input_file,
        output_file=output_file,
        css_files=None,
        profile="presentation",
        force=True
    )
    
    converter = MarkdownToHTMLConverter(config, logger)
    converter.convert()
    
    assert output_file.exists()
    html_content = output_file.read_text(encoding="utf-8")
    
    # プレゼンターコンポーネントが注入されていること
    assert "mono-presenter" in html_content
    # スピーカーノートJSONタグが注入されていること
    assert '<script type="application/json" id="mono-speaker-notes">' in html_content
    assert "導入のトークスクリプトです" in html_content
    assert "2枚目の詳細な発表原稿です" in html_content
