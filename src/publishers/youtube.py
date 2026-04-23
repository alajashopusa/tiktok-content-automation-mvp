"""YouTube publishing helper (stub).

In production, implement OAuth2 flow and YouTube Data API v3 upload.
This is a minimal placeholder to illustrate wiring from the orchestrator.
"""
from typing import Dict, Optional


def publish_to_youtube(video_path: str, metadata: Dict[str, str], credentials: Optional[Dict] = None, category: Optional[str] = None) -> str:
    print(f"Publishing to YouTube: {video_path} with metadata {metadata}, category={category}")
    return "https://youtube.com/shorts/mock-video-id"
