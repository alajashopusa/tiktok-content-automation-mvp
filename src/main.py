"""Orchestrator for TikTok Shop -> Reels -> Pinterest/YouTube Shorts."""
import argparse
import os
import logging

from tiktok_api import get_product_image_urls
from image_capture import capture_images
from video_builder import build_reel
from publishers.pinterest import publish_to_pinterest
from publishers.youtube import publish_to_youtube

logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


def main(args: argparse.Namespace) -> None:
    shop_id = args.shop_id
    board_id = args.board_id
    youtube_category = args.youtube_category
    output_dir = args.output_dir or "outputs"
    images_dir = os.path.join(output_dir, "images")
    reel_path = os.path.join(output_dir, "reel.mp4")

    logging.info("Starting automation for shop_id=%s", shop_id)
    image_urls = get_product_image_urls(shop_id, limit=5)
    logging.info("Fetched %d image URLs", len(image_urls))

    image_paths = capture_images(image_urls, output_dir=images_dir)
    logging.info("Downloaded %d images to %s", len(image_paths), images_dir)

    if not image_paths:
        logging.error("No images available to build reel. Aborting.")
        return

    reel_path = build_reel(image_paths, reel_path, duration_per_image=2, title=f"{shop_id} Reel")
    logging.info("Created reel at %s", reel_path)

    metadata = {
        "title": f"New Reel from {shop_id}",
        "description": "Automated reel generated from TikTok Shop images",
        "tags": "#TikTok #Reels #Marketing",
    }

    publish_to_pinterest(reel_path, metadata, board_id=board_id)
    publish_to_youtube(reel_path, metadata, credentials=None, category=youtube_category or "Shorts")
    logging.info("Workflow completed.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="TikTok Shop → Reels → Pinterest/YouTube Shorts automation")
    parser.add_argument("--shop-id", required=True, help="TikTok Shop ID or identifier for the shop")
    parser.add_argument("--board-id", required=False, help="Pinterest Board ID to publish to")
    parser.add_argument("--youtube-category", required=False, help="YouTube category (e.g., Shorts)")
    parser.add_argument("--output-dir", required=False, help="Output directory for assets (default: outputs)")
    args = parser.parse_args()
    main(args)
