import base64
import mimetypes
from pathlib import Path


class Base64MediaEmbedder:
    """
    Template for converting local files into Base64 encoded Data URIs.
    Inspired by Mono's MediaEmbedder (src/embedders/media.py).
    Useful for creating self-contained HTML files without external dependencies.
    """

    def __init__(self):
        # A simple cache to avoid re-encoding the same file multiple times
        self._cache = {}

    def get_mime_type(self, filepath: Path) -> str:
        """Guess the MIME type of a file based on its extension."""
        mime_type, _ = mimetypes.guess_type(str(filepath))
        return mime_type or "application/octet-stream"

    def encode_file_to_data_uri(self, filepath: Path) -> str:
        """
        Reads a local file, encodes it to Base64, and returns a Data URI string
        that can be embedded directly into HTML (e.g. in an <img src="...">).
        """
        if not filepath.exists():
            raise FileNotFoundError(f"File not found: {filepath}")

        # Use file path and modified time as a cache key
        mtime = filepath.stat().st_mtime
        cache_key = f"{filepath.resolve()}_{mtime}"

        if cache_key in self._cache:
            print(f"[DEBUG] Using cached Base64 string for {filepath.name}")
            return self._cache[cache_key]

        print(f"[DEBUG] Reading and encoding file: {filepath.name}")
        try:
            # Read file as binary
            with open(filepath, "rb") as f:
                file_data = f.read()

            # Encode to Base64 and decode to UTF-8 string for HTML injection
            base64_encoded = base64.b64encode(file_data).decode("utf-8")

            # Determine MIME type
            mime_type = self.get_mime_type(filepath)

            # Construct the Data URI
            data_uri = f"data:{mime_type};base64,{base64_encoded}"

            # Save to cache
            self._cache[cache_key] = data_uri

            return data_uri

        except Exception as e:
            raise RuntimeError(f"Failed to encode {filepath}: {e}")


# === Example Usage ===
if __name__ == "__main__":
    # Create a dummy image file for demonstration purposes
    dummy_image_path = Path("dummy_image.png")

    try:
        # Create a tiny 1x1 transparent PNG for testing
        tiny_png = base64.b64decode(
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII="
        )
        with open(dummy_image_path, "wb") as f:
            f.write(tiny_png)

        embedder = Base64MediaEmbedder()

        print("--- First run (should read file) ---")
        data_uri = embedder.encode_file_to_data_uri(dummy_image_path)
        print(f"Generated URI: {data_uri[:50]}...\n")

        print("--- Second run (should use cache) ---")
        cached_uri = embedder.encode_file_to_data_uri(dummy_image_path)
        print(f"Generated URI: {cached_uri[:50]}...\n")

        print("--- HTML Example ---")
        html = f'<img src="{data_uri}" alt="Embedded Image">'
        print(html)

    finally:
        # Cleanup
        if dummy_image_path.exists():
            dummy_image_path.unlink()
