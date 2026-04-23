"""Video reel builder using MoviePy.

Creates a simple 9:16 reel from a sequence of image files.
"""
from moviepy.editor import ImageClip, concatenate_videoclips
from typing import List


def build_reel(image_paths: List[str], output_path: str, duration_per_image: int = 2, title: str = None) -> str:
    clips = []
    for p in image_paths:
        clip = ImageClip(p).set_duration(duration_per_image)
        clips.append(clip)
    if not clips:
        raise ValueError("No images provided to build reel.")
    video = concatenate_videoclips(clips, method="compose")
    # Basic 9:16 aspect
    video = video.resize(height=1920)
    video = video.set_fps(24)
    # Optionally add a simple title as an overlay is skipped for MVP
    video.write_videofile(output_path, codec="libx264", audio=False, logger=None)
    return output_path
