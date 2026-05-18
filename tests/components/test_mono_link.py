import pytest
import sys
import os
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

spec = importlib.util.spec_from_file_location("mono_link_parser", "src/components/mono-link/parser.py")
mono_link_parser = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mono_link_parser)
Parser = mono_link_parser.Parser

def test_link_parser():
    parser = Parser()
    result = parser.process("@[link: \"https://example.com\"]")
    assert "<mono-link url=\"https://example.com\"" in result

    # Test card style defaults
    assert 'card-style="full"' in result


def test_mono_link_no_options():
    parser = Parser()
    markdown = '@[link]()'
    html = parser.process(markdown)
    assert isinstance(html, str)

def test_mono_link_all_options():
    parser = Parser()
    markdown = '@[link: "Label"](url: "test", style: "test")'
    html = parser.process(markdown)
    assert isinstance(html, str)
