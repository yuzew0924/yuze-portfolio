from datetime import datetime
from pathlib import Path


IMAGE_DIR = Path(__file__).resolve().parent / "static" / "images"
WEB_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
DEFAULT_CATEGORY = "Uncategorized"


def get_images():
    images = []

    for image_path in IMAGE_DIR.rglob("*"):
        if not image_path.is_file():
            continue

        extension = image_path.suffix.lower()
        if extension not in WEB_IMAGE_EXTENSIONS:
            continue

        modified_time = image_path.stat().st_mtime
        relative_path = image_path.relative_to(IMAGE_DIR)
        category = relative_path.parts[0] if len(relative_path.parts) > 1 else DEFAULT_CATEGORY
        images.append(
            {
                "filename": image_path.name,
                "path": relative_path.as_posix(),
                "category": category,
                "date": datetime.fromtimestamp(modified_time).strftime("%Y-%m-%d"),
                "sort_key": modified_time,
            }
        )

    return sorted(images, key=lambda image: image["sort_key"], reverse=True)


def get_categories(images):
    return sorted({image["category"] for image in images})
