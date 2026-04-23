"""Image capture module: downloads images from provided URLs."""
import os
from urllib.parse import urlparse
import requests


def _ensure_dir(path: str) -> None:
    os.makedirs(path, exist_ok=True)


def capture_images(image_urls, output_dir: str = "output/images") -> list:
    """Download images from a list of URLs to output_dir.

    Returns: list of local file paths
    """
    _ensure_dir(output_dir)
    local_paths = []
    for idx, url in enumerate(image_urls, start=1):
        try:
            resp = requests.get(url, timeout=20)
            resp.raise_for_status()
            parsed = urlparse(url)
            ext = os.path.splitext(parsed.path)[1] or ".jpg"
            out_path = os.path.join(output_dir, f"image_{idx}{ext}")
            with open(out_path, "wb") as f:
                f.write(resp.content)
            local_paths.append(out_path)
        except Exception as e:
            # Skip problematic URLs but continue processing others
            print(f"Warning: failed to download {url}: {e}")
    return local_paths
