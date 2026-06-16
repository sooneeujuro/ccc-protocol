#!/usr/bin/env python3
"""fig_drop_sheet.py — READ-ONLY: render ALL cruft-drop candidates on one sheet.

Reads FIG_CRUFT_DROPLIST.json, lays out every to-be-dropped image (across the
10 papers) in a single labeled grid so the operator can eyeball the whole
deletion set at once. Touches no corpus/live file.
"""
import json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

REFIX = Path(r"G:\fig_refix_out")
DROP = json.loads(Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\FIG_CRUFT_DROPLIST.json").read_text(encoding="utf-8"))
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\_contact_sheets\_DROP_ALL.png")

THUMB = 150
PAD = 10
LABEL_H = 40
COLS = 9
try:
    FONT = ImageFont.truetype("arial.ttf", 12)
    FONT_B = ImageFont.truetype("arialbd.ttf", 16)
except Exception:
    FONT = FONT_B = ImageFont.load_default()

items = []
for slug, names in DROP.items():
    for n in names:
        f = REFIX / slug / n
        items.append((slug, n, f))

n = len(items)
cols = COLS
rows = (n + cols - 1) // cols
cellw = THUMB + PAD
cellh = THUMB + PAD + LABEL_H
head = 44
W = cols * cellw + PAD
H = head + rows * cellh + PAD
canvas = Image.new("RGB", (W, H), (255, 245, 245))
d = ImageDraw.Draw(canvas)
d.text((PAD, 12), f"CRUFT DROP CANDIDATES — {n} images across 10 papers (ALL to be removed)", fill=(150, 0, 0), font=FONT_B)

for idx, (slug, name, f) in enumerate(items):
    r, c = divmod(idx, cols)
    x = PAD + c * cellw
    y = head + r * cellh
    box = (x, y, x + THUMB, y + THUMB)
    dim = "?"
    try:
        with Image.open(f) as im:
            w, h = im.size
            dim = f"{w}x{h}"
            im = im.convert("RGB")
            im.thumbnail((THUMB, THUMB))
            canvas.paste(im, (x + (THUMB - im.width) // 2, y + (THUMB - im.height) // 2))
    except Exception:
        d.text((x + 6, y + 6), "ERR", fill=(200, 0, 0), font=FONT)
    d.rectangle(box, outline=(200, 0, 0), width=2)
    d.text((x + 2, y + THUMB + 3), f"{slug[:8]} {dim}", fill=(150, 0, 0), font=FONT)
    d.text((x + 2, y + THUMB + 19), name.split("__")[-1][:13], fill=(120, 120, 120), font=FONT)

canvas.save(OUT)
print(f"dropped imgs: {n} -> {OUT}")
