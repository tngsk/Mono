import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import unittest
import importlib.util
from pathlib import Path

def load_parser():
    parser_path = Path("src/components/mono-theme/parser.py")
    spec = importlib.util.spec_from_file_location("theme_parser", parser_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Parser()

class TestThemeParser(unittest.TestCase):
    def setUp(self):
        self.parser = load_parser()

    def test_parse_theme(self):
        markdown = "Some text @[theme: dark]() more text"
        html = self.parser.process(markdown)
        self.assertIn('<mono-theme theme="dark" show-ui="false" config=""></mono-theme>', html)

    def test_parse_theme_with_ui(self):
        markdown = "Some text @[theme: corporate](show_ui: true) more text"
        html = self.parser.process(markdown)
        self.assertIn('<mono-theme theme="corporate" show-ui="true" config=""></mono-theme>', html)

    def test_parse_theme_with_font_size(self):
        markdown = "Some text @[theme: light](show_ui: \"true\", font_size: \"20px\") more text"
        html = self.parser.process(markdown)
        self.assertIn('<mono-theme theme="light" show-ui="true" config="" font-size="20px"></mono-theme>', html)

    def test_mono_theme_no_options(self):
        markdown = '@[theme]()'
        html = self.parser.process(markdown)
        self.assertTrue(isinstance(html, str))

    def test_mono_theme_all_options(self):
        markdown = '@[theme: "Label"](theme_name: "test", show_ui: "test", config: "test", font_size: "16px")'
        html = self.parser.process(markdown)
        self.assertTrue(isinstance(html, str))

if __name__ == '__main__':
    unittest.main()
