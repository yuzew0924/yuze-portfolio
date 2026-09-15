# Yuze Portfolio

A small Flask photo gallery.

## Optimize Photos

Keep original full-size photos outside the website image folder:

```text
photos-original/
```

Use one of the current category folders:

```text
photos-original/Aviation/
photos-original/Culture/
photos-original/Landscapes/
photos-original/Nature/
photos-original/Night/
photos-original/People/
photos-original/Pets/
photos-original/Urban/
```

The website presents several folders with longer display names:

- `Culture` → Culture & Landmarks
- `Nature` → Nature & Wildlife
- `Night` → Night Sky
- `Urban` → Urban & Architecture

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

Add original `.jpg`, `.jpeg`, `.png`, or `.webp` files to the matching folder
under `photos-original/`. Do not manually copy originals into
`app/static/images/`; that folder contains generated website assets.

The gallery scans generated files when each page loads, so new categories are
created automatically from folder names. If you add a new short folder name
that needs a longer display label, also update `CATEGORY_LABELS` in
`app/main.py`.

HEIC files are not published because the current Pillow setup cannot reliably
decode them. Convert HEIC photos to JPG or WebP before publishing.

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
