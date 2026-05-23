import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load the parser module dynamically
spec = importlib.util.spec_from_file_location("mono_group_assignment_parser", "src/components/mono-group-assignment/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_group_assignment_basic(parser):
    markdown = '@[group-assignment](groups: 3)'
    html = parser.process(markdown)
    assert '<mono-group-assignment' in html


def test_mono_group_assignment_no_options(parser):
    markdown = '@[group-assignment]()'
    html = parser.process(markdown)
    assert isinstance(html, str)

def test_mono_group_assignment_all_options(parser):
    markdown = '@[group-assignment: "Label"](title: "test")'
    html = parser.process(markdown)
    assert isinstance(html, str)
