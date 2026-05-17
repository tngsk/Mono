import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load the parser module dynamically
spec = importlib.util.spec_from_file_location("mono_icon_parser", "src/components/mono-icon/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_icon_basic(parser):
    markdown = '@[icon: "home"](size: "md")'
    html = parser.process(markdown)
    assert '<mono-icon name="home" size="md"' in html


def test_mono_icon_no_options(parser):
    markdown = '@[icon]()'
    html = parser.process(markdown)
    assert isinstance(html, str)

def test_mono_icon_all_options(parser):
    markdown = '@[icon: "Label"](name: "test", size: "test", color: "test", display: "test")'
    html = parser.process(markdown)
    assert isinstance(html, str)
