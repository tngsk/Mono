import pytest
import importlib.util
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

def load_parser():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    if root_dir not in sys.path:
        sys.path.insert(0, root_dir)

    parser_file = os.path.join(root_dir, "src/components/mono-synth/parser.py")
    spec = importlib.util.spec_from_file_location("mono_synth_parser", parser_file)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Parser()

@pytest.fixture
def parser():
    return load_parser()

def test_mono_synth_parser_basic(parser):
    content = "@[mono-synth]"
    result = parser.process(content)
    assert result == "<mono-synth></mono-synth>"

def test_mono_synth_parser_with_sample(parser):
    content = '@[mono-synth](sample: "asset-mysample.wav")'
    result = parser.process(content)
    assert 'sample="asset-mysample.wav"' in result

def test_mono_synth_parser_with_common_args(parser):
    content = '@[mono-synth](class: "my-synth", padding: "10px")'
    result = parser.process(content)
    assert 'class="my-synth"' in result
    assert 'padding="10px"' in result

def test_mono_synth_parser_fast_path(parser):
    content = "This is a text without mono-synth."
    result = parser.process(content)
    assert result == content
