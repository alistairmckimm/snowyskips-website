from PIL import Image, ImageFilter, ImageDraw, ImageEnhance, ImageFont

F = '/usr/share/fonts/opentype/inter/'
XB = lambda s: ImageFont.truetype(F + 'Inter-ExtraBold.otf', s)
BD = lambda s: ImageFont.truetype(F + 'Inter-Bold.otf', s)
SB = lambda s: ImageFont.truetype(F + 'Inter-SemiBold.otf', s)
BROWN, GREEN, OFF = (82, 55, 42), (79, 114, 48), (245, 242, 236)
RATE = {'G': (270, 'general waste'), 'C': (320, 'building & demolition'), 'K': (99, 'concrete & bricks'), 'R': (95, 'green waste')}
OW, OH = 1000, 750

LG = '/home/claude/lg/'
PF = '/home/claude/photos/full/'
# key, source file, crop (x0,y0,w,h in source px), focus centre (fx,fy as 0-1), bin, label, tonnes, rate
JOBS = [
 ('mck074', LG+'33.jpg', (0,150,675,506), (.45,.55), '1 m³', 'Household rubbish', 0.10, 'G'),
 ('mck053', LG+'16.jpg', (0,180,675,506), (.5,.55), '2 m³', 'Cardboard & packaging', 0.16, 'C'),
 ('mck068', PF+'MCK-068.jpg', (0,280,750,562), (.5,.5), '2 m³', 'Household clean-out', 0.24, 'G'),
 ('mck072', LG+'31.jpg', (0,120,675,506), (.55,.5), '5 m³', 'Light building waste', 0.32, 'C'),
 ('mck046', PF+'MCK-046.jpg', (0,300,750,562), (.5,.5), '2 m³', 'Plaster & reno offcuts', 0.36, 'C'),
 ('mck052', LG+'15.jpg', (0,150,675,506), (.5,.5), '2 m³', 'Mixed building waste', 0.42, 'C'),
 ('mck070', LG+'29.jpg', (0,150,675,506), (.5,.5), '2 m³', 'Site clean-up', 0.45, 'C'),
 ('mck054', LG+'17.jpg', (0,150,675,506), (.5,.5), '5 m³', 'Synthetic turf & furniture', 0.52, 'C'),
 ('mck095', LG+'52.jpg', (0,150,675,506), (.5,.45), '5 m³', 'Reno & demolition', 0.58, 'C'),
 ('mck096', PF+'MCK-096.jpg', (0,250,750,562), (.5,.5), '8 m³', 'Household clean-out', 0.64, 'G'),
 ('mck088', LG+'45.jpg', (0,230,675,506), (.4,.6), '9 m³', 'Bagged waste', 0.94, 'C'),
 ('mck108', LG+'57.jpg', (0,140,675,506), (.55,.45), '8 m³', 'Shelving & shop fit-out', 0.94, 'C'),
 ('mck085', LG+'42.jpg', (0,230,675,506), (.45,.55), '8 m³', 'Carpet underlay / synthetic turf', 1.00, 'C'),
 ('mck104', LG+'55.jpg', (0,220,675,506), (.5,.5), '12 m³', 'Timber & cabinetry', 1.04, 'C'),
 ('mck091', LG+'49.jpg', (0,230,675,506), (.5,.5), '8 m³', 'Carpet underlay / synthetic turf', 1.28, 'C'),
 ('mck086', PF+'MCK-086.jpg', (0,300,750,562), (.5,.5), '5 m³', 'Timber framing', 1.40, 'C'),
 ('mck044', LG+'9.jpg', (0,200,675,506), (.45,.5), '5 m³', 'Carpet underlay / synthetic turf', 2.20, 'C'),
 ('mck077', LG+'36.jpg', (0,200,675,506), (.5,.5), '3.5 m³', 'Concrete & footings', 3.28, 'K'),
]

def rr(d, box, r, fill):
    d.rounded_rectangle(box, r, fill=fill)

def shadow(base, box, r, off=6, blur=10, alpha=110):
    sh = Image.new('L', base.size, 0)
    ImageDraw.Draw(sh).rounded_rectangle((box[0]+2, box[1]+off, box[2]+2, box[3]+off), r, fill=alpha)
    sh = sh.filter(ImageFilter.GaussianBlur(blur))
    base.paste(Image.new('RGB', base.size, (0, 0, 0)), (0, 0), sh)

def make(key, src, crop, focus, binsz, label, t, rk, special=None):
    x, y, w, h = crop
    im = Image.open(src).convert('RGB').crop((x, y, x+w, y+h)).resize((OW, OH), Image.LANCZOS)
    im = ImageEnhance.Contrast(im).enhance(1.06)
    im = ImageEnhance.Color(im).enhance(1.08)
    im = im.filter(ImageFilter.UnsharpMask(1.4, 60, 2))
    # strong background blur outside the focus ellipse
    bl = im.filter(ImageFilter.GaussianBlur(16))
    bl = ImageEnhance.Brightness(bl).enhance(0.82)
    cx, cy = focus[0]*OW, focus[1]*OH
    m = Image.new('L', im.size, 0)
    ImageDraw.Draw(m).ellipse((cx-400, cy-260, cx+400, cy+260), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(80))
    out = Image.composite(im, bl, m)
    d = ImageDraw.Draw(out)

    rate, rname = RATE[rk]
    cost = round(t * rate)
    if special:
        price, sub, wtxt, rtxt = special
    else:
        price, sub = f'${cost:,}', 'LANDFILL FEE  INC GST'
        wtxt, rtxt = f'{t:.2f} t', f'× ${rate}/t {rname}'

    # top-left tag
    tag = f'{binsz} LOAD  ·  {label}' if binsz else label
    f = BD(26)
    tw = d.textlength(tag, font=f)
    box = (28, 28, 28 + tw + 40, 28 + 52)
    shadow(out, box, 26, off=4, blur=8, alpha=90)
    d = ImageDraw.Draw(out)
    rr(d, box, 26, GREEN)
    d.text((48, 54), tag, font=f, fill='white', anchor='lm')

    # bottom-left price card
    pf, sf = XB(86), BD(19)
    pw = d.textlength(price, font=pf)
    cw = max(pw, d.textlength(sub, font=sf)) + 56
    box = (28, OH - 28 - 168, 28 + cw, OH - 28)
    shadow(out, box, 18)
    d = ImageDraw.Draw(out)
    rr(d, box, 18, GREEN if special else BROWN)
    d.text((28 + 28, OH - 28 - 168 + 10), price, font=pf, fill='white')
    d.text((28 + 28, OH - 28 - 30), sub, font=sf, fill=(232, 222, 205), anchor='lm')

    # weight card next to it
    wf, rf = XB(46), SB(19)
    ww = max(d.textlength(wtxt, font=wf), d.textlength(rtxt, font=rf)) + 56
    bx0 = box[2] + 16
    box2 = (bx0, OH - 28 - 104, bx0 + ww, OH - 28)
    shadow(out, box2, 16)
    d = ImageDraw.Draw(out)
    rr(d, box2, 16, OFF)
    d.text((bx0 + 22, OH - 28 - 104 + 14), wtxt, font=wf, fill=BROWN)
    d.text((bx0 + 22, OH - 28 - 22), rtxt, font=rf, fill=(90, 80, 72), anchor='lm')

    # small credit bottom-right
    cf = SB(17)
    ct = 'Real Snowy Skips load · weighed at the landfill'
    ctw = d.textlength(ct, font=cf)
    if 28 + tw + 40 + 24 > OW - 31 - ctw:
        cx0, cy0 = 32, 104
    else:
        cx0, cy0 = OW - 31 - ctw, 54
    d.text((cx0 + 1, cy0 + 1), ct, font=cf, fill=(0, 0, 0), anchor='lm')
    d.text((cx0, cy0), ct, font=cf, fill='white', anchor='lm')

    out.save(f'/home/claude/lg2/{key}.jpg', quality=86)
    return key, cost

NEW = [
 ('green', '/home/claude/dp/orig/255.jpg', (0,180,750,562), (.5,.5), '', 'Green waste  ·  garden prunings', 0.42, 'R'),
 ('scrap', LG+'57.jpg', (0,140,675,506), (.55,.45), '', 'Scrap steel & metal shelving', 0, 'G', ('FREE', 'NO LANDFILL FEE', 'Scrap metal', 'separated & recycled at the landfill')),
 ('mck050', LG+'14.jpg', (0,260,675,506), (.45,.5), '2 m³', 'Old pallets', 0.18, 'C'),
 ('mck082', LG+'39.jpg', (0,150,675,506), (.5,.5), '2 m³', 'Shed & garage clean-out', 0.30, 'C'),
 ('mck081', LG+'38.jpg', (0,150,675,506), (.5,.5), '6 m³', 'Household clean-out', 0.32, 'G'),
 ('mck037', LG+'4.jpg', (0,230,675,506), (.55,.5), '5 m³', 'Mixed building waste', 0.50, 'C'),
 ('mck098', LG+'54.jpg', (0,200,675,506), (.45,.5), '5 m³', 'Mixed waste & synthetic turf', 0.70, 'C'),
 ('mck061', LG+'22.jpg', (0,150,675,506), (.5,.5), '5 m³', 'Plaster & timber strip-out', 1.16, 'C'),
 ('mck058', LG+'18.jpg', (0,260,675,506), (.5,.5), '8 m³', 'Synthetic turf, rope & site waste', 1.32, 'C'),
 # Peggy Brooks tree removal, Berridale, 18 Oct 2024: $26.49 inc GST at 2024-25 commercial $86/t = 0.31 t
 ('green_trees', '/home/claude/gw18/20241018_125317.jpg', (0,420,1932,1449), (.47,.55), '', 'Green waste  ·  tree removal', 0.31, 'R'),
]

if __name__ == '__main__':
    import sys
    only = [a for a in sys.argv[1:] if a.startswith('mck') or a in ('green','scrap','green_trees')]
    for j in JOBS + NEW:
        if not only or j[0] in only: print(make(*j))
