"""One-off script to render the RouteWise mark (a routing/fork glyph: one
node branching into several) as a PNG favicon. Run manually when the mark
changes; the output is committed as a static asset.
"""
from PIL import Image, ImageDraw

SIZE = 256
img = Image.new("RGBA", (SIZE, SIZE), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

bg_color = (14, 17, 23, 255)  # matches app background
draw.rounded_rectangle([0, 0, SIZE, SIZE], radius=56, fill=bg_color)

# Scale factor from the 24x24 design grid to SIZE.
s = SIZE / 24

def line(p1, p2, width, color):
    draw.line([tuple(c * s for c in p1), tuple(c * s for c in p2)], fill=color, width=int(width * s))

def dot(center, r, color):
    x, y = center
    draw.ellipse([(x - r) * s, (y - r) * s, (x + r) * s, (y + r) * s], fill=color)

STROKE = (140, 130, 210, 255)
C1, C2, C3 = (167, 139, 250, 255), (96, 230, 216, 255), (92, 200, 252, 255)

line((12, 20), (12, 14), 2.4, STROKE)
line((12, 14), (5, 6), 2.2, STROKE)
line((12, 14), (12, 5), 2.2, STROKE)
line((12, 14), (19, 6), 2.2, STROKE)

dot((12, 20), 2.6, (200, 190, 250, 255))
dot((12, 14), 1.7, (200, 190, 250, 255))
dot((5, 6), 2.3, C1)
dot((12, 5), 2.3, C2)
dot((19, 6), 2.3, C3)

img.save("webapp/favicon.png")
print("saved webapp/favicon.png")
