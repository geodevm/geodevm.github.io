"""
Resize photos for the website's Photo Gallery.

Reads every .jpg, .jpeg and .png file in a folder and saves two smaller copies
into the website repository:
    images/gallery/full/    the full photo, at most 2000 pixels on the long side
    images/gallery/thumbs/  a small version for the grid, 600 pixels on the short side

Everything else in the folder (CR3, DNG, and any other file type) is ignored.
Your original photos are never changed.

The copies also drop the photos' hidden camera data (EXIF), which can include
the GPS location where a photo was taken.

How to run it (in the VSCode terminal, from the repository folder):
    py -m pip install pillow                          (first time only)
    py scripts/resize_photos.py "C:\\path\\to\\your\\photos"

At the end it prints lines you can paste into _data/gallery.yml.
"""

import argparse
import re
import sys
from pathlib import Path

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow isn't installed. Run:  py -m pip install pillow  and try again.")

ALLOWED = {".jpg", ".jpeg", ".png"}
FULL_LONG_EDGE = 2000
THUMB_SHORT_EDGE = 600
JPEG_QUALITY = 85

REPO = Path(__file__).resolve().parent.parent
DEFAULT_OUT = REPO / "images" / "gallery"


def web_name(path):
    """Make a file name that is safe in a web address: lowercase, no spaces."""
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") or "photo"
    ext = ".png" if path.suffix.lower() == ".png" else ".jpg"
    return stem + ext


def shrink(img, long_edge=None, short_edge=None):
    w, h = img.size
    if long_edge:
        scale = long_edge / max(w, h)
    else:
        scale = short_edge / min(w, h)
    if scale >= 1:
        return img.copy()
    return img.resize((round(w * scale), round(h * scale)), Image.LANCZOS)


def save(img, dest):
    if dest.suffix == ".png":
        img.save(dest, optimize=True)
    else:
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        img.save(dest, quality=JPEG_QUALITY, optimize=True, progressive=True)


def main():
    parser = argparse.ArgumentParser(description="Resize JPEG and PNG photos for the website gallery.")
    parser.add_argument("source", help="folder containing your photos")
    parser.add_argument("--out", default=str(DEFAULT_OUT),
                        help="where to put the resized copies (default: images/gallery in this repository)")
    parser.add_argument("--overwrite", action="store_true",
                        help="redo photos that were already resized")
    args = parser.parse_args()

    source = Path(args.source)
    if not source.is_dir():
        sys.exit(f"Can't find the folder: {source}")
    out = Path(args.out)
    (out / "full").mkdir(parents=True, exist_ok=True)
    (out / "thumbs").mkdir(parents=True, exist_ok=True)

    photos = sorted(p for p in source.iterdir() if p.is_file() and p.suffix.lower() in ALLOWED)
    skipped = sorted(p.name for p in source.iterdir() if p.is_file() and p.suffix.lower() not in ALLOWED)

    if not photos:
        sys.exit("No .jpg, .jpeg or .png files found in that folder.")

    done, existing, failed, used = [], [], [], set()
    for p in photos:
        name = web_name(p)
        if name in used:
            print(f"  ! Skipping {p.name}: another photo already uses the web name {name}. Rename one of them.")
            failed.append(p.name)
            continue
        used.add(name)

        full_path, thumb_path = out / "full" / name, out / "thumbs" / name
        if full_path.exists() and thumb_path.exists() and not args.overwrite:
            existing.append(name)
            continue
        try:
            with Image.open(p) as img:
                img = ImageOps.exif_transpose(img)
                save(shrink(img, long_edge=FULL_LONG_EDGE), full_path)
                save(shrink(img, short_edge=THUMB_SHORT_EDGE), thumb_path)
        except Exception as err:
            print(f"  ! Couldn't process {p.name}: {err}")
            failed.append(p.name)
            continue
        done.append(name)
        print(f"  resized {p.name}  ->  {name}")

    print()
    print(f"Resized {len(done)} photo(s).")
    if existing:
        print(f"Already done, left alone: {len(existing)} (use --overwrite to redo them).")
    if skipped:
        print(f"Ignored {len(skipped)} other file(s), e.g. CR3/DNG. Not touched.")
    if failed:
        print(f"Problems with {len(failed)} file(s), listed above.")

    if done:
        print()
        print("Paste these into _data/gallery.yml and fill in the captions and descriptions:")
        print()
        for name in done:
            print(f"- file: {name}")
            print(f"  caption: \"\"")
            print(f"  alt: \"\"")
            print()


if __name__ == "__main__":
    main()
