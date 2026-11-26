# Builds figure-xywh-units.html: one inline SVG, two rows, three panels each.
import sys
out = sys.argv[1]
def grid(n=4):
    s = []
    for j in range(n):
        for i in range(n):
            s.append(f'<rect x="{i*100}" y="{j*100}" width="100" height="100" fill="rgb({30+50*i},{30+50*j},160)"/>')
            s.append(f'<text x="{i*100+50}" y="{j*100+62}" font-size="34" text-anchor="middle" fill="white" font-family="-apple-system, sans-serif">{i},{j}</text>')
    return "\n".join(s)
G = grid()
P = 200  # panel size in figure pixels

def panel(x, y, vb, title, sub, overlays=""):
    return f'''
  <g transform="translate({x},{y})">
    <text x="{P/2}" y="-30" font-size="15" font-weight="600" text-anchor="middle">{title}</text>
    <text x="{P/2}" y="-12" font-size="13" text-anchor="middle" fill="#444">{sub}</text>
    <svg width="{P}" height="{P}" viewBox="{vb}">{G}</svg>
    <rect width="{P}" height="{P}" fill="none" stroke="#999"/>
    {overlays}
  </g>'''

def row(y, frag, mf_vb, mf_box, br_vb, br_box, steps):
    # panel 1: the whole image, with the two selections drawn on it
    # boxes are in panel pixels: the image is 200x200 CSS px, drawn 1:1 here
    over = (f'<rect x="{mf_box[0]}" y="{mf_box[1]}" width="{mf_box[2]}" height="{mf_box[3]}" fill="none" stroke="#e8a000" stroke-width="5" stroke-dasharray="10 6"/>'
            f'<rect x="{br_box[0]}" y="{br_box[1]}" width="{br_box[2]}" height="{br_box[3]}" fill="none" stroke="#ff2a6d" stroke-width="5"/>')
    s = f'<text x="20" y="{y-62}" font-size="17" font-weight="700" font-family="ui-monospace, Menlo, monospace">#{frag}</text>'
    s += panel(20, y, "0 0 400 400", "The image", 'width="200" viewBox="0 0 400 400"', over)
    s += panel(270, y, mf_vb, "Image pixels", "Media Fragments", f'<rect width="{P}" height="{P}" fill="none" stroke="#e8a000" stroke-width="5" stroke-dasharray="10 6"/>')
    s += panel(520, y, br_vb, "What browsers show", "Firefox, Chrome, WebKit", f'<rect width="{P}" height="{P}" fill="none" stroke="#ff2a6d" stroke-width="5"/>')
    for k, line in enumerate(steps):
        s += f'<text x="770" y="{y+30+k*24}" font-size="14" font-family="-apple-system, sans-serif">{line}</text>'
    return s

body = ""
body += row(110, "xywh=percent:0,0,100,100",
            "0 0 400 400", (0, 0, 200, 200),
            "0 0 200 200", (0, 0, 100, 100),
            ["100% of the image width (200 px) = 200",
             "→ viewBox 0 0 200 200",
             "but the drawing is 400 units wide,",
             "so 200 units is half of it:",
             "a quarter of the image is shown."])
body += row(430, "xywh=100,100,100,100",
            "200 200 200 200", (100, 100, 100, 100),
            "100 100 100 100", (50, 50, 50, 50),
            ["checked against the image: 100+100 ≤ 200 px, fits",
             "→ viewBox 100 100 100 100",
             "but 1 image pixel is 2 drawing units,",
             "so the region is half as big",
             "and in the wrong place."])
legend = ('<g transform="translate(20,690)" font-size="14" font-family="-apple-system, sans-serif">'
          '<rect width="30" height="14" fill="none" stroke="#e8a000" stroke-width="4" stroke-dasharray="8 5"/><text x="40" y="12">region in image pixels (Media Fragments)</text>'
          '<rect x="360" width="30" height="14" fill="none" stroke="#ff2a6d" stroke-width="4"/><text x="400" y="12">region browsers select (numbers used as viewBox units)</text></g>')
html = f'''<!DOCTYPE html><meta charset="utf-8"><title>xywh units figure</title>
<style>body{{margin:0;background:white}}</style>
<svg id="fig" xmlns="http://www.w3.org/2000/svg" width="1130" height="720" font-family="-apple-system, sans-serif">
<rect width="1130" height="720" fill="white"/>
{body}
{legend}
</svg>'''
open(out, "w").write(html)
