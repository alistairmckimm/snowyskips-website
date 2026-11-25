# One-off edit script (25 Nov 2026): Concrete removal & disposal page + links.
p = 'gen_pages.py'; s = open(p).read()

# menu
a = '''f'<a href="{pre}#farm-commercial-clean-ups" style="{a}">Farm &amp; commercial clean-ups</a>\''''
assert s.count(a) == 1
s = s.replace(a, a + '''
            f'<a href="{pre}#concrete-removal" style="{a}">Concrete removal &amp; disposal</a>\'''', 1)
# footer
a = '''<br><a href="#farm-commercial-clean-ups" style="color: #e8e2d9">Farm &amp; commercial clean-ups</a>'''
assert s.count(a) == 1
s = s.replace(a, a + '''<br><a href="#concrete-removal" style="color: #e8e2d9">Concrete removal</a>''', 1)

BTN = '<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>'
UL = '<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">'
FIG = '<figure style="flex: 1 1 240px; min-width: 0; margin: 0"><img src="/img/{f}" alt="{alt}" style="width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 6px">{cap}</figcaption></figure>'
photos = ('<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-top: 28px">'
          + FIG.format(f='concrete-saw.jpg', alt='Concrete saw cutting along a path next to a brick wall', cap='Saw-cutting a clean edge')
          + FIG.format(f='concrete-rubble-bin.jpg', alt='Broken concrete loaded in a Snowy Skips bin', cap='Broken concrete, kept separate')
          + FIG.format(f='bricks-bin.jpg', alt='Old bricks loaded level in a galvanised skip bin', cap='Bricks loaded level for the road')
          + '</div>')

html = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">CONCRETE REMOVAL &amp; DISPOSAL</div>
<h1 style="{{HS}}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Concrete removal and disposal: we cut it, break it, load it and cart it away.</h1>
<p style="margin: 16px 0 0 0; font-size: 20px">Old driveways, paths, slabs, footings and brick rubble. Concrete removal is one of our specialties, for builders, commercial sites, councils and homeowners right across the Snowy Monaro.</p>
{BTN}
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
{photos}
<h2 style="{{H2}}">What we remove</h2>
{UL}
<li>Driveways, footpaths and paved areas</li>
<li>Concrete slabs, including old shed and garage slabs</li>
<li>Footings, piers, kerbs and old retaining walls</li>
<li>Brick rubble, pavers and blocks</li>
<li>Concrete and brick waste from building and renovation jobs</li>
</ul>
<h2 style="{{H2}}">How we do it</h2>
<p style="{{P}}">We saw-cut a clean, straight edge so the concrete that's staying isn't damaged, then break it out with jackhammers and breakers, or with our machines on bigger jobs. Our crew loads it straight into our trucks or bins and carts it away. Small job or large commercial site, you get one crew with the saws, breakers, machines and trucks.</p>
<h2 style="{{H2}}">Disposal done right, and cheaper</h2>
<p style="{{P}}">We keep concrete and bricks separate from general rubbish, because clean concrete and bricks are charged at a much cheaper landfill rate than mixed building waste. Every load is weighed on the landfill weighbridge and you get the dockets. See <a href="#landfill-costs">landfill fees</a> for real loads we've weighed.</p>
<h2 style="{{H2}}">Doing it yourself? Hire a bin, but watch the weight</h2>
<p style="{{P}}">Concrete, bricks and rubble are extremely heavy. A bin can be over the legal weight long before it looks full, so ask us for a smaller bin and a fill mark inside it showing how high you can load. Keep concrete and bricks out of your general rubbish bin to save on the landfill fee.</p>
<h2 style="{{H2}}">Pricing</h2>
<p style="{{P}}">Concrete removal is priced on the job: how much there is, how thick it is, whether it's reinforced, and how easy it is to get to. Send us a few photos and rough measurements and we'll give you a price.</p>
{BTN}
</section>'''
assert "'''" not in html
blk = f"# ---------- concrete-removal ----------\nmains['concrete-removal'] = f'''{html}'''\nPAGES.append('concrete-removal')\n\n"
a2 = "# ---------- Single item pickup ----------"
assert s.count(a2) == 1
s = s.replace(a2, blk + a2, 1)

a3 = " 'farm-commercial-clean-ups': ("
assert s.count(a3) == 1
s = s.replace(a3, " 'concrete-removal': ('Concrete Removal & Disposal | Driveways, Slabs & Footings | Snowy Monaro | Snowy Skips',\n"
                  "   'Concrete removal and disposal across the Snowy Monaro: driveways, paths, slabs, footings and brick rubble. Saw-cut, broken out, loaded and carted away, with weighbridge dockets.'),\n" + a3, 1)

# link from the farm & commercial page
a4 = "<li>Commercial sites: warehouse and shop clean-outs, end-of-lease strip-outs and yard clean-ups</li>"
assert s.count(a4) == 1
s = s.replace(a4, a4 + "\n<li>Old slabs, footings and concrete: see <a href=\"#concrete-removal\">concrete removal &amp; disposal</a></li>", 1)
open(p, 'w').write(s)
print('ok')
