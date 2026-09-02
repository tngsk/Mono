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

    def test_slide_section_with_headings(self):
        md_text = """# Chapter 1
Intro text

## Section 1.1
Detail text

## Section 1.2
Another detail"""

        html = markdown.markdown(md_text, extensions=[SlideSectionExtension()])
        self.assertIn('<section class="mono-slide" data-slide-index="0">', html)
        self.assertIn('<section class="mono-slide" data-slide-index="1">', html)
        self.assertIn('<section class="mono-slide" data-slide-index="2">', html)
        self.assertIn('<h1>Chapter 1</h1>', html)
        self.assertIn('<h2>Section 1.1</h2>', html)

    def test_slide_section_plain_text(self):
        md_text = """Plain paragraph 1.

Plain paragraph 2."""

        html = markdown.markdown(md_text, extensions=[SlideSectionExtension()])
        self.assertIn('<section class="mono-slide" data-slide-index="0">', html)
        self.assertIn('<p>Plain paragraph 1.</p>', html)


if __name__ == '__main__':
    unittest.main()
