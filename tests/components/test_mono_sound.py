import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load the parser module dynamically
spec = importlib.util.spec_from_file_location("mono_sound_parser", "src/components/mono-sound/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_sound_basic(parser):
    markdown = '@[sound](src: "test.mp3")'
    html = parser.process(markdown)
    assert 'src="test.mp3"' in html


def test_mono_sound_no_options(parser):
    markdown = '@[sound]()'
    html = parser.process(markdown)
    assert isinstance(html, str)

def test_mono_sound_all_options(parser):
    markdown = '@[sound: "Label"](label: "test", src: "test")'
    html = parser.process(markdown)
    assert isinstance(html, str)
