#!/usr/bin/env python3
"""Feather the lower edge of already-transparent website device derivatives.

Craftshot source captures are immutable and several intentionally end at the
bottom of their source canvas. This utility affects only the website WebP
derivatives: it preserves every pixel above the requested fade region and
smoothly takes the existing alpha to zero before the canvas edge.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import numpy as np
from PIL import Image


def finish(path: Path, start: float, end: float) -> None:
    image = Image.open(path).convert("RGBA")
    pixels = np.asarray(image).copy()
    height = image.height
    start_row = round(height * start)
    end_row = round(height * end)
    if not 0 <= start_row < end_row <= height:
        raise ValueError(f"invalid fade for {path}: {start} to {end}")

    alpha = pixels[:, :, 3].astype(np.float32)
    progress = np.ones(height, dtype=np.float32)
    progress[start_row:end_row] = np.linspace(1, 0, end_row - start_row, endpoint=False)
    progress[end_row:] = 0
    pixels[:, :, 3] = np.rint(alpha * progress[:, None]).astype(np.uint8)
    pixels[pixels[:, :, 3] == 0, :3] = 0

    Image.fromarray(pixels, mode="RGBA").save(
        path,
        "WEBP",
        lossless=True,
        method=6,
        exact=True,
    )
    print(f"{path}: alpha fade {start:.0%}–{end:.0%}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("directory", type=Path)
    parser.add_argument("--start", type=float, default=0.78)
    parser.add_argument("--end", type=float, default=0.97)
    args = parser.parse_args()
    paths = sorted(args.directory.glob("*.webp"))
    if not paths:
        parser.error("no WebP files found")
    for path in paths:
        finish(path, args.start, args.end)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
