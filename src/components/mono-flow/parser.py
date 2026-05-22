import re
import html
import json
from src.processors.base_parser import BaseComponentParser
from collections import defaultdict, deque

class Parser(BaseComponentParser):
    # OPTIONS: title="text", direction="TB|LR"
    START_PATTERN = r"@\[flow(?:(?:\:\s*)?([^\]]*))\](?:\(((?:[^()]*|\([^()]*\))*)\))?"
    END_PATTERN = r"@\[/flow\]"

    @property
    def block_level_tags(self) -> list[str]:
        return ["mono-flow"]

    def process(self, markdown_content: str) -> str:
        # Match from @[flow] to @[/flow] using a non-greedy wildcard.
        # We need to capture the opening tag, the content, and the closing tag.
        pattern = re.compile(f"({self.START_PATTERN})(.*?)({self.END_PATTERN})", re.DOTALL)

        def replacer(match: re.Match) -> str:
            start_tag = match.group(1)
            bracket_content = match.group(2)
            args_str = match.group(3)
            content = match.group(4)
            end_tag = match.group(5)

            title, specific_args = self.parse_bracket_content(bracket_content)
            common_args = self.parse_key_value_args(args_str) if args_str else {}
            args = {**specific_args, **common_args}

            if 'title' in args:
                title = args['title']

            direction_raw = args.get("direction", "LR").strip("'\"").upper()
            if direction_raw in ("VERTICAL", "TB", "DOWN"):
                direction = "TB"
            elif direction_raw in ("HORIZONTAL", "LR", "RIGHT"):
                direction = "LR"
            else:
                direction = direction_raw

            nodes = set()
            edges = []
            node_order = {}

            def add_node(n: str) -> str:
                n = n.strip()
                if n and n not in node_order:
                    node_order[n] = len(node_order)
                    nodes.add(n)
                return n

            # Parse the content line by line
            lines = content.split('\n')
            last_node = None
            for line in lines:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue

                is_continuation = False
                prefix_match = re.match(r'^(?:->|=>|→)\s*(.*)', line)
                if prefix_match:
                    is_continuation = True
                    line = prefix_match.group(1)

                parts = re.split(r'\s*(?:->|=>|→)\s*', line)
                current_line_nodes = []

                for part in parts:
                    node_name = part
                    label = ""
                    if ':' in node_name:
                        node_part, label_part = node_name.split(':', 1)
                        node_name = node_part.strip()
                        label = label_part.strip()

                    node_name = node_name.strip()
                    current_line_nodes.append((node_name, label))
                    if node_name:
                        add_node(node_name)

                if is_continuation and last_node and current_line_nodes and current_line_nodes[0][0]:
                    edges.append({
                        "from": last_node,
                        "to": current_line_nodes[0][0],
                        "label": current_line_nodes[0][1]
                    })

                # Connect inline nodes
                for i in range(len(current_line_nodes) - 1):
                    n1 = current_line_nodes[i][0]
                    n2 = current_line_nodes[i+1][0]
                    l2 = current_line_nodes[i+1][1]
                    if n1 and n2:
                        edges.append({
                            "from": n1,
                            "to": n2,
                            "label": l2
                        })

                # Update last node
                if current_line_nodes:
                    last_valid = [n for n, l in current_line_nodes if n]
                    if last_valid:
                        last_node = last_valid[-1]

            # Calculate layers
            layers = self._calculate_layers(nodes, edges)

            # Build HTML
            attrs = []
            if title and title.strip():
                 attrs.append(f'title="{html.escape(title.strip())}"')
            attrs.append(f'direction="{html.escape(direction)}"')
            attrs_str = " ".join(attrs)

            result = f'<mono-flow {attrs_str}{self.get_common_attributes(args)}>\n'
            result += '<div class="flow-container">\n'

            # Calculate max layer
            max_layer = max(layers.values()) if layers else 0

            # Group nodes by layer
            layer_to_nodes = defaultdict(list)
            for node, layer in layers.items():
                layer_to_nodes[layer].append(node)

            for layer_idx in range(max_layer + 1):
                if layer_idx in layer_to_nodes:
                    result += f'<div class="flow-layer" data-layer="{layer_idx}">\n'
                    # Sort by original definition order to maintain logical flow and consistent visual order
                    for node in sorted(layer_to_nodes[layer_idx], key=lambda x: node_order.get(x, 0)):
                        safe_node = html.escape(node)
                        # We use data-id to identify the node for SVG path generation
                        result += f'<div class="flow-node" data-id="{safe_node}">{safe_node}</div>\n'
                    result += '</div>\n'

            result += '</div>\n'

            # Embed connections as JSON
            safe_edges = json.dumps(edges).replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026")
            result += f"<script type=\"application/json\" class=\"flow-connections\">{safe_edges}</script>\n"

            result += '</mono-flow>'
            return result

        return pattern.sub(replacer, markdown_content)

    def _calculate_layers(self, nodes: set[str], edges: list[dict]) -> dict[str, int]:
        """
        Calculate the visual layer (depth) of each node using a topological sort / longest path approach.
        Handles cycles by tracking visited nodes in the current path.
        """
        if not nodes:
            return {}

        # Build adjacency list
        adj = defaultdict(list)
        in_degree = {node: 0 for node in nodes}
        for edge in edges:
            u, v = edge['from'], edge['to']
            adj[u].append(v)
            in_degree[v] = in_degree.get(v, 0) + 1

        # Find starting nodes (in-degree 0)
        start_nodes = [node for node in nodes if in_degree[node] == 0]
        if not start_nodes and nodes:
            # Graph might be a single cycle, pick an arbitrary node
            start_nodes = [next(iter(nodes))]

        layers = {node: 0 for node in nodes}

        # Use BFS to find longest path to each node
        queue = deque([(node, 0) for node in start_nodes])
        while queue:
            curr_node, curr_layer = queue.popleft()

            # If we found a longer path, update layer
            if curr_layer > layers[curr_node]:
                layers[curr_node] = curr_layer

            for neighbor in adj[curr_node]:
                # Simple cycle prevention: limit max layer
                # Or just update if we found a strictly longer path and it's less than num_nodes
                if curr_layer + 1 > layers[neighbor] and curr_layer + 1 <= len(nodes):
                    layers[neighbor] = curr_layer + 1
                    queue.append((neighbor, curr_layer + 1))

        # Pull unconnected nodes to layer 0
        for node in nodes:
            if in_degree[node] == 0 and not adj[node]:
                layers[node] = 0

        return layers
