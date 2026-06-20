import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))
import unittest
import importlib.util

# Load parser.py dynamically since we cannot import it directly due to hyphens in dir name
spec = importlib.util.spec_from_file_location("mono_image_parser", "src/components/mono-image/parser.py")
mono_image_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mono_image_parser)

class TestMonoImageParser(unittest.TestCase):
    def setUp(self):
        self.parser = mono_image_parser.Parser()

    def test_mono_image_basic(self):
        markdown = '@[image: "An image"]()'
        html = self.parser.process(markdown)
        self.assertIn('<img src="An image"', html)
        self.assertIn('alt=""', html)

    def test_mono_image_no_options(self):
        markdown = '@[image]()'
        html = self.parser.process(markdown)
        self.assertIn('<img src=""', html)
        self.assertIn('alt=""', html)

    def test_mono_image_all_options(self):
        markdown = '@[image: "Alt Text"](src: "https://example.com/image.jpg", width: "100px", height: "200px")'
        html = self.parser.process(markdown)
        self.assertIn('src="https://example.com/image.jpg"', html)
        self.assertIn('alt="Alt Text"', html)
        self.assertIn('width: 100px;', html)
        self.assertIn('height: 200px;', html)

if __name__ == '__main__':
    unittest.main()
