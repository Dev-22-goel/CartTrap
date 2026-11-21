"""One labelled grid image of a golden set, small enough for Discord (< 8 MB).

    uv run python scripts/make_contact_sheet.py --set holdout2
    -> eval/golden/holdout2_contact_sheet.jpg

Each tile is labelled with the case id and ATTACK or BENIGN. Reads eval/golden/manifest.json.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
GOLDEN = ROOT / "eval" / "golden"
MAX_BYTES = 8 * 1024 * 1024


def _font(size: int):
    for name in ("arialbd.ttf", "DejaVuSans-Bold.ttf", "Arial Bold.ttf"):
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            continue
    return ImageFont.load_default()


def group_of(c: dict) -> str:
    return "holdout2" if c.get("holdout2") else "holdout" if c.get("holdout") else "golden"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--set", default="holdout2", choices=["golden", "holdout", "holdout2"])
    ap.add_argument("--cols", type=int, default=5)
    ap.add_argument("--tile", type=int, default=640, help="tile width in px")
    args = ap.parse_args()

    cases = [c for c in json.loads((GOLDEN / "manifest.json").read_text(encoding="utf-8"))["cases"]
             if group_of(c) == args.set]
    if not cases:
        sys.exit(f"no {args.set} cases in the manifest")
    tw, th, label_h, pad = args.tile, int(args.tile * 0.75), 64, 12
    cols = args.cols
    rows = (len(cases) + cols - 1) // cols
    title_h = 70
    W = cols * tw + (cols + 1) * pad
    H = title_h + rows * (th + label_h) + (rows + 1) * pad
    sheet = Image.new("RGB", (W, H), (24, 24, 28))
    d = ImageDraw.Draw(sheet)
    f_title, f_id, f_tag = _font(36), _font(24), _font(22)
    n_atk = sum(c["label"] == "attack" for c in cases)
    d.text((pad, 16), f"CartTrap {args.set}: {len(cases)} cases ({n_atk} attacks, {len(cases) - n_atk} benign) - "
                      f"not scored until after Task 15", fill=(235, 235, 235), font=f_title)

    for i, c in enumerate(cases):
        r, k = divmod(i, cols)
        x = pad + k * (tw + pad)
        y = title_h + pad + r * (th + label_h + pad)
        with Image.open(GOLDEN / c["file"]) as im:
            im = im.convert("RGB")
            im.thumbnail((tw, th), Image.LANCZOS)
            sheet.paste(im, (x + (tw - im.width) // 2, y + (th - im.height) // 2))
        attack = c["label"] == "attack"
        tag, color = ("ATTACK", (214, 48, 49)) if attack else ("BENIGN", (39, 174, 96))
        ly = y + th
        d.rectangle([x, ly, x + tw, ly + label_h], fill=(40, 40, 46))
        tag_w = d.textlength(tag, font=f_tag) + 20
        d.rectangle([x + 8, ly + 16, x + 8 + tag_w, ly + label_h - 16], fill=color)
        d.text((x + 18, ly + 19), tag, fill="white", font=f_tag)
        d.text((x + tag_w + 20, ly + 18), c["id"], fill=(240, 240, 240), font=f_id)

    out = GOLDEN / f"{args.set}_contact_sheet.jpg"
    for q in (88, 80, 70, 60):
        sheet.save(out, format="JPEG", quality=q, optimize=True)
        if out.stat().st_size < MAX_BYTES:
            break
    print(f"wrote {out.relative_to(ROOT)}  {sheet.width}x{sheet.height}  {out.stat().st_size / 1e6:.2f} MB (q={q})")


if __name__ == "__main__":
    main()
