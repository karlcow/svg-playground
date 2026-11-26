# Writes the SVG test images for probe-fragment-sizing.html.
# Each cell (col i, row j) is 100 user units, filled rgb(30+50i, 30+50j, 160),
# with a small "i,j" label in the top-middle band of the cell (y 2..25), away
# from the diagonals where the probe samples.
import sys, os
out = sys.argv[1]
def grid(cols, rows):
    s = []
    for j in range(rows):
        for i in range(cols):
            s.append(f'  <rect x="{i*100}" y="{j*100}" width="100" height="100" fill="rgb({30+50*i},{30+50*j},160)"/>')
            s.append(f'  <text x="{i*100+50}" y="{j*100+20}" font-family="sans-serif" font-size="18" text-anchor="middle">{i},{j}</text>')
    return "\n".join(s)
files = {
  "sz-d-400-vb400.svg": ('width="400" height="400" viewBox="0 0 400 400"', 4, 4, '  <view id="q" viewBox="200 200 200 200"/>\n'),
  "sz-a-200-vb400.svg": ('width="200" height="200" viewBox="0 0 400 400"', 4, 4, ''),
  "sz-e-400-vb100.svg": ('width="400" height="400" viewBox="100 100 400 400"', 5, 5, ''),
  "sz-b-vbonly-400.svg": ('viewBox="0 0 400 400"', 4, 4, ''),
  "sz-c-vbonly-400x200.svg": ('viewBox="0 0 400 200"', 4, 2, '  <view id="sq" viewBox="0 0 200 200"/>\n'),
}
for name, (attrs, c, r, extra) in files.items():
    with open(os.path.join(out, name), "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" {attrs}>\n{extra}{grid(c, r)}\n</svg>\n')
    print(name)
