import re
import json
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from markdown.postprocessors import Postprocessor


class NotesPreprocessor(Preprocessor):
    """
    Markdown内のHTMLコメント（<!-- ... -->）をトークスクリプトとして抽出し、
    Markdown本文から除去した上でスライド単位に構造化するプリプロセッサ。
    """
    def __init__(self, md):
        super().__init__(md)
        self.comment_pattern = re.compile(r"<!--([\s\S]*?)-->")
        self.slide_break_hr = re.compile(r"^---+\s*$")
        self.slide_break_heading = re.compile(r"^#{1,2}\s+")

    def run(self, lines):
        content = "\n".join(lines)
        
        # スライド境界を検出するために行単位で走査し、各スライドのノートを収集
        notes_by_slide = {}
        cleaned_lines = []
        current_slide_idx = 0
        current_notes = []
        slide_has_content = False

        is_in_code_block = False
        is_in_comment = False
        current_comment_buf = []

        # ドキュメント全体に明示的なスライド区切り（---）が存在するかを判定
        has_explicit_hr = any(bool(self.slide_break_hr.match(line.strip())) for line in lines)

        for line in lines:
            stripped = line.strip()
            
            # 空行の保存
            if not stripped and not is_in_comment:
                cleaned_lines.append(line)
                continue

            # コードブロック内のコメントは無視
            if stripped.startswith("```"):
                is_in_code_block = not is_in_code_block
                cleaned_lines.append(line)
                slide_has_content = True
                continue
            
            if is_in_code_block:
                cleaned_lines.append(line)
                slide_has_content = True
                continue

            # スライド境界（--- を最優先、存在しない場合のみ H1/H2 でフォールバック）
            is_hr = bool(self.slide_break_hr.match(stripped))
            is_heading = (not has_explicit_hr) and bool(self.slide_break_heading.match(stripped))

            if is_hr or is_heading:
                if slide_has_content:
                    if current_notes:
                        notes_by_slide[str(current_slide_idx)] = "\n\n".join(current_notes)
                        current_notes = []
                    current_slide_idx += 1
                    slide_has_content = False
                if is_hr:
                    cleaned_lines.append(line)
                    continue

            # コメントの抽出と行のクリーンアップ
            current_line_output = []
            remaining_line = line

            while "<!--" in remaining_line or is_in_comment:
                if not is_in_comment:
                    start_idx = remaining_line.find("<!--")
                    current_line_output.append(remaining_line[:start_idx])
                    remaining_line = remaining_line[start_idx + 4:]
                    is_in_comment = True
                    current_comment_buf = []

                if is_in_comment:
                    if "-->" in remaining_line:
                        end_idx = remaining_line.find("-->")
                        current_comment_buf.append(remaining_line[:end_idx])
                        full_comment = "\n".join(current_comment_buf).strip()
                        # note: などのプレフィックスがあれば除去
                        clean_note = re.sub(r"^(?:note|talk|script):\s*", "", full_comment, flags=re.IGNORECASE).strip()
                        if clean_note:
                            current_notes.append(clean_note)
                        remaining_line = remaining_line[end_idx + 3:]
                        is_in_comment = False
                        current_comment_buf = []
                    else:
                        current_comment_buf.append(remaining_line)
                        remaining_line = ""
                        break

            if not is_in_comment:
                if remaining_line:
                    current_line_output.append(remaining_line)
                assembled_line = "".join(current_line_output)
                if assembled_line.strip():
                    cleaned_lines.append(assembled_line)
                    slide_has_content = True

        if current_notes:
            notes_by_slide[str(current_slide_idx)] = "\n\n".join(current_notes)

        # Markdownインスタンスにノート辞書を保存
        self.md.speaker_notes = notes_by_slide
        return cleaned_lines


class NotesPostprocessor(Postprocessor):
    """
    抽出したスピーカーノートを安全なJSONスクリプトタグとしてHTMLに埋め込むポストプロセッサ。
    """
    def run(self, text):
        notes = getattr(self.md, "speaker_notes", {})
        if not notes:
            return text
        escaped_json = (
            json.dumps(notes, ensure_ascii=False)
            .replace("<", "\\u003c")
            .replace(">", "\\u003e")
            .replace("&", "\\u0026")
        )
        script_tag = f'<script type="application/json" id="mono-speaker-notes">{escaped_json}</script>'
        return f"{text}\n{script_tag}\n<mono-presenter></mono-presenter>"


class NotesExtension(Extension):
    """スピーカーノート抽出Markdown拡張"""
    def extendMarkdown(self, md):
        md.registerExtension(self)
        md.preprocessors.register(NotesPreprocessor(md), "mono_notes_pre", 25)
        md.postprocessors.register(NotesPostprocessor(md), "mono_notes_post", 25)


def makeExtension(**kwargs):
    return NotesExtension(**kwargs)
