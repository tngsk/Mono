import xml.etree.ElementTree as etree
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class SlideSectionTreeprocessor(Treeprocessor):
    """
    Wraps content between horizontal rules (---) into <section class="mono-slide">.
    This enables Presentation Focus Mode (P-key) without altering standard markdown flow.
    """
    def run(self, root: etree.Element) -> etree.Element:
        children = list(root)
        if not children:
            return root

        # Check if there is at least one hr element
        has_hr = any(child.tag == "hr" for child in children)
        if not has_hr:
            # If no hr, do not alter the DOM structure to maintain standard document flow
            return root

        new_children = []
        current_section = None
        slide_index = 0

        def start_new_section(idx: int):
            sec = etree.Element("section")
            sec.set("class", "mono-slide")
            sec.set("data-slide-index", str(idx))
            return sec

        for child in children:
            if child.tag == "hr":
                if current_section is not None and len(current_section) > 0:
                    new_children.append(current_section)
                    current_section = None
                    slide_index += 1
                child.set("class", "mono-slide-divider")
                new_children.append(child)
            else:
                if current_section is None:
                    current_section = start_new_section(slide_index)
                current_section.append(child)

        if current_section is not None and len(current_section) > 0:
            new_children.append(current_section)

        root.clear()
        root.extend(new_children)
        return root


class SlideSectionExtension(Extension):
    def extendMarkdown(self, md):
        # Register treeprocessor with a priority lower than standard block processors
        md.treeprocessors.register(SlideSectionTreeprocessor(md), "slide_section", 15)


def makeExtension(**kwargs):
    return SlideSectionExtension(**kwargs)
