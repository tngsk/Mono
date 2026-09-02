import xml.etree.ElementTree as etree
from markdown.treeprocessors import Treeprocessor
from markdown.extensions import Extension


class SlideSectionTreeprocessor(Treeprocessor):
    def run(self, root: etree.Element) -> etree.Element:
        children = list(root)
        if not children:
            return root

        # Check if there is at least one hr element or if we should section all top-level blocks
        has_hr = any(child.tag == "hr" for child in children)

        new_children = []
        current_section = None

        def start_new_section():
            sec = etree.Element("section")
            sec.set("class", "mono-slide")
            sec.set("data-zoomable", "true")
            return sec

        for child in children:
            if child.tag == "hr":
                if current_section is not None and len(current_section) > 0:
                    new_children.append(current_section)
                    current_section = None
                # Preserve the hr as a slide divider
                child.set("class", "mono-slide-divider")
                new_children.append(child)
            else:
                if current_section is None:
                    current_section = start_new_section()
                current_section.append(child)

        if current_section is not None and len(current_section) > 0:
            new_children.append(current_section)

        # Replace root children with new_children
        root.clear()
        root.extend(new_children)

        return root


class SlideSectionExtension(Extension):
    def extendMarkdown(self, md):
        # Register treeprocessor with a priority lower than standard block processors
        md.treeprocessors.register(SlideSectionTreeprocessor(md), "slide_section", 15)


def makeExtension(**kwargs):
    return SlideSectionExtension(**kwargs)
