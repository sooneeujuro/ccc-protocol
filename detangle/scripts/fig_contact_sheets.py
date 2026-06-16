#!/usr/bin/env python3
"""fig_contact_sheets.py — READ-ONLY: render a contact sheet per reconvert paper.

For each fig_refix_out\<slug>\ paper, render ONLY the images its fresh MD
references (in MD order = what would actually go live), as a labeled grid.
Tiny images (<120px any side, or <20k px area) get a RED label = cruft suspect.
Also emits FIG_REFIX_REFERENCED.json: per paper, referenced images with dims
and a referenced-AND-tiny list (the actionable cruft set).

Writes PNGs to detangle\_contact_sheets\ . Touches no corpus/live file.
"""
import json
import re
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REFIX = Path(r"G:\fig_refix_out")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\_contact_sheets")
OUT.mkdir(exist_ok=True)
JSON_OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\FIG_REFIX_REFERENCED.json")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")
IMG_EXT = (".jpg", ".jpeg", ".png")

THUMB = 200
PAD = 12
LABEL_H = 34
COLS = 5

try:
    FONT = ImageFont.truetype("arial.ttf", 13)
    FONT_B = ImageFont.truetype("arialbd.ttf", 14)
except Exception:
    FONT = ImageFont.load_default()
    FONT_B = FONT


def is_tiny(w, h):
    return w < 120 or h < 120 or (w * h) < 20000


def md_refs(text):
    out = []
    for m in IMG_RE.finditer(text):
        tgt = m.group(1).strip().split()[0] if m.group(1).strip() else ""
        if not tgt or tgt.startswith(("http://", "https://", "data:")):
            continue
        out.append(tgt.replace("\\", "/").rsplit("/", 1)[-1])
    return out


def main():
    report = {}
    for slug in sorted(p.name for p in REFIX.iterdir() if p.is_dir()):
        folder = REFIX / slug
        mds = list(folder.rglob("*.md"))
        if not mds:
            continue
        text = mds[0].read_text(encoding="utf-8", errors="replace")
        refs = md_refs(text)  # in-order, may repeat
        seen, ordered = set(), []
        for r in refs:
            if r not in seen:
                seen.add(r); ordered.append(r)
        by_name = {f.name: f for f in folder.rglob("*") if f.suffix.lower() in IMG_EXT}

        items = []
        for name in ordered:
            f = by_name.get(name)
            if not f:
                items.append(dict(name=name, missing=True)); continue
            try:
                with Image.open(f) as im:
                    w, h = im.size
            except Exception as e:
                items.append(dict(name=name, error=str(e))); continue
            items.append(dict(name=name, w=w, h=h, bytes=f.stat().st_size, tiny=is_tiny(w, h), path=str(f)))

        referenced_tiny = [i for i in items if i.get("tiny")]
        report[slug] = dict(
            md_name=mds[0].name,
            referenced=len(ordered),
            referenced_tiny=[dict(name=i["name"], w=i["w"], h=i["h"]) for i in referenced_tiny],
            items=[{k: v for k, v in i.items() if k != "path"} for i in items],
        )

        # render grid
        n = len(items)
        cols = min(COLS, max(1, n))
        rows = (n + cols - 1) // cols
        cellw = THUMB + PAD
        cellh = THUMB + PAD + LABEL_H
        head = 40
        W = cols * cellw + PAD
        H = head + rows * cellh + PAD
        canvas = Image.new("RGB", (W, H), (250, 250, 250))
        d = ImageDraw.Draw(canvas)
        title = f"{slug}   referenced={n}   tiny(cruft?)={len(referenced_tiny)}"
        d.text((PAD, 12), title, fill=(0, 0, 0), font=FONT_B)
        for idx, it in enumerate(items):
            r, c = divmod(idx, cols)
            x = PAD + c * cellw
            y = head + r * cellh
            box = (x, y, x + THUMB, y + THUMB)
            if it.get("missing") or it.get("error"):
                d.rectangle(box, outline=(200, 0, 0), width=2)
                d.text((x + 6, y + 6), "MISSING" if it.get("missing") else "ERR", fill=(200, 0, 0), font=FONT)
            else:
                try:
                    with Image.open(it["path"]) as im:
                        im = im.convert("RGB")
                        im.thumbnail((THUMB, THUMB))
                        ox = x + (THUMB - im.width) // 2
                        oy = y + (THUMB - im.height) // 2
                        canvas.paste(im, (ox, oy))
                except Exception:
                    pass
                outline = (200, 0, 0) if it.get("tiny") else (180, 180, 180)
                d.rectangle(box, outline=outline, width=3 if it.get("tiny") else 1)
            tail = it["name"].split("__")[-1][:14]
            dim = f'{it.get("w","?")}x{it.get("h","?")}'
            color = (200, 0, 0) if it.get("tiny") else (60, 60, 60)
            d.text((x + 2, y + THUMB + 4), f"#{idx+1} {dim}", fill=color, font=FONT)
            d.text((x + 2, y + THUMB + 18), tail, fill=(120, 120, 120), font=FONT)
        canvas.save(OUT / f"{slug}.png")
        print(f"{slug}: referenced={n} tiny={len(referenced_tiny)} -> {slug}.png")

    JSON_OUT.write_text(json.dumps(report, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\njson: {JSON_OUT}")
    print(f"sheets: {OUT}")


if __name__ == "__main__":
    main()
