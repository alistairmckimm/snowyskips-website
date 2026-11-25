import re, json, os, shutil
P = '/home/claude/site/project/'
LIVE = os.environ.get('LIVE')=='1'
OUT = '/home/claude/website-live/' if LIVE else '/home/claude/website/'
shutil.rmtree(OUT, ignore_errors=True)
os.makedirs(OUT + 'img')
blobmap = json.load(open('/tmp/blobmap.json'))

def body(fn):
    s = open(P + fn).read()
    i = s.index('</helmet>') + len('</helmet>')
    j = s.index('</x-dc>')
    inner = s[i:j].strip()
    # drop the outer wrapper div
    k = inner.index('>') + 1
    assert inner.endswith('</div>')
    return inner[k:-len('</div>')].strip(), re.search(r'<div( id="([^"]+)")? style', inner).group(2)

main, _ = body('Main.dc.html')
h0 = main.index('<header'); h1 = main.index('</header>') + 9
f0 = main.index('<footer'); f1 = main.index('</footer>') + 9
header = main[h0:h1]
footer = main[f0:f1]
home = main[h1:f0]
home = home.replace('<section id="contact" style="background: #4F7230', '<section id="get-started" style="background: #4F7230')
home = home.replace('<a id="quote" href="#quote"', '<a href="#contact"')
import re as _re
header = _re.sub(r'<a href="#(tracking|areas)"[^>]*>[^<]*</a>\n','',header)
header = header.replace('href="#top"', 'href="#home"').replace('href="#book"', 'href="#skip-bins"')
footer = footer.replace('bookings@snowyskips.com.au', '<a href="mailto:bookings@snowyskips.com.au" style="color: #e8e2d9">bookings@snowyskips.com.au</a>')
footer = footer.replace('<p style="margin: 8px 0 0 0">Skip Bins<br>Equipment Hire<br>Labour Hire<br>Waste Tracking</p>',
  '<p style="margin: 8px 0 0 0"><a href="#skip-bins" style="color: #e8e2d9">Skip Bins</a><br><a href="#equipment-hire" style="color: #e8e2d9">Equipment Hire</a><br><a href="#labour-hire" style="color: #e8e2d9">Labour Hire</a><br><a href="#pricing" style="color: #e8e2d9">Pricing</a><br><a href="#landfill-costs" style="color: #e8e2d9">Landfill Costs</a></p>')

pages = [('home', home)]
for fn, pid in [('Skips.dc.html', 'skip-bins'), ('Pricing.dc.html', 'pricing'), ('Landfill.dc.html', 'landfill-costs'),
                ('Equipment.dc.html', 'equipment-hire'), ('Labour.dc.html', 'labour-hire'), ('About.dc.html', 'about'), ('Guide.dc.html', 'skip-bin-guide')]:
    b, _ = body(fn)
    pages.append((pid, b))

html_pages = ''
for pid, b in pages:
    html_pages += f'<main class="page" data-page="{pid}" id="page-{pid}">\n{b}\n</main>\n'

def swap(m):
    bid = m.group(1)
    src = blobmap[bid]
    ext = os.path.splitext(src)[1]
    name = bid[:10] + ext
    if not os.path.exists(OUT + 'img/' + name):
        shutil.copy(src, OUT + 'img/' + name)
    return 'img/' + name
allhtml = (header + html_pages + footer).replace('href="#quote"','href="#contact"').replace('href="#book"','href="#skip-bins"')
allhtml = re.sub(r'/_blob/([0-9a-f]{32})', swap, allhtml)
header2 = allhtml[:len(header)]

doc = f'''<!doctype html>
<html lang="en-AU">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Snowy Skips — Skip Bins, Equipment &amp; Labour Hire | Snowy Monaro</title>
<meta name="description" content="Skip bins, equipment hire and labour hire across the Snowy Monaro. We can load anything for you — every job fully waste tracked. Locally owned in Berridale.">
<meta name="robots" content="noindex">
<link rel="icon" href="img/{blobmap and '09c01ad123.png'}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&family=Source+Sans+3:wght@400;600;700&display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#ffffff;font-family:'Source Sans 3',sans-serif;color:#1f1f1f;font-size:18px;line-height:1.5}}
a{{color:#3d5a24}}a:hover{{color:#52372A}}
.page{{display:none}}.page.active{{display:block}}
header{{position:sticky;top:0;z-index:20}}
details.nav-guides summary::-webkit-details-marker{{display:none}}
details.nav-guides a:hover{{background:#F5F2EC}}
nav a.current{{color:#4F7230 !important;text-decoration:underline !important;text-underline-offset:6px}}
.preview-bar{{background:#D98B4A;color:#fff;text-align:center;font-size:14px;padding:6px 12px;font-weight:600}}
img{{max-width:100%}}
@media (max-width:720px){{
 h2{{font-size:32px !important}}
 header nav{{order:3;width:100%;overflow-x:auto;flex-wrap:nowrap !important;white-space:nowrap}}
 section{{padding-left:16px !important;padding-right:16px !important}}
}}
</style>
</head>
<body>
<div class="preview-bar">Preview — not live yet. Prices and bookings are for testing only.</div>
{allhtml}
<script>
(function(){{
  var pages=[].slice.call(document.querySelectorAll('.page'));
  function show(hash){{
    var id=(hash||'').replace('#','')||'home';
    var target=document.getElementById(id), page=null;
    pages.forEach(function(p){{ if(p.dataset.page===id) page=p; }});
    if(!page && target){{ page=target.closest('.page'); }}
    if(!page){{ page=pages[0]; target=null; }}
    pages.forEach(function(p){{ p.classList.toggle('active', p===page); }});
    document.querySelectorAll('header nav a').forEach(function(a){{
      a.classList.toggle('current', a.getAttribute('href')==='#'+page.dataset.page);
    }});
    if(target && target!==page && page.dataset.page!==id){{
      setTimeout(function(){{ var y=target.getBoundingClientRect().top+window.scrollY-150; window.scrollTo(0,y); }},0);
    }} else {{ window.scrollTo(0,0); }}
  }}
  window.addEventListener('hashchange',function(){{show(location.hash); document.querySelectorAll('details.nav-guides').forEach(function(d){{d.open=false;}});}});
  document.addEventListener('click',function(e){{document.querySelectorAll('details.nav-guides').forEach(function(d){{if(!d.contains(e.target))d.open=false;}});}});
  show(location.hash);
  document.querySelectorAll('form').forEach(function(f){{
    var b=f.querySelector('button'); if(!b) return;
    b.addEventListener('click',function(){{ b.textContent='Thanks — this is a preview, so nothing was sent yet.'; b.disabled=true; }});
  }});
}})();
</script>
</body>
</html>
'''

if LIVE:
    import sys as _s; _s.path.insert(0,'/home/claude/site')
    from towns import ALL as _ALL, STATE as _ST, slug as _slug
    _lst=' · '.join(t for t,_ in _ALL)
    _links=' · '.join(f'<a href="/skip-bin-hire-{_slug(t)}/" style="color: #3d5a24">{t}</a>' for t,_ in _ALL)
    assert _lst in doc
    doc = doc.replace(_lst, _links)
    doc = doc.replace('<title>Snowy Skips — Skip Bins, Equipment &amp; Labour Hire | Snowy Monaro</title>',
      '<title>Skip Bin Hire Berridale, Jindabyne, Cooma &amp; Snowy Monaro | Snowy Skips</title>')
    doc = doc.replace('<meta name="description" content="Skip bins, equipment hire and labour hire across the Snowy Monaro. We can load anything for you — every job fully waste tracked. Locally owned in Berridale.">',
      '<meta name="description" content="Skip bin hire and rubbish removal in Berridale, Jindabyne, Cooma, Bombala, Delegate, Thredbo, Perisher and across the Snowy Monaro. Bins 1.5–12 m³, we can load it for you, equipment and labour hire. Every load waste tracked. Locally owned in Berridale.">\n<link rel="canonical" href="https://snowyskips.com.au/">')
    _ld={"@context":"https://schema.org","@type":"LocalBusiness","name":"Snowy Skips","description":"Skip bin hire, rubbish removal, equipment hire and labour hire across the Snowy Monaro.","url":"https://snowyskips.com.au/","telephone":"+61408632007","email":"bookings@snowyskips.com.au",
      "address":{"@type":"PostalAddress","streetAddress":"8-10 Basalt Street","addressLocality":"Berridale","addressRegion":"NSW","postalCode":"2628","addressCountry":"AU"},
      "parentOrganization":{"@type":"Organization","name":"McKimm Civil Pty Ltd"},
      "sameAs":["https://g.page/r/CVmI479DHoovEAE"],
      "areaServed":[{"@type":"Place","name":f"{t}, {_ST.get(t,'NSW')}"} for t,_ in _ALL]}
    import json as _j
    doc = doc.replace('</head>', '<script type="application/ld+json">'+_j.dumps(_ld)+'</script>\n</head>',1)
    _fl='<div style="max-width: 1240px; margin: 0 auto; padding: 0 24px 24px 24px; font-size: 14px; line-height: 1.8; color: #cfc4b8"><strong style="color: #e8e2d9">Skip bin hire &amp; rubbish removal:</strong> ' + ' · '.join(f'<a href="/skip-bin-hire-{_slug(t)}/" style="color: #cfc4b8">{t}</a>' for t,_ in _ALL) + '</div>\n</footer>'
    _i=doc.rindex('</footer>'); doc=doc[:_i]+_fl+doc[_i+len('</footer>'):]
    # Dropdown menus: close when clicking outside, picking a link, opening another menu, or pressing Esc.
    _navjs = ('<script>(function(){var M=document.querySelectorAll("details.nav-guides");'
      'function shut(x){for(var i=0;i<M.length;i++){if(M[i]!==x)M[i].removeAttribute("open");}}'
      'for(var i=0;i<M.length;i++){M[i].addEventListener("toggle",function(){if(this.open)shut(this);});}'
      'document.addEventListener("click",function(e){var t=e.target;for(var i=0;i<M.length;i++){var d=M[i];'
      'if(d.open&&(!d.contains(t)||(t.closest&&t.closest("a"))))d.removeAttribute("open");}});'
      'document.addEventListener("keydown",function(e){if(e.key==="Escape")shut(null);});})();</script>\n</header>')
    assert doc.count('</header>')==1
    doc = doc.replace('</header>', _navjs, 1)
    # Christmas hours banner hides itself from Mon 4 Jan 2027 (Sydney time), even if nobody rebuilds the site.
    if 'id="christmas-hours"' in doc:
        _ci=doc.index('id="christmas-hours"'); _ce=doc.index('</section>',_ci)+len('</section>')
        doc=doc[:_ce]+'\n<script>if(Date.now()>=Date.parse("2027-01-04T00:00:00+11:00")){var _xb=document.getElementById("christmas-hours");if(_xb)_xb.remove();}</script>'+doc[_ce:]

LIVE_JS = "b.addEventListener('click',function(){ var NL=String.fromCharCode(10); var v=[].slice.call(f.querySelectorAll('input:not([type=file]),select,textarea')).map(function(e){ var l=e.closest('label'); return (l?l.firstChild.textContent.trim():'')+': '+e.value; }); var nm=f.querySelector('input[type=text]'); var sub='Quote request'+(nm&&nm.value?' - '+nm.value:''); location.href='mailto:bookings@snowyskips.com.au?subject='+encodeURIComponent(sub)+'&body='+encodeURIComponent(v.join(NL)+NL+NL+'(Attach photos of what is going here.)'); b.textContent='Your email app should open with the details - attach photos and press send.'; });"

if LIVE:
    doc = doc.replace('<div class="preview-bar">Preview — not live yet. Prices and bookings are for testing only.</div>\n','')
    doc = doc.replace('<meta name="robots" content="noindex">\n','')
    doc = doc.replace("b.addEventListener('click',function(){ b.textContent='Thanks — this is a preview, so nothing was sent yet.'; b.disabled=true; });", LIVE_JS)
    doc = re.sub(r'<label([^>]*)>Photos of what\'s going \(helps us quote\)<input[^>]*></label>', r'<p\1>Photos help us quote: when your email opens, attach a few clear photos of what is going before you press send.</p>', doc)
    open(OUT + 'CNAME', 'w').write('snowyskips.com.au\n')

open(OUT + 'index.html', 'w').write(doc)
print(len(doc), len(os.listdir(OUT + 'img')))
