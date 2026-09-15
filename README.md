# Yuze Portfolio

A small Flask photo gallery.

## Optimize Photos

Keep original full-size photos outside the website image folder:

```text
photos-original/
```

Use the same category folders there:

```text
photos-original/City/
photos-original/Landscape/
photos-original/Travel/
```

Then generate web-ready images:

```bash
python3 scripts/optimize_images.py
```

The script writes compressed `.webp` files to `app/static/images/` and keeps the same category folder structure. By default, images are resized to a maximum width of `2000px` with WebP quality `82`.

To rebuild everything:

```bash
python3 scripts/optimize_images.py --force
```

HEIC files are skipped by the optimizer because standard Pillow installs usually cannot read them reliably. Convert HEIC photos to JPG or WebP before optimizing.

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

## Publish New Photos

Keep originals in `photos-original/`, using the same category folders as the
website. To convert only new or changed photos, commit the generated WebP files,
and push them to `main`, run:

```bash
.venv/bin/python scripts/publish_photos.py
```

You can provide a custom commit message:

```bash
.venv/bin/python scripts/publish_photos.py --message "Add spring photos"
```

Use `--force` only when every optimized image needs to be rebuilt. Original
photos remain local and ignored by Git; only files under `app/static/images/`
are published.
