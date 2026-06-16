#!/usr/bin/env python3
"""fig_verify_sheet.py <slug> — 머지 후 LIVE articles 검증용 콘택트시트.

articles\<slug>__*.jpg 를 실제로 읽어 그리드 렌더. 머지가 live에 제대로
들어갔는지 눈으로 확인. READ-ONLY.
"""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ART = Path(r"G:\corpus_md_export_20260612\articles")
OUT = Path(r"C:\Users\USER\Documents\ccc-protocol\detangle\_contact_sheets")
OUT.mkdir(exist_ok=True)
slug = sys.argv[1]
imgs = sorted(ART.glob(f"{slug}__*.jpg"))
THUMB, PAD, LABEL_H, COLS = 180, 10, 22, 6
try:
    FONT = ImageFont.truetype("arial.ttf", 12)
    FONT_B = ImageFont.truetype("arialbd.ttf", 15)
except Exception:
    FONT = FONT_B = ImageFont.load_default()

n = len(imgs)
cols = min(COLS, max(1, n))
rows = (n + cols - 1) // cols
cellw, cellh, head = THUMB + PAD, THUMB + PAD + LABEL_H, 36
W, H = cols * cellw + PAD, head + rows * cellh + PAD
canvas = Image.new("RGB", (W, H), (245, 250, 245))
d = ImageDraw.Draw(canvas)
d.text((PAD, 10), f"LIVE articles\\{slug}__*  ({n} imgs)", fill=(0, 100, 0), font=FONT_B)
for i, f in enumerate(imgs):
    r, c = divmod(i, cols)
    x, y = PAD + c * cellw, head + r * cellh
    dim = "?"
    try:
        with Image.open(f) as im:
            w, h = im.size; dim = f"{w}x{h}"
            im = im.convert("RGB"); im.thumbnail((THUMB, THUMB))
            canvas.paste(im, (x + (THUMB - im.width) // 2, y + (THUMB - im.height) // 2))
    except Exception:
        d.text((x + 6, y + 6), "ERR", fill=(200, 0, 0), font=FONT)
    d.rectangle((x, y, x + THUMB, y + THUMB), outline=(180, 180, 180), width=1)
    d.text((x + 2, y + THUMB + 3), f"#{i+1} {dim}", fill=(60, 60, 60), font=FONT)
out = OUT / f"_LIVE_{slug}.png"
canvas.save(out)
print(f"{slug}: {n} imgs -> {out}")
