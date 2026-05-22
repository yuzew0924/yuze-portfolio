import random

from flask import Flask, render_template

from app.photo_loader import get_categories, get_images

app = Flask(__name__)


@app.route('/')
def main():
    img_list = get_images()
    categories = get_categories(img_list)
    random.shuffle(img_list)
    return render_template('gallery.html', categories=categories, img_list=img_list)


@app.route('/profile')
def profile():
    img_list = get_images()
    categories = get_categories(img_list)
    return render_template('profile.html', categories=categories)


if __name__ == '__main__':
    app.run()
