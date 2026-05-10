import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Load the parser module dynamically
spec = importlib.util.spec_from_file_location("mono_media_grid_parser", "src/components/mono-media-grid/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_media_grid_basic(parser):
    content = "@[media-grid]\ncontent\n@[/media-grid]"
    result = parser.process(content)
    assert '<mono-media-grid markdown="1">' in result
    assert '</mono-media-grid>' in result

def test_mono_media_grid_attributes(parser):
    content = "@[media-grid: columns=3, gap=2rem, fit=contain]\ncontent\n@[/media-grid]"
    result = parser.process(content)
    assert '<mono-media-grid markdown="1" columns="3" gap="2rem" fit="contain">' in result

def test_mono_media_grid_with_class(parser):
    content = "@[media-grid](class=\"my-gallery\")\ncontent\n@[/media-grid]"
    result = parser.process(content)
    assert '<mono-media-grid markdown="1" class="my-gallery">' in result
