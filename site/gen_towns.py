import re, json, os, sys
sys.path.insert(0, '/home/claude/site')
from towns import ZONES, ALL, STATE, slug
OUT = '/home/claude/website-live/'
SITE = 'https://snowyskips.com.au'
idx = open(OUT + 'index.html').read()
head_style = re.search(r'<style>.*?</style>', idx, re.S).group(0)
header = idx[idx.index('<header'):idx.index('</header>') + 9]
footer = idx[idx.index('<footer'):idx.index('</footer>') + 9]
fix = lambda h: re.sub(r'href="#', 'href="/#', h).replace('src="img/', 'src="/img/').replace('href="img/', 'href="/img/')
header, footer = fix(header), fix(footer)
IMG = {'alpine': '57286e8b8b.jpg', 'cooma': 'f9142da17d.jpg', 'z1': '65a67a3e77.jpg', 'z2': 'f9142da17d.jpg', 'z3': 'b41b59f532.jpg', 'quote': 'f9142da17d.jpg'}
avail = set(os.listdir(OUT + 'img'))
H = "font-family: 'Sora', sans-serif; font-weight: 800; color: #52372A"
pages = []
for town, zk in ALL:
    z = ZONES[zk]; s = slug(town); st = STATE.get(town, 'NSW')
    img = IMG[zk] if IMG[zk] in avail else '65a67a3e77.jpg'
    title = f'Skip Bin Hire {town} | Rubbish Removal {town} | Snowy Skips'
    if z['prices']:
        desc = f'Skip bin hire in {town}, {st} from {z["prices"][0]} inc GST (2 m³, up to 7 days, plus landfill). Rubbish removal, bin loading, equipment and labour hire. Local, based in Berridale.'
        price = f'''<div style="margin-top: 24px; border: 1px solid #e4e0d8; border-radius: 12px; padding: 22px 24px">
<h2 style="{H}; font-size: 24px; margin: 0">Skip bin prices for {town}</h2>
<p style="margin: 6px 0 0 0; color: #555; font-size: 16px">{town} is in our {z["name"]} pricing area. Indicative prices inc GST, up to 7 days' hire, plus landfill at cost.</p>
<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 14px; margin-top: 14px">
''' + ''.join(f'<div style="background: #F5F2EC; border-radius: 10px; padding: 14px 16px"><div style="{H}; font-size: 22px; color: #4F7230">{sz}</div><div style="font-size: 24px; font-weight: 700">{p}</div><div style="font-size: 14px; color: #D98B4A; font-weight: 600">24-hour hotshot: {h}</div></div>' for sz, p, h in zip(['2 m³', '5 m³', '8 m³'], z['prices'], z['hot'])) + f'''
</div>
<p style="margin: 12px 0 0 0; font-size: 15px; color: #555">We also run bins from 1.5 m³ up to 12 m³, and a 20 m³+ semi tipper for big jobs — call for a price. <a href="/#pricing">See all prices and zones</a> · <a href="/#landfill-costs">Real landfill costs</a></p>
</div>'''
    else:
        desc = f'Skip bin hire and rubbish removal in {town}, {st}. Call Snowy Skips for a price — bins, loading, equipment and labour hire across the Snowy Monaro.'
        price = f'''<div style="margin-top: 24px; background: #EAF1F8; border-radius: 12px; padding: 22px 24px"><h2 style="{H}; font-size: 24px; margin: 0">Prices for {town}</h2><p style="margin: 8px 0 0 0">{z["note"]}</p><p style="margin: 8px 0 0 0"><a href="tel:0408632007" style="font-weight: 700">Call 0408 632 007</a> for a quote.</p></div>'''
    near = [t for t, k in ALL if k == zk and t != town]
    nearhtml = ' · '.join(f'<a href="/skip-bin-hire-{slug(t)}/">{t}</a>' for t in near)
    body = f'''<main>
<section style="background: #F5F2EC">
<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px; display: flex; flex-wrap: wrap; gap: 40px; align-items: center">
<div style="flex: 1 1 480px; min-width: 0">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">SNOWY SKIPS · {town.upper()}</div>
<h1 style="{H}; font-size: 44px; line-height: 1.1; margin: 10px 0 0 0">Skip bin hire &amp; rubbish removal in {town}</h1>
<p style="margin: 14px 0 0 0; font-size: 20px">Snowy Skips delivers skip bins to {town} from our yard in Berridale — and if you'd rather not load it yourself, our crew and machines will do it for you. Every load is weighed and tracked to the landfill, with the docket supplied.</p>
<p style="margin: 10px 0 0 0; font-size: 17px; color: #444">{z["note"]}</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 22px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="/#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</div>
<img src="/img/{img}" alt="Snowy Skips truck and skip bin" style="flex: 1 1 420px; min-width: 0; width: 100%; height: 360px; object-fit: cover; border-radius: 10px; display: block">
</div>
</section>
<section style="max-width: 1240px; margin: 0 auto; padding: 16px 24px 48px 24px">
{price}
<h2 style="{H}; font-size: 28px; margin: 36px 0 0 0">What we do in {town}</h2>
<ul style="margin: 12px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li><a href="/#skip-bins">Skip bin hire</a> — 1.5 m³ to 12 m³ bins for clean-outs, renovations and building sites</li>
<li><a href="/#labour-hire">Rubbish removal</a> — we load it, cart it and tip it, including property clean-outs and cleaning</li>
<li><a href="/#equipment-hire">Equipment hire</a> — small plant, a Vermeer tree chipper, EWP, and machines with an operator</li>
<li><a href="/#equipment-hire">Site establishment</a> — site sheds, containers, toilets, fencing, water and erosion controls</li>
<li><a href="/#soil-venm">Soil and VENM</a> — carted and disposed of properly, with full tracking</li>
</ul>
<p style="margin: 20px 0 0 0; font-size: 17px">Not sure what can go in the bin? Read the <a href="/#skip-bin-guide">Snowy Skips Skip Bin Guide</a>.</p>
{f'<p style="margin: 20px 0 0 0; font-size: 17px"><strong>Nearby:</strong> {nearhtml}</p>' if near else ''}
</section>
</main>'''
    url = f'{SITE}/skip-bin-hire-{s}/'
    ld = {"@context": "https://schema.org", "@type": "LocalBusiness", "name": "Snowy Skips", "url": SITE + "/", "telephone": "+61408632007", "email": "bookings@snowyskips.com.au",
          "address": {"@type": "PostalAddress", "streetAddress": "8-10 Basalt Street", "addressLocality": "Berridale", "addressRegion": "NSW", "postalCode": "2628", "addressCountry": "AU"},
          "areaServed": {"@type": "Place", "name": f"{town}, {st}"}}
    doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{url}">
<link rel="icon" href="/img/09c01ad123.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
{head_style}
<script type="application/ld+json">{json.dumps(ld)}</script>
</head>
<body>
{header}
{body}
{footer}
</body>
</html>'''
    os.makedirs(OUT + f'skip-bin-hire-{s}', exist_ok=True)
    open(OUT + f'skip-bin-hire-{s}/index.html', 'w').write(doc)
    pages.append(url)
# sitemap + robots
sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(f'<url><loc>{u}</loc></url>\n' for u in [SITE + '/'] + pages) + '</urlset>\n'
open(OUT + 'sitemap.xml', 'w').write(sm)
open(OUT + 'robots.txt', 'w').write(f'User-agent: *\nAllow: /\nSitemap: {SITE}/sitemap.xml\n')
print(len(pages), 'town pages')
