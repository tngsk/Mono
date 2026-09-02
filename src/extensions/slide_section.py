import xml.etree.ElementTree as etree
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class SlideSectionTreeprocessor(Treeprocessor):
    """
    Wraps content into <section class="mono-slide"> based on headings (h1, h2) or horizontal rules (---).
    Enables Default Immersive Focus and Section Navigation without requiring manual markup.
    """
    def run(self, root: etree.Element) -> etree.Element:
        children = list(root)
        if not children:
            return root

        # Check if there are headings (h1, h2) or hr elements to structure
        has_boundaries = any(child.tag in ("h1", "h2", "hr") for child in children)
        if not has_boundaries:
            # If plain document with no headings/hr, wrap all in a single focus section
            sec = etree.Element("section")
            sec.set("class", "mono-slide")
            sec.set("data-slide-index", "0")
            for child in children:
                sec.append(child)
            root.clear()
            root.append(sec)
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
            elif child.tag in ("h1", "h2"):
                # When encountering a heading, if we already have content in the current section, start a new section
                if current_section is not None and len(current_section) > 0:
                    new_children.append(current_section)
                    slide_index += 1
                    current_section = start_new_section(slide_index)
                elif current_section is None:
                    current_section = start_new_section(slide_index)
                current_section.append(child)
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
