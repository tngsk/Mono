import json
import os
import glob
import re
from pathlib import Path

def generate_snippets():
    snippets = {}

    # 1. Basic markdown extensions / attr_list
    snippets["Markdown attr_list (class, id)"] = {
        "prefix": "[",
        "body": ["[${1:text}]{${2:.class #id}}"],
        "description": "Markdown attr_list extension for custom CSS classes and IDs"
    }

    # 2. Dynamically gather options from parser.py files
    components_with_parsers = {}
    for parser_path in glob.glob("src/components/*/parser.py"):
        comp_name = os.path.basename(os.path.dirname(parser_path)).replace("mono-", "")
        options = []
        with open(parser_path, "r") as f:
            for line in f:
                if "# OPTIONS:" in line:
                    opt_str = line.split("# OPTIONS:")[1].strip()
                    if opt_str:
                        # Safely split by comma using regex lookahead for word characters followed by a colon
                        options = [o.strip() for o in re.split(r',\s*(?=[\w-]+:)', opt_str)]
                    break
        components_with_parsers[comp_name] = options

    implicit_components = {
        "brush": [],
        "sync": [],
        "export": ["filename: \"val\""],
        "code-block": ["language: \"val\""]
    }

    all_components = {**implicit_components, **components_with_parsers}

    for comp, options in all_components.items():
        # Handle special input components with UUIDs
        prefix_comp = comp
        if comp == "textfield-input":
            prefix_comp = "textfield"

        prefix = f"@[{prefix_comp}"

        # Build the arguments string
        if options:
            attr_parts = []
            for i, opt in enumerate(options, start=2):
                if ":" in opt:
                    key = opt.split(":")[0].strip()

                    if key == "id" and prefix_comp in ["textfield", "notebook"]:
                        attr_parts.append(f'{key}: \"${{UUID}}\"')
                    else:
                        attr_parts.append(f'{key}: \"${{{i}:val}}\"')
                else:
                    attr_parts.append(f'{opt}: \"${{{i}:val}}\"')

            attrs = ", ".join(attr_parts)
            body = f"@[{prefix_comp}: \"${{1:Label}}\", {attrs}]"
        else:
            body = f"@[{prefix_comp}: \"${{1:Label}}\"]"

        # If it's an input component without options defined (failsafe)
        if prefix_comp in ["textfield", "notebook"] and "id:" not in body:
            if options:
                body = body[:-1] + f", id: \"${{UUID}}\"]"
            else:
                body = f"@[{prefix_comp}: \"${{1:Label}}\", id: \"${{UUID}}\"]"

        snippets[f"Mono Component: {prefix_comp}"] = {
            "prefix": prefix,
            "body": [body],
            "description": f"Mono {prefix_comp} component"
        }

    # Ensure directories exist
    os.makedirs(".zed/snippets", exist_ok=True)
    os.makedirs(".vscode", exist_ok=True)

    # Write for Zed
    zed_path = Path(".zed/snippets/markdown.json")
    with open(zed_path, "w") as f:
        json.dump(snippets, f, indent=2)
    print(f"Generated {zed_path}")

    # Write for VSCode
    vscode_path = Path(".vscode/mono.code-snippets")
    with open(vscode_path, "w") as f:
        json.dump(snippets, f, indent=2)
    print(f"Generated {vscode_path}")


if __name__ == "__main__":
    generate_snippets()
