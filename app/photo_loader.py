from datetime import datetime
from pathlib import Path


IMAGE_DIR = Path(__file__).resolve().parent / "static" / "images"
WEB_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
DEFAULT_CATEGORY = "Uncategorized"
EXTENSION_PRIORITY = {
    ".webp": 0,
    ".jpg": 1,
    ".jpeg": 1,
    ".png": 2,
    ".gif": 3,
}


def get_images():
    image_candidates = {}

    for image_path in IMAGE_DIR.rglob("*"):
        if not image_path.is_file():
            continue

        extension = image_path.suffix.lower()
        if extension not in WEB_IMAGE_EXTENSIONS:
            continue

        modified_time = image_path.stat().st_mtime
        relative_path = image_path.relative_to(IMAGE_DIR)
        category = relative_path.parts[0] if len(relative_path.parts) > 1 else DEFAULT_CATEGORY
        dedupe_key = relative_path.with_suffix("").as_posix().lower()
        image = {
            "filename": image_path.name,
            "path": relative_path.as_posix(),
            "category": category,
            "date": datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d"),
            "sort_key": modified_time,
            "extension_priority": EXTENSION_PRIORITY[extension],
        }

        existing_image = image_candidates.get(dedupe_key)
        if (
            existing_image is None
            or image["extension_priority"] < existing_image["extension_priority"]
        ):
            image_candidates[dedupe_key] = image

    images = image_candidates.values()
    return sorted(images, key=lambda image: image["sort_key"], reverse=True)


def get_categories(images):
    return sorted({image["category"] for image in images})
