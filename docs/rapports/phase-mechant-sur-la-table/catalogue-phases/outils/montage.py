import sys
from PIL import Image, ImageDraw
names = sys.argv[2:]
out = sys.argv[1]
cols = 2
W, H = 640, 360
rows = (len(names) + cols - 1) // cols
sheet = Image.new('RGB', (cols * W, rows * H), (20, 20, 20))
for i, n in enumerate(names):
    try:
        im = Image.open(f'out/{n}.png').convert('RGB')
    except Exception as e:
        continue
    im.thumbnail((W, H))
    x, y = (i % cols) * W, (i // cols) * H
    sheet.paste(im, (x, y))
    d = ImageDraw.Draw(sheet); d.rectangle([x, y, x + 8 * len(n) + 6, y + 14], fill=(0, 0, 0)); d.text((x + 3, y + 1), n, fill=(255, 255, 0))
sheet.save(out)
