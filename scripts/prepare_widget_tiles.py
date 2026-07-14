#!/usr/bin/env python3
"""Create website-only WealthX widget tiles from approved simulator captures.

The source screenshots remain read-only.  Each output is a deterministic crop
of a real widget surface, downsampled for web delivery without AI rendering.
"""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


SOURCE_SIZE = (1320, 2868)
TILES = {
    "widgets-home": ("home-screen.png", (84, 282, 1236, 1598)),
    "widgets-today": ("today-view.png", (84, 256, 1236, 2160)),
}
SOURCE_GROUPS = {
    "en-US": "TipShot_Widgets_en",
    "zh-Hans": "TipShot_Widgets_zhHans",
}


def build_tiles(source_root: Path, output_root: Path) -> None:
    output_root.mkdir(parents=True, exist_ok=True)
    for locale, source_group in SOURCE_GROUPS.items():
        for theme in ("light", "dark"):
            source_dir = source_root / locale / theme / source_group
            for topic, (filename, crop) in TILES.items():
                source = source_dir / filename
                if not source.exists():
                    raise FileNotFoundError(source)
                with Image.open(source) as image:
                    if image.size != SOURCE_SIZE:
                        raise ValueError(f"Unexpected source size for {source}: {image.size}")
                    tile = image.crop(crop).convert("RGB")
                    tile.thumbnail((960, 1600), Image.Resampling.LANCZOS)
                    output = output_root / f"{topic}.{locale}.{theme}.webp"
                    tile.save(output, "WEBP", lossless=True, method=6)
                    print(f"{output.name}: {tile.size[0]}x{tile.size[1]}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source-root", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    args = parser.parse_args()
    build_tiles(args.source_root, args.output_root)


if __name__ == "__main__":
    main()
