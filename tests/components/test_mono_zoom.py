import pytest
import os
import sys
import importlib.util

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

def load_parser():
    file_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../src/components/mono-zoom/parser.py'))
    spec = importlib.util.spec_from_file_location("mono_zoom_parser", file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.MonoZoomParser()

@pytest.fixture
def parser():
    return load_parser()

class TestMonoZoomParser:
    def test_process_does_nothing(self, parser):
        # mono-zoom is a system component that just includes assets and handles things on frontend.
        # Its process method should just return the input content unchanged.
        content = "Some markdown @[image: test.png]"
        result = parser.process(content)
        assert result == content
