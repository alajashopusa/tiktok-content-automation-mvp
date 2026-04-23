"""Tiny adapter to fetch product image URLs from TikTok Shop.

Note: In production, this should call the official TikTok Shop/Marketplace API
or your backend that exposes product imagery. Here we provide a small, deterministic
stub returning placeholder image URLs for the MVP workflow.
"""
from typing import List


def get_product_image_urls(shop_id: str, limit: int = 5) -> List[str]:
    # Placeholder image URLs (Unsplash) for MVP demonstration
    base = [
        "https://images.unsplash.com/photo-1507679799976-83d8f7fbd3b0",
        "https://images.unsplash.com/photo-1519985175798-46f3f2e0d7b0",
        "https://images.unsplash.com/photo-1523419791800-2b9e0a8f9f63",
        "https://images.unsplash.com/photo-1495567720989-cebdbdd97913",
        "https://images.unsplash.com/photo-1535568538082-5b2a8a1b2d3e",
    ]
    return base[:limit]
