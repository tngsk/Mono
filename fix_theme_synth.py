import re

# mono-theme
with open("src/components/mono-theme/parser.py", "r") as f:
    content = f.read()

new_content = re.sub(
    r'FAST_PATH_MARKERS = \("\@\[theme:",\)',
    'FAST_PATH_MARKERS = ("@[theme:",)',
    content
)
with open("src/components/mono-theme/parser.py", "w") as f:
    f.write(new_content)

# mono-synth
with open("src/components/mono-synth/parser.py", "r") as f:
    content = f.read()

new_content = re.sub(
    r'FAST_PATH_MARKERS = \("\@\[mono-synth",\)',
    'FAST_PATH_MARKERS = ("@[mono-synth",)',
    content
)
with open("src/components/mono-synth/parser.py", "w") as f:
    f.write(new_content)

print("Done")
