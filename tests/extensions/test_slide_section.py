import unittest
import markdown
from src.extensions.slide_section import SlideSectionExtension


class TestSlideSectionExtension(unittest.TestCase):
    def test_slide_section_with_hr(self):
        md_text = """# Slide 1
Content of slide 1

---

# Slide 2
Content of slide 2"""

        html = markdown.markdown(md_text, extensions=[SlideSectionExtension()])
        self.assertIn('<section class="mono-slide" data-slide-index="0">', html)
        self.assertIn('<section class="mono-slide" data-slide-index="1">', html)
        self.assertIn('<hr class="mono-slide-divider"', html)
        self.assertIn('<h1>Slide 1</h1>', html)
        self.assertIn('<h1>Slide 2</h1>', html)

    def test_slide_section_without_hr(self):
        md_text = """# Single Document
Single section content"""

        html = markdown.markdown(md_text, extensions=[SlideSectionExtension()])
        self.assertIn('<section class="mono-slide" data-slide-index="0">', html)
        self.assertIn('<h1>Single Document</h1>', html)


if __name__ == '__main__':
    unittest.main()
