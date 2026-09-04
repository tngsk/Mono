from tests.conftest import load_parser


def test_mono_presenter_parsing(load_parser):
    parser = load_parser("mono-presenter")
    text = "# スライドタイトル\n@[presenter]()\n本文"
    output = parser.parse(text)
    assert "<mono-presenter></mono-presenter>" in output
    assert "@[presenter]" not in output


def test_mono_presenter_no_directive(load_parser):
    parser = load_parser("mono-presenter")
    text = "# スライドタイトル\n本文のみ"
    output = parser.parse(text)
    assert output == text
