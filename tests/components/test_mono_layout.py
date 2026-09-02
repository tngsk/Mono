import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

spec = importlib.util.spec_from_file_location("mono_layout_parser", "src/components/mono-layout/parser.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
Parser = module.Parser

@pytest.fixture
def parser():
    return Parser()

def test_mono_layout_hbox(parser):
    markdown = """@[hbox](class: "gap-md")
:::
Left
:::
:::
Right
:::
@[/hbox]"""
    html = parser.process(markdown)
    assert '<mono-layout type="hbox" class="gap-md"' in html
    assert '<div class="column" markdown="1">\nLeft\n</div>' in html
    assert '<div class="column" markdown="1">\nRight\n</div>' in html

def test_mono_layout_vbox(parser):
    markdown = """@[vbox](class: "center")
:::
Top
:::
:::
Bottom
:::
@[/vbox]"""
    html = parser.process(markdown)
    assert '<mono-layout type="vbox" class="center"' in html
    assert 'Top' in html
    assert 'Bottom' in html

def test_mono_layout_aliases(parser):
    markdown = """@[hstack]
:::
Left
:::
:::
Right
:::
@[/hstack]"""
    html = parser.process(markdown)
    assert '<mono-layout type="hbox"' in html

    markdown_row = """@[row]
:::
A
:::
@[/row]"""
    html_row = parser.process(markdown_row)
    assert '<mono-layout type="hbox"' in html_row
