# Yuze Portfolio

A small Flask photo gallery.

## Add Photos

Put new web-ready images in:

```text
app/static/images/
```

Supported formats are `.jpg`, `.jpeg`, `.png`, `.webp`, and `.gif`. The gallery scans this folder when the home page loads, so no Excel update is needed.

To add photo types, create folders inside `app/static/images/`:

```text
app/static/images/landscape/
app/static/images/portrait/
app/static/images/street/
```

Photos in these folders are automatically added to the `Types` dropdown. Photos directly inside `app/static/images/` are shown as `Uncategorized`.

HEIC files are not included because many browsers cannot display them reliably. Convert HEIC photos to JPG or WebP before adding them.
