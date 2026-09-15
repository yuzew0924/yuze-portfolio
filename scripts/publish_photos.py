#!/usr/bin/env python3
"""Optimize local originals, commit generated gallery files, and push main."""

import argparse
import subprocess
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
PHOTO_OUTPUT = "app/static/images"


def run(*args, capture=False):
    result = subprocess.run(
        args,
        cwd=PROJECT_ROOT,
        check=False,
        text=True,
        capture_output=capture,
    )
    if result.returncode:
        if capture:
            print(result.stdout, end="")
            print(result.stderr, end="", file=sys.stderr)
        raise SystemExit(result.returncode)
    return result.stdout.strip() if capture else ""


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert new originals, commit generated photos, and push main."
    )
    parser.add_argument(
        "--message",
        default="Update gallery photos",
        help="Git commit message. Defaults to 'Update gallery photos'.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Rebuild every optimized photo before publishing.",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    branch = run("git", "branch", "--show-current", capture=True)
    if branch != "main":
        print(f"Refusing to publish from '{branch}'. Switch to main first.")
        return 1

    staged_before = run("git", "diff", "--cached", "--name-only", capture=True)
    unrelated_staged = [
        path for path in staged_before.splitlines() if not path.startswith(f"{PHOTO_OUTPUT}/")
    ]
    if unrelated_staged:
        print("Refusing to include unrelated staged files:")
        for path in unrelated_staged:
            print(f"  {path}")
        print("Commit or unstage them, then run this command again.")
        return 1

    optimize_command = [sys.executable, "scripts/optimize_images.py"]
    if args.force:
        optimize_command.append("--force")
    run(*optimize_command)

    run("git", "add", "-A", "--", PHOTO_OUTPUT)
    staged_photos = run(
        "git", "diff", "--cached", "--name-only", "--", PHOTO_OUTPUT, capture=True
    )
    if not staged_photos:
        print("No new or changed gallery photos to publish.")
        return 0

    print("Publishing:")
    for path in staged_photos.splitlines():
        print(f"  {path}")

    run("git", "commit", "-m", args.message, "--", PHOTO_OUTPUT)
    run("git", "push", "origin", "main")
    print("Gallery photos published to main.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
