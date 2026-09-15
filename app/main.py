import random

from flask import Flask, abort, redirect, render_template, url_for
from PIL import Image

from app.photo_loader import IMAGE_DIR, get_categories, get_images

app = Flask(__name__)

PROJECTS = {
    "course-schedule-pilot": {
        "title": "Course Schedule Pilot",
        "eyebrow": "AI course planning",
        "summary": "A conversational course-planning assistant that generates, ranks, and visualizes conflict-free weekly schedules around each student's preferences.",
        "description": "Course Schedule Pilot turns course choices and personal scheduling preferences into practical weekly plans. It combines a conversational interface with schedule generation and ranking so students can compare options without manually resolving every conflict.",
        "highlights": ["Generates conflict-free weekly schedules", "Ranks options around student preferences", "Presents schedules in an interactive visual interface"],
        "technologies": ["React", "TypeScript", "FastAPI", "Python", "OpenAI"],
        "live_url": "https://courseschedulepilot.vercel.app",
        "github_url": "https://github.com/yuzew0924/Calendar_Agent",
        "visual_class": "visual-calendar",
        "icon": "fa-regular fa-calendar-check",
    },
    "uw-major-advisor": {
        "title": "UW Major Advisor",
        "eyebrow": "Retrieval-augmented advising",
        "summary": "A citation-grounded RAG assistant for questions about admissions and requirements across University of Washington majors.",
        "description": "UW Major Advisor makes complex admissions information easier to navigate. It retrieves relevant source material, builds a grounded response, and provides citations so students can verify the guidance against university information.",
        "highlights": ["Answers questions across seven UW majors", "Uses retrieval to ground responses", "Includes citations for source verification"],
        "technologies": ["RAG", "FAISS", "Python", "OpenAI", "Streamlit"],
        "live_url": "https://uw-major-advisor.streamlit.app/",
        "github_url": "https://github.com/yuzew0924/uw-major-advisor",
        "visual_class": "visual-uw",
        "mark": "W",
    },
    "lunar-phase-classification": {
        "title": "Lunar Phase Classification",
        "eyebrow": "Computer vision study",
        "summary": "An image-classification study comparing a custom CNN with ResNet-18 transfer learning across seven lunar phases.",
        "description": "This project explores how convolutional neural networks distinguish visually similar lunar phases. It compares a custom architecture with transfer learning and evaluates performance across a seven-class image dataset.",
        "highlights": ["Seven-class lunar phase dataset", "Custom CNN and ResNet-18 comparison", "Model evaluation and error analysis"],
        "technologies": ["PyTorch", "ResNet-18", "CNN", "Computer Vision"],
        "github_url": "https://github.com/yuzew0924/lunar-phase-classification",
        "visual_class": "visual-moon",
        "icon": "fa-solid fa-moon",
    },
    "heart-disease-analysis": {
        "title": "Heart Disease Analysis",
        "eyebrow": "Applied machine learning",
        "summary": "An exploratory analysis and model comparison using clinical variables to study and predict heart-disease outcomes.",
        "description": "This analysis examines relationships between clinical variables and heart-disease outcomes, then compares machine-learning approaches to understand their predictive behavior and tradeoffs.",
        "highlights": ["Exploratory analysis of clinical variables", "Comparison of multiple predictive models", "Clear evaluation of model performance"],
        "technologies": ["Python", "scikit-learn", "EDA", "Jupyter"],
        "github_url": "https://github.com/yuzew0924/heart-disease-analysis",
        "visual_class": "visual-heart",
        "icon": "fa-solid fa-heart-pulse",
    },
}

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


def get_landscape_images(images, min_ratio=1.4):
    landscape_images = []
    for image in images:
        try:
            with Image.open(IMAGE_DIR / image["path"]) as photo:
                width, height = photo.size
        except (OSError, ValueError):
            continue

        if width / max(height, 1) >= min_ratio:
            landscape_images.append(image)

    return landscape_images


@app.route('/')
def profile():
    img_list = get_images()
    covers = random.sample(img_list, min(3, len(img_list)))
    landscape_images = get_landscape_images(img_list)
    hero_image = random.choice(landscape_images or img_list) if img_list else None
    gallery_entry = {
        "covers": add_image_ratios(covers),
        "count": len(img_list),
    }
    return render_template(
        'profile.html',
        gallery_entry=gallery_entry,
        hero_image=hero_image,
    )


@app.route('/profile')
def legacy_profile():
    return redirect(url_for('profile'), code=301)


@app.route('/projects/<slug>')
def project_detail(slug):
    project = PROJECTS.get(slug)
    if project is None:
        abort(404)
    return render_template('project.html', project=project)


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
