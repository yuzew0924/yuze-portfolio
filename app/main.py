import random

from flask import Flask, abort, redirect, render_template, url_for
from PIL import Image

from app.photo_loader import IMAGE_DIR, get_categories, get_images

app = Flask(__name__)

GALLERY_COVER_PATHS = (
    "Landscape/DSC07020.webp",
    "Travel/DSC09153.webp",
    "Nature/DSC09420.webp",
)


def add_image_ratios(images):
    collage_images = []
    for image in images:
        try:
            with Image.open(IMAGE_DIR / image["path"]) as photo:
                width, height = photo.size
        except (OSError, ValueError):
            width, height = 1, 1

        collage_image = image.copy()
        collage_image["aspect_ratio"] = width / max(height, 1)
        collage_images.append(collage_image)

    return collage_images


@app.route('/')
def profile():
    img_list = get_images()
    images_by_path = {image["path"]: image for image in img_list}
    covers = [images_by_path[path] for path in GALLERY_COVER_PATHS if path in images_by_path]
    if not covers:
        covers = img_list[:3]
    gallery_entry = {
        "covers": add_image_ratios(covers),
        "count": len(img_list),
    }
    return render_template('profile.html', gallery_entry=gallery_entry)


@app.route('/profile')
def legacy_profile():
    return redirect(url_for('profile'), code=301)


@app.route('/gallery/<category>')
def gallery(category):
    img_list = get_images()
    categories = get_categories(img_list)
    if category not in categories:
        abort(404)

    category_images = [image for image in img_list if image["category"] == category]
    random.shuffle(category_images)
    return render_template(
        'gallery.html',
        categories=categories,
        current_category=category,
        img_list=category_images,
    )


@app.route('/gallery')
def gallery_all():
    img_list = get_images()
    categories = get_categories(img_list)
    random.shuffle(img_list)
    return render_template(
        'gallery.html',
        categories=categories,
        current_category='All Photos',
        img_list=img_list,
    )


if __name__ == '__main__':
    app.run()
