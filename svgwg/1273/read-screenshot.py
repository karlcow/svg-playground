# Reads the live <img> column of probe-fragment-sizing.html from a screenshot.
# Usage: python3 -I read-screenshot.py <screenshot.png>
# Converts the PNG to BMP with sips (macOS), finds each grid thumbnail, and
# decodes the cell under the four corner samples (12% and 88%), the same points
# the probe samples on the canvas. Prints one line per thumbnail, top to bottom.
# Cell (i,j) is rgb(30+50i, 30+50j, 160); see make-svgs.py.
import struct, subprocess, sys, tempfile, os

REGIONS = {
    '0,0 3,0 0,3 3,3': 'full', '0,0 1,0 0,1 1,1': 'tl-quarter', '2,2 3,2 2,3 3,3': 'br-quarter',
    '1,1 1,1 1,1 1,1': 'cell-1-1', '0,0 0,0 0,0 0,0': 'cell-0-0', '0,0 2,0 0,2 2,2': 'tl-3x3',
    '1,1 2,1 1,2 2,2': 'mid-2x2', '1,1 4,1 1,4 4,4': 'e-full',
}

def load(png):
    bmp = os.path.join(tempfile.mkdtemp(), 'shot.bmp')
    subprocess.run(['sips', '-s', 'format', 'bmp', png, '--out', bmp], check=True, capture_output=True)
    d = open(bmp, 'rb').read()
    off = struct.unpack_from('<I', d, 10)[0]
    w, h = struct.unpack_from('<ii', d, 18)
    bp = struct.unpack_from('<H', d, 28)[0] // 8
    stride = (w * bp + 3) & ~3
    flip = h > 0
    h = abs(h)
    def px(x, y):
        yy = (h - 1 - y) if flip else y
        i = off + yy * stride + x * bp
        return d[i + 2], d[i + 1], d[i]
    return w, h, px

def cell(c):
    r, g, b = c
    i, j = round((r - 30) / 50), round((g - 30) / 50)
    if not (0 <= i <= 4 and 0 <= j <= 4):
        return None
    if abs(r - (30 + 50 * i)) > 12 or abs(g - (30 + 50 * j)) > 12 or abs(b - 160) > 12:
        return None
    return f'{i},{j}'

def runs_at(px, h, x, gap=8, lo=60, hi=100):
    """Vertical runs of grid pixels at column x, bridging gaps up to `gap`
    pixels (cell labels), kept when lo <= height <= hi (the 80px thumbnails
    of the region table, not the 200px images of the ratio table)."""
    out, top, last = [], None, None
    for y in range(h):
        if cell(px(x, y)):
            if top is None:
                top = y
            last = y
        elif top is not None and y - last > gap:
            if lo <= last + 1 - top <= hi:
                out.append((top, last + 1))
            top = None
    if top is not None and lo <= last + 1 - top <= hi:
        out.append((top, last + 1))
    return out

def main(png):
    w, h, px = load(png)
    # The thumbnail column: the x with the most 60-100px runs.
    best_x = max(range(0, w, 2), key=lambda x: len(runs_at(px, h, x)))
    for top, bot in runs_at(px, h, best_x):
        side = bot - top
        # Left edge: walk left from best_x along a row, bridging label gaps.
        ym = top + side // 2
        x0, miss = best_x, 0
        while x0 > 0 and miss <= 8:
            x0 -= 1
            miss = 0 if cell(px(x0, ym)) else miss + 1
        x0 += miss
        x1 = x0 + side - 1  # thumbnails are square
        pts = [(.12, .12), (.88, .12), (.12, .88), (.88, .88)]
        cells = ' '.join(cell(px(x0 + int((x1 - x0) * fx), top + int(side * fy))) or '?' for fx, fy in pts)
        print(f'y={top:5d} x={x0} size={side}  {cells:20s} {REGIONS.get(cells, "other")}')

if __name__ == '__main__':
    main(sys.argv[1])
