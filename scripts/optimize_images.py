#!/usr/bin/env python3
import argparse
from pathlib import Path

from PIL import Image, ImageOps


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE_DIR = PROJECT_ROOT / "photos-original"
DEFAULT_OUTPUT_DIR = PROJECT_ROOT / "app" / "static" / "images"
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
SKIPPED_EXTENSIONS = {".heic", ".heif"}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Optimize original photos into web-ready gallery images."
    )
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE_DIR,
        help="Folder containing original photos. Defaults to photos-original/.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=DEFAULT_OUTPUT_DIR,
        help="Folder for optimized website images. Defaults to app/static/images/.",
    )
    parser.add_argument(
        "--max-width",
        type=int,
        default=2000,
        help="Maximum output width in pixels. Defaults to 2000.",
    )
    parser.add_argument(
        "--quality",
        type=int,
        default=82,
        help="WebP quality from 1 to 100. Defaults to 82.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild images even when the optimized output is newer.",
    )
    return parser.parse_args()


def iter_source_images(source_dir):
    for path in sorted(source_dir.rglob("*")):
        if path.is_file():
            yield path


def should_skip(source_path, output_path, force):
    if force:
        return False
    if not output_path.exists():
        return False
    return output_path.stat().st_mtime >= source_path.stat().st_mtime


def resized_dimensions(width, height, max_width):
    if width <= max_width:
        return width, height

    ratio = max_width / width
    return max_width, round(height * ratio)


def optimize_image(source_path, output_path, max_width, quality):
    with Image.open(source_path) as image:
        image = ImageOps.exif_transpose(image)

        if image.mode not in ("RGB", "L"):
            image = image.convert("RGB")

        width, height = resized_dimensions(image.width, image.height, max_width)
        if (width, height) != image.size:
            image = image.resize((width, height), Image.Resampling.LANCZOS)

        output_path.parent.mkdir(parents=True, exist_ok=True)
        image.save(output_path, "WEBP", quality=quality, method=6)


def display_path(path):
    try:
        return path.relative_to(PROJECT_ROOT)
    except ValueError:
        return path


def main():
    args = parse_args()
    source_dir = args.source.resolve()
    output_dir = args.output.resolve()

    if not source_dir.exists():
        print(f"Source folder does not exist: {source_dir}")
        print("Create it and put original photos there, preserving category folders.")
        return 1

    processed = 0
    skipped = 0
    skipped_heic = 0
    failed = 0

    for source_path in iter_source_images(source_dir):
        extension = source_path.suffix.lower()

        if extension in SKIPPED_EXTENSIONS:
            skipped_heic += 1
            print(f"skip HEIC/HEIF: {source_path.relative_to(source_dir)}")
            continue

        if extension not in SUPPORTED_EXTENSIONS:
            skipped += 1
            continue

        relative_path = source_path.relative_to(source_dir)
        output_path = output_dir / relative_path.with_suffix(".webp")

        if should_skip(source_path, output_path, args.force):
            skipped += 1
            continue

        try:
            optimize_image(source_path, output_path, args.max_width, args.quality)
        except Exception as error:
            failed += 1
            print(f"failed: {relative_path} ({error})")
            continue

        processed += 1
        print(f"optimized: {relative_path} -> {display_path(output_path)}")

    print()
    print(f"Processed: {processed}")
    print(f"Skipped: {skipped}")
    print(f"Skipped HEIC/HEIF: {skipped_heic}")
    print(f"Failed: {failed}")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
