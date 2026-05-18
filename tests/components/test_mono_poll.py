import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load the parser module dynamically
spec = importlib.util.spec_from_file_location("mono_poll_parser", "src/components/mono-poll/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_poll_basic(parser):
    markdown = '@[poll: "Question"](options: "A,B")'
    html = parser.process(markdown)
    assert '<mono-poll' in html


def test_mono_poll_no_options(parser):
    markdown = '@[poll]()'
    html = parser.process(markdown)
    assert isinstance(html, str)

def test_mono_poll_all_options(parser):
    markdown = '@[poll: "Label"](title: "test", options: "test")'
    html = parser.process(markdown)
    assert isinstance(html, str)
