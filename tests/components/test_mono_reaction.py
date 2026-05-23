import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load the parser module dynamically
spec = importlib.util.spec_from_file_location("mono_reaction_parser", "src/components/mono-reaction/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_reaction_basic(parser):
    markdown = '@[reaction: "👍"]()'
    html = parser.process(markdown)
    assert '<mono-reaction' in html


def test_mono_reaction_no_options(parser):
    markdown = '@[reaction]()'
    html = parser.process(markdown)
    assert isinstance(html, str)

def test_mono_reaction_all_options(parser):
    markdown = '@[reaction: "Label"](label: "test", options: "test")'
    html = parser.process(markdown)
    assert isinstance(html, str)
