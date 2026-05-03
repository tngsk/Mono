import re
import html
import json
import subprocess
from pathlib import Path
from markdown.postprocessors import Postprocessor
from markdown.extensions import Extension
import logging

logger = logging.getLogger(__name__)

class CodeBlockPostprocessor(Postprocessor):
    def run(self, text):
        pattern = re.compile(
            r'(<pre><code(?:\s+[^>]+)?>(.*?)</code></pre>)', re.DOTALL
        )

        matches = list(pattern.finditer(text))
        if not matches:
            return text

        batch_data = []
        for match in matches:
            original_block = match.group(1)
            code_content = match.group(2)
            raw_code = html.unescape(code_content)

            language = ""
            lang_match = re.search(r'class="[^"]*language-([^"\s]+)[^"]*"', original_block)
            if lang_match:
                language = lang_match.group(1)

            batch_data.append({"code": raw_code, "language": language})

        highlighted_results = self._highlight_code_batch(batch_data)

        class Replacer:
            def __init__(self):
                self.idx = 0

            def __call__(self, match: re.Match) -> str:
                original_block = match.group(1)

                language = ""
                lang_match = re.search(r'class="[^"]*language-([^"\s]+)[^"]*"', original_block)
                if lang_match:
                    language = lang_match.group(1)

                theme = ""
                theme_match = re.search(r'theme="([^"]*)"', original_block)
                if theme_match:
                    theme = theme_match.group(1)

                highlighted_code = highlighted_results[self.idx]
                self.idx += 1

                highlighted_block = f'<pre><code class="language-{language} hljs">{highlighted_code}</code></pre>'

                theme_attr = f' theme="{theme}"' if theme else ""
                return f'<mono-code-block language="{language}"{theme_attr}>\n{highlighted_block}\n</mono-code-block>'

        return pattern.sub(Replacer(), text)

    def _highlight_code_batch(self, batch_data: list) -> list:
        """Call Node.js script to highlight multiple code blocks."""
        script_path = Path(__file__).parent / "highlight_renderer.js"

        if not script_path.exists():
            logger.warning("highlight_renderer.js not found. Falling back to unhighlighted code.")
            return [html.escape(item["code"]) for item in batch_data]

        try:
            input_data = json.dumps(batch_data)

            result = subprocess.run(
                ["node", str(script_path)],
                input=input_data,
                text=True,
                capture_output=True,
                check=True
            )
            return json.loads(result.stdout)
        except subprocess.CalledProcessError as e:
            logger.error(f"Highlight.js rendering failed: {e.stderr}")
            return [html.escape(item["code"]) for item in batch_data]
        except Exception as e:
            logger.error(f"Highlight.js process execution error: {e}")
            return [html.escape(item["code"]) for item in batch_data]

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(CodeBlockPostprocessor(md), 'code_block', 10)

def makeExtension(**kwargs):
    return CodeBlockExtension(**kwargs)