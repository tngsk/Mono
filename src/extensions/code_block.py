import html
import json
import logging
import re
import subprocess
from pathlib import Path

from markdown.extensions import Extension
from markdown.postprocessors import Postprocessor

logger = logging.getLogger("markdown_converter")


class CodeBlockPostprocessor(Postprocessor):
    def run(self, text):
        # Match <pre> tags which might contain attributes from extensions like attr_list
        pattern = re.compile(
            r"(<pre(?:\s+[^>]+)?><code(?:\s+[^>]+)?>(.*?)</code></pre>)", re.DOTALL
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
            lang_match = re.search(
                r'class="[^"]*language-([^"\s]+)[^"]*"', original_block
            )
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
            original_pre_and_code = match.group(1)

            language = result_item["language"]

            # Extract existing attributes from both <pre> and <code> tags to preserve them
            # Python-Markdown's attr_list can put attributes on either depending on the fence syntax
            pre_match = re.search(r"<pre([^>]*)>", original_pre_and_code)
            code_tag_match = re.search(r"<code([^>]*)>", original_pre_and_code)

            pre_attrs = pre_match.group(1) if pre_match else ""
            code_attrs = code_tag_match.group(1) if code_tag_match else ""

            # Combine attributes, but we'll extract the theme specifically
            combined_attrs = pre_attrs + " " + code_attrs

            # Extract theme if present in any of the tags
            theme = ""
            theme_match = re.search(r'theme="([^"]*)"', combined_attrs)
            if theme_match:
                theme = theme_match.group(1)

            # Clean up pre_attrs to remove redundant or internal attributes
            # 1. Remove theme attribute as it's passed explicitly
            pre_attrs = re.sub(r'\s*theme="[^"]*"', "", pre_attrs)
            # 2. Remove language class from pre_attrs if it was moved there by some extension
            pre_attrs = re.sub(r'\s*class="[^"]*language-[^"\s]+[^"]*"', "", pre_attrs)

            highlighted_block = f'<pre><code class="language-{language} hljs">{highlighted_code}</code></pre>'

            theme_attr = f' theme="{theme}"' if theme else ""
            return f'<mono-code-block language="{language}"{theme_attr}{pre_attrs}>\n{highlighted_block}\n</mono-code-block>'

        return pattern.sub(replacer, text)

    def _highlight_code_batch(self, blocks: list) -> list:
        """Call Node.js script to highlight multiple code blocks at once."""
        script_path = Path(__file__).parent / "highlight_renderer.js"

        # Fallback if no script
        if not script_path.exists():
            logger.warning(
                "highlight_renderer.js not found. Falling back to unhighlighted code."
            )
            return [
                {"highlighted": html.escape(b["code"]), "language": b["language"]}
                for b in blocks
            ]

        try:
            input_data = json.dumps(blocks)

            result = subprocess.run(
                ["node", str(script_path)],
                input=input_data,
                text=True,
                capture_output=True,
                check=True,
            )

            highlighted_strings = json.loads(result.stdout.strip())

            if len(highlighted_strings) != len(blocks):
                logger.error(
                    "Highlight.js batch process returned incorrect number of results."
                )
                return [
                    {"highlighted": html.escape(b["code"]), "language": b["language"]}
                    for b in blocks
                ]

            return [
                {"highlighted": h_code, "language": b["language"]}
                for h_code, b in zip(highlighted_strings, blocks)
            ]

        except subprocess.CalledProcessError as e:
            logger.error(f"Highlight.js rendering failed: {e.stderr}")
            return [
                {"highlighted": html.escape(b["code"]), "language": b["language"]}
                for b in blocks
            ]
        except Exception as e:
            logger.error(f"Highlight.js process execution error: {e}")
            return [
                {"highlighted": html.escape(b["code"]), "language": b["language"]}
                for b in blocks
            ]


class CodeBlockExtension(Extension):
    def extendMarkdown(self, md):
        md.postprocessors.register(CodeBlockPostprocessor(md), "code_block", 10)


def makeExtension(**kwargs):
    return CodeBlockExtension(**kwargs)
