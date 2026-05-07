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

        blocks_to_highlight = []
        for match in matches:
            original_block = match.group(1)
            code_content = match.group(2)
            raw_code = html.unescape(code_content)

            language = ""
            lang_match = re.search(r'class="[^"]*language-([^"\s]+)[^"]*"', original_block)
            if lang_match:
                language = lang_match.group(1)

            blocks_to_highlight.append({"code": raw_code, "language": language})

        # Batch highlight
        highlighted_results = self._highlight_code_batch(blocks_to_highlight)

        # Replace in text
        def replacer(match: re.Match) -> str:
            # We pop from the beginning since finditer returns them in order
            result_item = highlighted_results.pop(0)
            highlighted_code = result_item["highlighted"]
            original_block = match.group(1)

            language = result_item["language"]
            theme = ""
            theme_match = re.search(r'theme="([^"]*)"', original_block)
            if theme_match:
                theme = theme_match.group(1)

            highlighted_block = f'<pre><code class="language-{language} hljs">{highlighted_code}</code></pre>'

            theme_attr = f' theme="{theme}"' if theme else ""
            return f'<mono-code-block language="{language}"{theme_attr}>\n{highlighted_block}\n</mono-code-block>'

        return pattern.sub(replacer, text)

    def _highlight_code_batch(self, blocks: list) -> list:
        """Call Node.js script to highlight multiple code blocks at once."""
        script_path = Path(__file__).parent / "highlight_renderer.js"

        # Fallback if no script
        if not script_path.exists():
            logger.warning("highlight_renderer.js not found. Falling back to unhighlighted code.")
            return [{"highlighted": html.escape(b["code"]), "language": b["language"]} for b in blocks]

        try:
            input_data = json.dumps(blocks)

            result = subprocess.run(
                ["node", str(script_path)],
                input=input_data,
                text=True,
                capture_output=True,
                check=True
            )

            highlighted_strings = json.loads(result.stdout.strip())

            if len(highlighted_strings) != len(blocks):
                logger.error("Highlight.js batch process returned incorrect number of results.")
                return [{"highlighted": html.escape(b["code"]), "language": b["language"]} for b in blocks]

            return [
                {"highlighted": h_code, "language": b["language"]}
                for h_code, b in zip(highlighted_strings, blocks)
            ]

        except subprocess.CalledProcessError as e:
            logger.error(f"Highlight.js rendering failed: {e.stderr}")
            return [{"highlighted": html.escape(b["code"]), "language": b["language"]} for b in blocks]
        except Exception as e:
            logger.error(f"Highlight.js process execution error: {e}")
            return [{"highlighted": html.escape(b["code"]), "language": b["language"]} for b in blocks]

class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(CodeBlockPostprocessor(md), 'code_block', 10)

def makeExtension(**kwargs):
    return CodeBlockExtension(**kwargs)
