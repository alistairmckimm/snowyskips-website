"""Split the single-page live build into one real page per section, add /faq/, rewrite links, write sitemap.
Run after: LIVE=1 build_site.py ; gen_towns.py"""
import re, json, os, glob, html as H_
OUT = '/home/claude/website-live/'
SITE = 'https://snowyskips.com.au'
d = open(OUT + 'index.html').read()

head = d[:d.index('<body>')]
header = d[d.index('<header'):d.index('</header>') + 9]
footer = d[d.index('<footer'):d.index('</footer>') + 9]
mains = dict(re.findall(r'<main class="page" data-page="([^"]+)" id="page-[^"]+">\n(.*?)\n</main>', d, re.S))
forms_js = re.search(r"  document\.querySelectorAll\('form'\)\.forEach\(.*?\n  \}\);\n", d, re.S).group(0)
PAGES = list(mains)  # home, skip-bins, pricing, ...

# FAQ link in the Customer Guide menu
header = header.replace('Snowy Skips Skip Bin Guide</a>',
    'Snowy Skips Skip Bin Guide</a><a href="#faq" style="display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none">Skip bin FAQs</a><a href="#skip-bin-permits" style="display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none">Council permits for skip bins</a><a href="#too-good-to-tip" style="display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none">Too Good to Tip Giveaways</a>', 1)
# Labour Hire dropdown (labour hire, insurance & accident clean-ups, single item pickups)
def _labour_menu(pre):
    a = 'display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none'
    return ('<details class="nav-guides" style="position: relative; padding: 10px 0"><summary style="cursor: pointer; list-style: none; color: #1f1f1f">Labour Hire ▾</summary>'
            '<div style="position: absolute; top: 100%; left: -12px; z-index: 30; background: #ffffff; border: 1px solid #e4e0d8; border-radius: 8px; box-shadow: 0 8px 24px rgba(0,0,0,0.12); padding: 8px 0; min-width: 320px; font-size: 16px; white-space: normal">'
            f'<a href="{pre}#labour-hire" style="display: block; padding: 8px 16px; color: #52372A; font-weight: 700; text-decoration: none">Labour hire &amp; clean-outs</a>'
            f'<a href="{pre}#insurance-accident-clean-ups" style="{a}">Insurance &amp; accident clean-ups</a>'
            f'<a href="{pre}#farm-commercial-clean-ups" style="{a}">Farm &amp; commercial clean-ups</a>'
            f'<a href="{pre}#concrete-removal" style="{a}">Concrete removal &amp; disposal</a>'
            f'<a href="{pre}#deceased-estate-clean-outs" style="{a}">Deceased estate &amp; pre-sale clean-outs</a>'
            f'<a href="{pre}#single-item-pickup" style="{a}">Single item pickups</a></div></details>')
_LH = '<a href="#labour-hire" style="color: #1f1f1f; text-decoration: none; padding: 10px 0">Labour Hire</a>'
assert header.count(_LH) == 1
header = header.replace(_LH, _labour_menu(''), 1)
_FL = '<a href="#labour-hire" style="color: #e8e2d9">Labour Hire</a>'
if _FL in footer: footer = footer.replace(_FL, _FL + '<br><a href="#insurance-accident-clean-ups" style="color: #e8e2d9">Insurance &amp; accident clean-ups</a><br><a href="#farm-commercial-clean-ups" style="color: #e8e2d9">Farm &amp; commercial clean-ups</a><br><a href="#concrete-removal" style="color: #e8e2d9">Concrete removal</a><br><a href="#deceased-estate-clean-outs" style="color: #e8e2d9">Deceased estate clean-outs</a>', 1)
footer = footer.replace('<a href="#landfill-costs" style="color: #e8e2d9">Landfill Costs</a>',
    '<a href="#landfill-costs" style="color: #e8e2d9">Landfill Costs</a><br><a href="#faq" style="color: #e8e2d9">FAQs</a>', 1)

# ---------- FAQ ----------
FAQ = [
 ("What size skip bins do you have?",
  "We run bins from 1.5 m³ right through to 12 m³. Our most popular sizes are the 2 m³ mini skip, the 5 m³ renovation skip and the 8 m³ builder's skip. For big jobs our crew can hand load straight into our semi tipper trailer, over 20 m³ in one go. Not sure which size? Send us a photo of what's going and we'll tell you.",
  'See <a href="/skip-bins/">skip bin sizes</a>.'),
 ("How much does a skip bin cost?",
  "Prices start from $330 inc GST for a 2 m³ bin in Cooma, for up to 7 days' hire, plus landfill at cost. Berridale, Jindabyne and other areas cost a little more depending on the distance. Prices on the website are a guide only. If our trucks are already working in your area and you can be flexible on times, we can often give you a sharper quote.",
  'See <a href="/pricing/">prices for your area</a>.'),
 ("How is the landfill fee worked out?",
  "Landfill is charged on top of the bin hire, at cost, at the council's current rates. Every load is weighed on the landfill weighbridge and you get the docket. As a rough guide, a 2 m³ household clean-out we weighed at 0.24 t cost about $65 to tip, and a 5 m³ load of timber and building waste at 1.4 t cost about $450.",
  'See <a href="/landfill-costs/">real loads and what they cost</a>.'),
 ("How long can I keep the bin?",
  "Prices cover up to 7 days. After that it's $15 a day for a 2 m³ bin, $20 a day for a 5 m³ bin and $25 a day for an 8 m³ bin. Farms, rural properties and building sites can also keep a permanent bin with no set pickup days. Give us a few days' notice when it's ready to empty and we'll fit it into our regular runs, which keeps the price well down.", ''),
 ("How quickly can you deliver a skip bin?",
  "We can generally deliver and pick up within 24 hours' notice, but ideally book well ahead so your project runs smoothly. ASAP and emergency jobs may cost extra.", ''),
 ("Is it cheaper to get a changeover or more than one bin?",
  "Usually, yes. Swapping a full bin for an empty one, or booking several bins on the same run, means less travel and handling for us, so we can generally give you a sharper price. Ask us when you book.",
  'See <a href="/pricing/">pricing and service areas</a>.'),
 ("We've just built and council won't give us bins yet. Can you help?",
  "Yes, this is one of our specialties. Until a new home or building has its occupation certificate, council usually won't supply wheelie bins. We can put a small permanent bin on site and empty it whenever you need, until your council bins arrive.",
  'See <a href="/pricing/">pricing</a>.'),
 ("What is a 24-hour hotshot?",
  "A quick turnaround: we drop the bin off and pick it up the next day. Hotshot prices are generally 10% less than standard hire, and up to 15% less if our trucks are already nearby. Hotshot discounts don't apply below our minimum charge.", ''),
 ("What can go in a skip bin?",
  "General household rubbish, building, renovation and demolition waste, timber, plasterboard, carpet, underlay, synthetic turf, furniture, and green waste and garden prunings. Concrete, bricks and rubble can go in too, but they're heavy, so don't overfill. Green waste, concrete and clean scrap steel are much cheaper to tip on their own, so ask us about a separate bin.",
  'Read the <a href="/skip-bin-guide/">Skip Bin Guide</a>.'),
 ("What can't go in a skip bin?",
  "Never put asbestos, liquids or sludge, food waste, medical waste and sharps, or animal carcasses in a skip bin. Contact us and we can guide you in the right direction to have these correctly and lawfully serviced.", ''),
 ("Can lithium batteries or battery-powered tools go in a skip bin?",
  "Never. Lithium batteries, and anything with one inside (phones, vapes, laptops, power tool packs, e-bikes, toys, solar lights), can catch fire when they're crushed or damaged in a bin or on the truck. Those fires are fierce, give off toxic smoke and are very hard to put out, and they put our drivers, the public and the landfill at risk. Keep them out of your bin and let us know when you book: we can take batteries and battery equipment away separately, packed safely, and send them to an authorised recycler. Never put hot ashes, gas bottles, fuel or chemicals in a bin either.",
  'Read the <a href="/skip-bin-guide/">Skip Bin Guide</a>.'),
 ("Can I put a mattress, fridge or tyres in the bin?",
  "Ask us first. Fridges, freezers, air-conditioners, mattresses, tyres, batteries, paint, gas bottles, chemicals, TVs and electronics go to their own area at the landfill. Place them on top of the load so they can be separated. A separation fee of $49.50 inc GST and the item's own council fee apply.",
  'See <a href="/pricing/#extra-charges">extra charges</a>.'),
 ("Can you pick up just one item, like a fridge or a mattress?",
  "Yes. You don't need a whole skip bin for one fridge, a mattress, a couch or a desk. If our trucks are in your area, a single item pickup is generally $49 plus the landfill fee for the item. Further out, the price depends on the distance and where our trucks are running, so call us for a quote.",
  'See <a href="/single-item-pickup/">single item pickups</a>.'),
 ("Do you do large farm or commercial clean-ups with heavy steel or lots of batteries?",
  "Yes. On large farm and commercial clean-ups with a lot of heavy scrap steel or a large number of car batteries, the scrap has value to authorised recyclers, so we may be able to do the bins and pickup for free or at a reduced price, depending on how much there is and where you are. This doesn't apply to small loads. We package the batteries to meet the legal requirements for transporting them and remove everything from site, so you don't have to handle it. Give us a call to talk it through.",
  ''),
 ("Do I need a council permit for a skip bin?",
  "On your own property (driveway, yard or building site) you generally don't need one. If the bin has to go on the road, nature strip or footpath, you need Snowy Monaro Regional Council's approval under Section 138 of the Roads Act first. We can handle the application for you: we hold $20 million public liability insurance and have the safe work method statements, and an accredited traffic control company prepares the traffic plan. Allow time for council to approve it.",
  'Read <a href="/skip-bin-permits/">council permits for skip bins</a>.'),
 ("How full can I fill the bin?",
  "Level with the top or below. Nothing over the sides or sticking up, because an overloaded bin can't be carried safely or legally until it's levelled off. Soil, concrete, bricks and rock are extremely heavy, so a bin can be over the legal weight long before it's full. Ask us to put a mark inside your bin showing how high you can fill it.",
  'See <a href="/skip-bins/#loading-tips">loading tips</a>.'),
 ("Can you load the bin for me?",
  "Yes. You don't have to load a bin at all. Our crew and machines can come to your site, load it, separate it and take it right through to the landfill. Send us a few clear photos of everything that's going and we can generally quote the whole job, bin and loading together.",
  'See <a href="/labour-hire/">labour hire and clean-outs</a>.'),
 ("What areas do you service?",
  "We're based in Berridale and service the whole Snowy Monaro: Cooma, Polo Flat, Berridale, Jindabyne, East Jindabyne, Kalkite, Dalgety, Crackenback, Adaminaby, Bredbo, Numeralla, Nimmitabel, Bombala, Delegate, Michelago and more. Thredbo, Perisher, Charlotte Pass and the alpine resorts are by quote, because access can be difficult. We also go further out by quote: the Upper Murray around Khancoban, Corryong and Walwa, and East Gippsland around Bendoc and Cann River.",
  'See <a href="/pricing/">service areas and zones</a>.'),
 ("Can you take soil, fill or VENM?",
  "Yes. Under NSW law excavated soil is classed as waste, even when it's clean. We cart and dispose of virgin excavated natural material (VENM) in our skip bins and trucks with the right paperwork and full tracking. Soil generally needs to be tested before it's moved, and it must be kept clean and never mixed with other waste.",
  'See <a href="/skip-bins/#soil-venm">how we handle soil and VENM</a>.'),
 ("Do you price match?",
  "Yes. Send us a genuine written quote or published price from a local operator servicing the Snowy Monaro, dated within the last 7 days, for the same job, before you book, and we'll match it.",
  'See <a href="/pricing/#price-match">how our price match works</a>.'),
 ("What happens to my waste?",
  "Every bin we run is documented from order to landfill. Your load is weighed, tipped at a landfill or recycling centre that can lawfully accept it, and you get a docket with the weight, tip receipt and photos.", ''),
]
HS = "font-family: 'Sora', sans-serif; font-weight: 800; color: #52372A"
faq_items = ''.join(f'''<details style="border-bottom: 1px solid #e4e0d8; padding: 18px 0">
<summary style="cursor: pointer; font-family: 'Sora', sans-serif; font-weight: 700; font-size: 20px; color: #52372A">{H_.escape(q)}</summary>
<p style="margin: 10px 0 0 0">{H_.escape(a)}{(' ' + more) if more else ''}</p>
</details>
''' for q, a, more in FAQ)
mains['faq'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 900px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">FREQUENTLY ASKED QUESTIONS</div>
<h1 style="{HS}; font-size: 44px; line-height: 1.1; margin: 10px 0 0 0">Skip bin questions, answered</h1>
<p style="margin: 14px 0 0 0; font-size: 20px">Sizes, prices, landfill, permits and what can go in. Can't see your question? Call us on <a href="tel:0408632007" style="font-weight: 700">0408 632 007</a>.</p>
</div>
</section>
<section style="max-width: 900px; margin: 0 auto; padding: 16px 24px 56px 24px">
{faq_items}
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 32px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</section>'''
faq_ld = {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
    {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a, _ in FAQ]}
PAGES.append('faq')

# ---------- Permit article ----------
P = "margin: 14px 0 0 0; font-size: 18px; line-height: 1.6"
H2 = HS + "; font-size: 28px; margin: 36px 0 0 0"
mains['skip-bin-permits'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">SKIP BIN GUIDE</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Do I need a council permit for a skip bin in the Snowy Monaro?</h1>
<p style="margin: 16px 0 0 0; font-size: 20px"><strong>The short answer:</strong> if the bin goes on your own property (your driveway, yard or building site), you generally don't need a permit. If it has to go on the road, nature strip or footpath, you need Snowy Monaro Regional Council's approval first, and we can look after that for you.</p>
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<h2 style="{H2}">On your own property</h2>
<p style="{P}">Most of our bins go on driveways. We need firm, level ground, clear access for the truck and no low wires overhead. If the bin or truck has to go over grass or a finished surface, tell us when you book and we'll work out the best spot with you. Our <a href="/skip-bins/">2 m³ mini skip</a> suits tight driveways and town blocks.</p>
<h2 style="{H2}">On the road, nature strip or footpath</h2>
<p style="{P}">The road reserve (the road, kerb, nature strip and footpath) is controlled by council. Under Section 138 of the NSW Roads Act, any activity in the road reserve needs council's consent before it happens, and Snowy Monaro Regional Council lists skip bins among the activities that need a road management approval.</p>
<p style="{P}">The application is lodged through the NSW Planning Portal. Council asks for:</p>
<ul style="margin: 10px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>public liability insurance of at least $20 million, in the applicant's name, with council noted as an interested party</li>
<li>a traffic control plan prepared by an accredited person</li>
<li>a safe work method statement and details of the work</li>
<li>council's application fee, as set in its Fees and Charges</li>
</ul>
<h2 style="{H2}">We can do the paperwork for you</h2>
<p style="{P}">Snowy Skips holds $20 million public liability and professional indemnity insurance, and we already have the safe work method statements. Our traffic control plans are prepared by an accredited traffic control company in Jindabyne, usually within about 2 days. So we can apply for the permit on your behalf and look after the whole job, from the application to delivery, pickup and disposal.</p>
<p style="{P}">The approval itself depends on council's processing time, so let us know as early as you can. Where it makes sense, we'll still look for a spot on your property first, because it's quicker and cheaper for you.</p>
<h2 style="{H2}">Not sure where your bin can go?</h2>
<p style="{P}">Send us a photo of the spot, or call us on <a href="tel:0408632007" style="font-weight: 700">0408 632 007</a>, and we'll tell you whether it needs a permit.</p>
<p style="margin: 24px 0 0 0; font-size: 15px; color: #555">This is general information, not legal advice. Council's requirements can change; check with <a href="https://www.snowymonaro.nsw.gov.au/Building-and-Planning/Development-Engineering/Works-Within-the-Road-Road-Management-Approvals-s138" rel="noopener">Snowy Monaro Regional Council</a> for the current rules.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a><a href="#faq" style="color: #4F7230; font-weight: 700; padding: 14px 6px">More skip bin FAQs</a></div>
</section>'''
PAGES.append('skip-bin-permits')

# ---------- Insurance & accident clean-ups ----------
mains['insurance-accident-clean-ups'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">INSURANCE &amp; ACCIDENT CLEAN-UPS</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Storm, fire, flood or accident damage? We clear the site so your builder can start.</h1>
<p style="margin: 16px 0 0 0; font-size: 20px">One local contractor for the whole clean-up: skip bins, machinery and a crew to load it, across the Snowy Monaro. We work with homeowners, builders, loss adjusters and insurers, and every load is tracked with weighbridge dockets.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
<p style="margin: 14px 0 0 0; font-size: 16px; color: #52372A"><strong>24-hour emergency call-outs</strong> for storm damage, fallen trees and make-safe work.</p>
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-top: 28px"><figure style="flex: 1 1 300px; min-width: 0; margin: 0"><img src="/img/roof-blown-off-lodge.jpg" alt="Roof sheeting and timber torn off a lodge in a storm, with a Snowy Skips mini excavator clearing it" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 6px">Storm damage: removal of the roof structure before any further strong winds could blow light materials throughout the national park and further increase clean-up costs.</figcaption></figure><figure style="flex: 1 1 300px; min-width: 0; margin: 0"><img src="/img/lodge-water-damage.jpg" alt="Water across the timber floor of a lodge after the roof blew off" style="width: 100%; aspect-ratio: 4 / 5; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 6px">Water damage inside the building: removal of water and debris before further structural damage to the building and subfloor levels.</figcaption></figure></div>
<h2 style="{H2}">Get us in straight away</h2>
<p style="{P}">After a storm, fire or flood, the first few hours matter. The sooner the site is made safe and cleared, the less extra damage there is: loose roofing iron and debris can blow into neighbouring properties and the bush, and water that gets in keeps spreading through floors and walls. Insurers generally expect damage to be kept from getting worse, so call us as soon as it happens, day or night, on <a href="tel:0408632007">0408 632 007</a>.</p>
<h2 style="{H2}">What we do</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li><strong>Full clean-outs</strong> of damaged contents: furniture, carpets, whitegoods, flood-soaked and smoke-damaged items.</li>
<li><strong>Strip-outs</strong>: wet plasterboard, carpet and underlay, kitchens, flooring and fittings that need to come out before repairs.</li>
<li><strong>Small demolition</strong>: damaged sheds, carports, garages, decks and small single-storey structures (see the note on demolition below).</li>
<li><strong>Make-safe and site clean-up</strong>: storm debris, fallen trees (we have a 12-inch tree chipper), broken fencing, and clearing up after a vehicle has gone through a fence, carport or shed.</li>
<li><strong>Site set-up for the rebuild</strong>: temporary fencing, site toilets, site sheds and containers, and bins for the builder.</li>
</ul>
<p style="{P}">Bins, machines and labour all come from us, so there's one booking, one invoice and one set of records.</p>
<h2 style="{H2}">Records for your insurer or loss adjuster</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Geotagged, date- and time-stamped photos before, during and after the clean-up, plus video where it helps</li>
<li>Live video calls from site with you, your loss adjuster or insurer while the job is under way, so they can see the damage and the work without travelling</li>
<li>Weighbridge dockets for every load, with tonnes by waste type</li>
<li>A clear, itemised invoice for bins, labour, machinery and landfill</li>
<li>A written quote or scope for the assessor before we start, where the claim needs one</li>
</ul>
<p style="{P}">Every job goes through our <a href="#tracking">waste tracking</a>, so you can show exactly what was removed and where it went.</p>
<h2 style="{H2}">We can manage the whole job, from damage to ready-to-build</h2>
<p style="{P}">Snowy Skips can run the entire process for you under one management overlay: making the site safe, the clean-up, the records, and keeping you, your insurer and the loss adjuster up to date. We hand over to your builder when you're ready, either once the site is cleared, or after we've also done the site preparation so it's ready to go. One point of contact from the day of the damage until the rebuild starts.</p>
<h2 style="{H2}">Asbestos comes out first</h2>
<p style="{P}">Many homes built before 1990 contain asbestos, and fire or storm damage can break it up. If asbestos may be present, it must be checked and removed by a licensed asbestos removalist before anyone else works on the site. Once the area has been cleared, we take over the rest of the clean-up. We don't remove asbestos and it can't go in our skip bins.</p>
<h2 style="{H2}">A note on demolition</h2>
<p style="{P}">We take down small damaged structures that don't need a demolition licence in NSW: generally structures under 6 metres high, with no machinery working on a raised or suspended floor. Anything bigger goes to a licensed demolition contractor, and we can supply the bins, machinery and cartage for them.</p>
<h2 style="{H2}">How it works</h2>
<ol style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Call us on <a href="tel:0408632007">0408 632 007</a>. For urgent storm or make-safe work, call any time, day or night.</li>
<li>We look at the site (or your photos) and give you, your builder or the assessor a quote and scope.</li>
<li>We isolate the site and make it safe before anyone goes in: physical barriers and warning signage, a full site safety inspection, and we work alongside licensed contractors who can safely certify that services such as power, gas and water are isolated before entry. These are the same safety systems we use on our McKimm Civil construction sites. Doing this quickly helps prevent further damage to the building's structure, pavements and the rest of the property.</li>
<li>We clear the site, keeping everything separated so recyclable and cheaper-to-tip waste costs less.</li>
<li>You get the photos, dockets and invoice for the claim, and the site is ready for the builder.</li>
</ol>
<h2 style="{H2}">For loss adjusters and builders</h2>
<p style="{P}">Need a local contractor in the Snowy Monaro, Upper Murray or far East Gippsland? We know the area, run our own trucks and machinery, and can usually start sooner than a contractor travelling from the city. Call Al on <a href="tel:0408632007">0408 632 007</a> or email <a href="mailto:bookings@snowyskips.com.au">bookings@snowyskips.com.au</a>.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a><a href="#labour-hire" style="color: #4F7230; font-weight: 700; padding: 14px 6px">Labour hire &amp; clean-outs</a></div>
</section>'''
PAGES.append('insurance-accident-clean-ups')

# ---------- farm-commercial-clean-ups ----------
mains['farm-commercial-clean-ups'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">FARM &amp; COMMERCIAL CLEAN-UPS</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Big clean-up on the farm or at the business? We bring the bins, machines and crew.</h1>
<p style="margin: 16px 0 0 0; font-size: 20px">Old machinery, sheds, wire, scrap steel, car batteries and years of built-up rubbish. We clear large farm and commercial sites right across the Snowy Monaro, Upper Murray and far East Gippsland.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<h2 style="{H2}">What we clear</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Old machinery, vehicles, implements and heavy scrap steel</li>
<li>Fencing wire, posts, old yards and collapsed or unwanted sheds</li>
<li>Large numbers of car and truck batteries</li>
<li>General rubbish, timber, tyres and green waste from around the property</li>
<li>Commercial sites: warehouse and shop clean-outs, end-of-lease strip-outs and yard clean-ups</li>
<li>Old slabs, footings and concrete: see <a href="#concrete-removal">concrete removal &amp; disposal</a></li>
</ul>
<h2 style="{H2}">Scrap steel and batteries have value</h2>
<p style="{P}">Heavy scrap steel and batteries go to authorised scrap metal recyclers in the cities, not landfill. Because the scrap is worth something, on <strong>large jobs</strong> the bins and pickup <strong>may be free or reduced</strong>, depending on how much there is and where the property is. Give us a call and we'll take a look. (This is for big clean-ups only, not small loads of steel.)</p>
<p style="{P}">Batteries are packed to meet the legal requirements for transport and taken off site separately. They never go in a skip bin.</p>
<h2 style="{H2}">Machines, crew and bins on site</h2>
<p style="{P}">We bring the excavator or loader, the trucks and bins, and a crew to load it all. While the machine is on site, it can also do other jobs around the property: clearing, tidying up yards, digging or moving material. Ask us when you book.</p>
<p style="{P}">For ongoing work, a <a href="#pricing">permanent bin</a> on the farm is much cheaper than one-off bins: no set pickups, just give us a few days' notice and we fit it into our regular runs.</p>
<p style="{P}">Machinery or sheds to move rather than scrap? We also run drop deck floats. See <a href="#transport">machinery &amp; large item transport</a>.</p>
<h2 style="{H2}">Every load tracked</h2>
<p style="{P}">You get weighbridge dockets and a record of where everything went: scrap to the recycler, rubbish to landfill. Handy for your records, your accountant or a business's environmental reporting. See <a href="#tracking">waste tracking</a>.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</section>'''
PAGES.append('farm-commercial-clean-ups')

# ---------- deceased-estate-clean-outs ----------
mains['deceased-estate-clean-outs'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">DECEASED ESTATE &amp; PRE-SALE CLEAN-OUTS</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Clearing a loved one's home, or getting a property ready for sale? We can take care of it.</h1>
<p style="margin: 16px 0 0 0; font-size: 20px">We've cleared many homes for families, executors and solicitors over the years. We handle the whole clean-out with care, keep anything personal aside for the family, and leave the property ready to list.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<h2 style="{H2}">How we help</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Full house, shed and yard clean-outs, done by our own crew</li>
<li>Personal papers, photos and anything that looks valuable set aside for the family, as you direct</li>
<li>Good furniture and household items passed on to locals through our <a href="#too-good-to-tip">Too Good to Tip Giveaways</a>, or to charity, instead of landfill</li>
<li>Cleaning once the house is empty, plus a garden and yard tidy-up</li>
<li>Bins, trucks and machinery for big properties and farms</li>
</ul>
<p style="{P}">Family interstate? We can work with the executor, solicitor or real estate agent, send photo updates as we go, and hand the keys back when we're done.</p>
<h2 style="{H2}">Selling the property? Pay from the settlement</h2>
<p style="{P}">If the property is being sold, you don't need to find the money up front. We can do the clean-out now and be <strong>paid from the sale at settlement</strong>: our invoice goes to the conveyancer or solicitor with the settlement figures. This needs a short written agreement signed by the executor or owner before we start. Just ask when you call.</p>
<p style="{P}">This works for any home being cleared for sale, not just deceased estates.</p>
<h2 style="{H2}">For solicitors, executors and real estate agents</h2>
<p style="{P}">One local contractor for the whole job: the clean-out, the rubbish, the cleaning and the yard. Every load is weighed and you get the dockets and an itemised invoice for the estate's records. Call Al on <a href="tel:0408632007">0408 632 007</a> or email <a href="mailto:bookings@snowyskips.com.au">bookings@snowyskips.com.au</a>.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</section>'''
PAGES.append('deceased-estate-clean-outs')

# ---------- concrete-removal ----------
mains['concrete-removal'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">CONCRETE REMOVAL &amp; DISPOSAL</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Concrete removal and disposal: we cut it, break it, load it and cart it away.</h1>
<p style="margin: 16px 0 0 0; font-size: 20px">Old driveways, paths, slabs, footings and brick rubble. Concrete removal is one of our specialties, for builders, commercial sites, councils and homeowners right across the Snowy Monaro.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<div style="display: flex; flex-wrap: wrap; gap: 16px; margin-top: 28px"><figure style="flex: 1 1 240px; min-width: 0; margin: 0"><img src="/img/concrete-saw.jpg" alt="Concrete saw cutting along a path next to a brick wall" style="width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 6px">Saw-cutting a clean edge</figcaption></figure><figure style="flex: 1 1 240px; min-width: 0; margin: 0"><img src="/img/concrete-rubble-bin.jpg" alt="Broken concrete loaded in a Snowy Skips bin" style="width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 6px">Broken concrete, kept separate</figcaption></figure><figure style="flex: 1 1 240px; min-width: 0; margin: 0"><img src="/img/bricks-bin.jpg" alt="Old bricks loaded level in a galvanised skip bin" style="width: 100%; aspect-ratio: 4 / 3; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 6px">Bricks loaded level for the road</figcaption></figure></div>
<h2 style="{H2}">What we remove</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Driveways, footpaths and paved areas</li>
<li>Concrete slabs, including old shed and garage slabs</li>
<li>Footings, piers, kerbs and old retaining walls</li>
<li>Brick rubble, pavers and blocks</li>
<li>Concrete and brick waste from building and renovation jobs</li>
</ul>
<h2 style="{H2}">How we do it</h2>
<p style="{P}">We saw-cut a clean, straight edge so the concrete that's staying isn't damaged, then break it out with jackhammers and breakers, or with our machines on bigger jobs. Our crew loads it straight into our trucks or bins and carts it away. Small job or large commercial site, you get one crew with the saws, breakers, machines and trucks.</p>
<h2 style="{H2}">Disposal done right, and cheaper</h2>
<p style="{P}">We keep concrete and bricks separate from general rubbish, because clean concrete and bricks are charged at a much cheaper landfill rate than mixed building waste. Every load is weighed on the landfill weighbridge and you get the dockets. See <a href="#landfill-costs">landfill fees</a> for real loads we've weighed.</p>
<h2 style="{H2}">Doing it yourself? Hire a bin, but watch the weight</h2>
<p style="{P}">Concrete, bricks and rubble are extremely heavy. A bin can be over the legal weight long before it looks full, so ask us for a smaller bin and a fill mark inside it showing how high you can load. Keep concrete and bricks out of your general rubbish bin to save on the landfill fee.</p>
<h2 style="{H2}">Pricing</h2>
<p style="{P}">Concrete removal is priced on the job: how much there is, how thick it is, whether it's reinforced, and how easy it is to get to. Send us a few photos and rough measurements and we'll give you a price.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</section>'''
PAGES.append('concrete-removal')

# ---------- Single item pickup ----------
mains['single-item-pickup'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">SINGLE ITEM PICKUPS</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Just one fridge, mattress or couch to go? We'll pick it up.</h1>
<p style="margin: 16px 0 0 0; font-size: 20px">You don't need a whole skip bin for one or two bulky items. Our trucks run right across the Snowy Monaro every week, so we can call in, load it and take it to the landfill for you.</p>
<p style="margin: 16px 0 0 0; font-size: 22px"><strong>Generally $49 plus landfill</strong> for a single item when our trucks are in your area.</p>
</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<figure style="margin: 8px 0 32px 0"><img src="/img/single-item-pickup.jpg" alt="Fridge, couch, drawers and a storage tub loaded on the Snowy Skips truck in a driveway" style="width: 100%; max-height: 520px; object-fit: cover; border-radius: 10px; display: block"><figcaption style="font-size: 15px; color: #555555; margin-top: 8px">A few household items picked up from a driveway: fridge, couch and drawers.</figcaption></figure>
<h2 style="{H2}">What we pick up</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Fridges and freezers</li>
<li>Mattresses and bed bases</li>
<li>Couches, armchairs and other furniture</li>
<li>Desks, tables, cabinets and wardrobes</li>
<li>Washing machines, dryers and other whitegoods</li>
<li>Any other bulky item that's too big for the car or the wheelie bin</li>
</ul>
<p style="{P}">One item, two items or a small load: just tell us what's going.</p>
<h2 style="{H2}">Thinking of hiring a trailer?</h2>
<p style="{P}">Before you pay for trailer hire or trailer rental, give us a call. If the fridge, couch or mattress won't fit in your trailer, or you'd rather not hire one, load it and drive it to the tip yourself, we'll come and get it. It's quick and painless: we pick it up from your place and take it away, or move it from one place to another for you.</p>
<p style="{P}">Bigger or heavier things to move, like machinery, site sheds or containers? We also run drop deck floats with ramps. See <a href="#transport">machinery &amp; large item transport</a>.</p>
<h2 style="{H2}">What it costs</h2>
<p style="{P}">If our trucks are already in your area, a single item pickup is <strong>generally $49 plus the landfill fee</strong> for the item. Fridges, mattresses, tyres and similar items have their own council landfill fees, which we pass on at cost.</p>
<p style="{P}">If you're further out, the price goes up on a sliding scale depending on the distance and where our trucks are running that week. Call us and we'll give you a price before we come.</p>
<h2 style="{H2}">How it works</h2>
<ol style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Call us on <a href="tel:0408632007">0408 632 007</a> or send a photo of the item and where it is.</li>
<li>We give you a price and fit the pickup in when our trucks are running your way.</li>
<li>We load it, take it to the landfill and dispose of it properly.</li>
</ol>
<p style="{P}">Got more than a few items? A <a href="/skip-bins/">skip bin</a> or our <a href="/labour-hire/">clean-out crew</a> may work out cheaper.</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>
</section>'''
PAGES.append('single-item-pickup')

# ---------- Free to a good home ----------
import json as _json, os as _os, shutil as _sh, datetime as _dt
for _f in _os.listdir('/home/claude/site/extra_img'): _sh.copy('/home/claude/site/extra_img/'+_f, OUT+'img/'+_f)
_items = _json.load(open('/home/claude/site/free_items.json'))
_os.makedirs(OUT + 'img/free', exist_ok=True)
def _fmt(d): return _dt.date.fromisoformat(d).strftime('%-d %b %Y')
_cards = ''
for it in _items:
    if it.get('gone'): continue
    _sh.copy('/home/claude/site/free_items/' + it['photo'], OUT + 'img/free/' + it['photo'])
    _cards += f'''<article data-listed="{it['listed']}" style="border: 1px solid #e4e0d8; border-radius: 10px; overflow: hidden; background: #fff"><img src="/img/free/{it['photo']}" alt="{it['name']}" loading="lazy" style="width: 100%; aspect-ratio: 4 / 3; object-fit: cover; display: block"><div style="padding: 14px 16px"><h3 style="{HS}; font-size: 19px; margin: 0">{it['name']}</h3><p style="margin: 6px 0 0 0; font-size: 16px">{it.get('desc','')}</p><p style="margin: 8px 0 0 0; font-size: 14px; color: #666">Listed {_fmt(it['listed'])}</p></div></article>'''
if not _cards:
    _cards = '<p style="font-size: 18px; margin: 0; grid-column: 1 / -1; background: #F5F2EC; border-radius: 10px; padding: 18px 20px">Nothing on the list right now. Check back soon, or follow us on Facebook for new items.</p>'
mains['too-good-to-tip'] = f'''<section style="background: #F5F2EC">
<div style="max-width: 1100px; margin: 0 auto; padding: 56px 24px">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">OUR COMMUNITY REUSE PROGRAM</div>
<h1 style="{HS}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">Too Good to Tip Giveaways</h1>
<p style="margin: 8px 0 0 0; font-size: 22px; font-weight: 700; color: #4F7230">Free items for locals who need them</p>
<p style="margin: 16px 0 0 0; font-size: 20px; max-width: 820px">Got something in good condition that someone else could use? <strong>Just leave it on top of your bin load</strong> and we'll assess whether it can be given away. Items that can be reused go free to locals who need them, can reuse them, or are doing it tough. It keeps good things out of landfill and can lower your landfill fees.</p>
<p style="margin: 12px 0 0 0; font-size: 18px; max-width: 820px"><strong>We never go through the contents of your bin</strong>, or through private documents, photos or personal belongings. We only look at items you choose to leave on top for reuse. If everything must go straight to landfill, just tell us when you book.</p>
</div>
</section>
<section style="max-width: 1100px; margin: 0 auto; padding: 32px 24px 8px 24px">
<h2 style="{H2}; margin-top: 0">Available now</h2>
<div style="display: grid; grid-template-columns: repeat(auto-fill, minmax(240px, 1fr)); gap: 20px; margin-top: 18px">{_cards}</div>
</section>
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<h2 style="{H2}">How it works</h2>
<ol style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Call or message us on <a href="tel:0408632007">0408 632 007</a> with the item you'd like, and tell us a little about what you need it for.</li>
<li>We'll arrange a time for you to collect it from our depot. Please don't turn up unannounced.</li>
<li>Bring a vehicle and enough help to load it safely, or ask us about delivery: from $49 when our trucks are in your area, depending on the size of the item.</li>
</ol>
<h2 style="{H2}">The rules</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li><strong>For people who'll use them, not resell them.</strong> Anyone found reselling items they got from us will be banned from taking free items in future.</li>
<li><strong>Items are listed for about 4 weeks.</strong> Anything not collected by then goes to the council's reuse centre or is recycled or disposed of properly.</li>
<li>One or two items per household at a time, so more people get a go.</li>
<li>First in, best dressed. We may hold an item for someone in genuine need.</li>
</ul>
<h2 style="{H2}">What we don't give away</h2>
<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">
<li>Gas appliances and anything that runs on fuel</li>
<li>Cots, car seats, prams, high chairs and helmets</li>
<li>Recalled or damaged items</li>
<li>Used mattresses (we only give away mattresses that are brand new)</li>
<li>Soft furnishings that aren't clean and in good condition</li>
<li>Anything that may contain asbestos</li>
<li>Electrical items, unless clearly marked as tested, or as "untested, for parts only"</li>
</ul>
<div style="margin-top: 32px; border-top: 2px solid #e4e0d8; padding-top: 18px; font-size: 15px; color: #555; line-height: 1.6">
<strong>Disclaimer.</strong> All items are second-hand and given away free, as is, with no warranty of any kind. We haven't inspected or tested them unless we say so. Electrical items are untested unless clearly marked otherwise: have them tested and tagged by a licensed electrician before you use them. You're responsible for checking an item is safe and suitable before you take it or use it, and for loading and transporting it safely. Snowy Skips and McKimm Civil Pty Ltd accept no liability for any loss, damage or injury arising from items taken, to the extent the law allows. We may refuse any request.
</div>
</section>'''
PAGES.append('too-good-to-tip')

META = {
 'home': (None, None),
 'skip-bins': ('Skip Bin Hire Snowy Monaro | 1.5 to 12 m³ Bins | Snowy Skips',
   'Skip bin hire across the Snowy Monaro, from 1.5 m³ to 12 m³, plus a 20 m³+ semi tipper. Fill it yourself or we load it for you. Delivered within 24 hours\' notice from Berridale.'),
 'pricing': ('Skip Bin Prices Cooma, Jindabyne, Berridale & Snowy Monaro | Snowy Skips',
   'Indicative skip bin prices by area: Cooma from $330, Berridale and Jindabyne from $440 inc GST for up to 7 days, plus landfill at cost. 24-hour hotshot prices, extra charges and price match.'),
 'landfill-costs': ('Landfill Costs for Skip Bins | Real Loads Weighed | Snowy Skips',
   'What does it cost to tip a skip bin in the Snowy Monaro? Real Snowy Skips loads weighed on the landfill weighbridge, with what each one cost at council rates.'),
 'equipment-hire': ('Equipment Hire & Site Establishment Snowy Monaro | Snowy Skips',
   'Equipment hire in the Snowy Monaro: small plant, tree chipper, EWP, compressors, generators and machines with an operator, plus site sheds, toilets, temporary fencing and erosion controls.'),
 'labour-hire': ('Labour Hire, Rubbish Removal & Property Clean-Outs | Snowy Skips',
   'Don\'t want to load the bin? Our crew and machines load, separate and cart your rubbish to the landfill. Property clean-outs, estates and site clean-ups across the Snowy Monaro.'),
 'about': ('About & Contact | Locally Owned in Berridale | Snowy Skips',
   'Snowy Skips is a locally owned skip bin, equipment and labour hire business at 8–10 Basalt Street, Berridale NSW. Call 0408 632 007 or email bookings@snowyskips.com.au.'),
 'skip-bin-guide': ('Skip Bin Guide | What Can Go in a Skip Bin | Snowy Skips',
   'What can and can\'t go in a skip bin, how to load it, how to avoid extra charges, and our hire conditions. The Snowy Skips Skip Bin Guide.'),
 'too-good-to-tip': ('Too Good to Tip Giveaways | Free Reused Items | Snowy Skips',
   'Good-condition furniture, tools and materials we\'ve saved from landfill, free for Snowy Monaro locals who need them. See what\'s available and how to collect.'),
 'concrete-removal': ('Concrete Removal & Disposal | Driveways, Slabs & Footings | Snowy Monaro | Snowy Skips',
   'Concrete removal and disposal across the Snowy Monaro: driveways, paths, slabs, footings and brick rubble. Saw-cut, broken out, loaded and carted away, with weighbridge dockets.'),
 'farm-commercial-clean-ups': ('Farm & Commercial Clean-Ups | Scrap Steel, Machinery & Batteries | Snowy Skips',
   'Large farm and commercial clean-ups across the Snowy Monaro: old machinery, sheds, scrap steel and car batteries. Bins, machines and crew, with every load tracked.'),
 'deceased-estate-clean-outs': ('Deceased Estate & Pre-Sale Clean-Outs | Snowy Monaro | Snowy Skips',
   'Respectful deceased estate and pre-sale house clean-outs across the Snowy Monaro. Personal items kept aside, cleaning and yard tidy, and the option to pay from the sale at settlement.'),
 'insurance-accident-clean-ups': ('Insurance & Accident Clean-Ups | Storm, Fire & Flood | Snowy Monaro | Snowy Skips',
   'Storm, fire, flood or accident damage in the Snowy Monaro? Snowy Skips clears the site with bins, machinery and labour, with photos and weighbridge dockets for your insurer.'),
 'single-item-pickup': ('Single Item Pickup & Bulky Rubbish Removal | Snowy Monaro | Snowy Skips',
   'Fridge, mattress, couch or desk to go? No need for trailer hire: Snowy Skips picks up single bulky items across the Snowy Monaro, generally $49 plus landfill when our trucks are in your area.'),
 'skip-bin-permits': ('Do I Need a Council Permit for a Skip Bin? | Snowy Monaro | Snowy Skips',
   'Do you need a council permit for a skip bin in Cooma, Jindabyne or Berridale? On your property, generally no. On the road or footpath, yes. Here is how it works, and how we can apply for you.'),
 'faq': ('Skip Bin FAQs | Sizes, Prices, Permits & Landfill | Snowy Skips',
   'Answers to common skip bin questions: sizes, prices, landfill fees, hire length, permits, what can go in, loading and soil/VENM, across the Snowy Monaro.'),
}

# anchor -> page
anchor_page = {}
for pid in PAGES:
    for a in re.findall(r' id="([^"]+)"', mains[pid]):
        anchor_page.setdefault(a, pid)
path = lambda pid: '/' if pid == 'home' else f'/{pid}/'
def target(x, cur=None):
    if x in PAGES: return path(x)
    if x in anchor_page:
        p = anchor_page[x]
        return f'#{x}' if p == cur else f'{path(p)}#{x}'
    return path('home')
def relink(s, cur=None):
    s = re.sub(r'href="/?#([^"]*)"', lambda m: f'href="{target(m.group(1) or "home", cur)}"', s)
    return s.replace('src="img/', 'src="/img/').replace('href="img/', 'href="/img/')

SCRIPT = '''<script>
(function(){
  document.addEventListener('click',function(e){document.querySelectorAll('details.nav-guides').forEach(function(d){if(!d.contains(e.target))d.open=false;});});
%s})();
</script>''' % forms_js
REDIRECT = '<script>(function(){var m={%s};var h=location.hash.slice(1);if(m[h])location.replace(m[h]);})();</script>' % ','.join(
    f'"{k}":"{target(k)}"' for k in sorted(set(PAGES) | set(anchor_page)) if k != 'home' and (k in PAGES or anchor_page.get(k) != 'home'))

base_head = head.replace('<link rel="icon" href="img/', '<link rel="icon" href="/img/')
base_head = base_head.replace('</style>', '[id]{scroll-margin-top:150px}\n</style>', 1)
ld_home = re.search(r'<script type="application/ld\+json">.*?</script>\n', base_head).group(0)
urls = []
for pid in PAGES:
    hd = base_head
    if pid != 'home':
        t, desc = META[pid]
        hd = re.sub(r'<title>.*?</title>', f'<title>{H_.escape(t, quote=False)}</title>', hd)
        hd = re.sub(r'<meta name="description" content="[^"]*">', f'<meta name="description" content="{H_.escape(desc)}">', hd)
        hd = hd.replace('<link rel="canonical" href="https://snowyskips.com.au/">', f'<link rel="canonical" href="{SITE}{path(pid)}">')
        hd = hd.replace(ld_home, '<script type="application/ld+json">' + json.dumps(faq_ld) + '</script>\n' if pid == 'faq' else '')
    else:
        hd = hd.replace('</head>', REDIRECT + '\n</head>')
    hdr = relink(header, pid).replace(f'href="{path(pid)}" style="color: #1f1f1f', f'class="current" href="{path(pid)}" style="color: #1f1f1f') if pid != 'home' else relink(header, pid)
    body = f'<body>\n{hdr}\n<main class="page active" id="page-{pid}">\n{relink(mains[pid], pid)}\n</main>\n{relink(footer, pid)}\n{SCRIPT}\n</body>\n</html>\n'
    fn = OUT + ('index.html' if pid == 'home' else f'{pid}/index.html')
    os.makedirs(os.path.dirname(fn), exist_ok=True)
    open(fn, 'w').write(hd + body)
    urls.append(SITE + path(pid))

# town pages: rewrite /#x links
towns = sorted(glob.glob(OUT + 'skip-bin-hire-*/index.html'))
for fn in towns:
    s = open(fn).read()
    s = s.replace('Snowy Skips Skip Bin Guide</a>', 'Snowy Skips Skip Bin Guide</a><a href="/faq/" style="display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none">Skip bin FAQs</a><a href="/skip-bin-permits/" style="display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none">Council permits for skip bins</a><a href="/too-good-to-tip/" style="display: block; padding: 8px 16px; color: #1f1f1f; text-decoration: none">Too Good to Tip Giveaways</a>', 1)
    s = s.replace(_LH.replace('href="#', 'href="/#'), _labour_menu('/'), 1)
    s = re.sub(r'href="/#([^"]*)"', lambda m: f'href="{target(m.group(1) or "home")}"', s)
    open(fn, 'w').write(s)
    urls.append(SITE + '/' + os.path.relpath(os.path.dirname(fn), OUT) + '/')

open(OUT + 'sitemap.xml', 'w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    + ''.join(f'<url><loc>{u}</loc></url>\n' for u in urls) + '</urlset>\n')
# sanity
left = []
for fn in glob.glob(OUT + '**/index.html', recursive=True):
    s = open(fn).read()
    left += [(fn, m) for m in re.findall(r'href="(/?#[^"]*)"', s) if not m.startswith('#')]
    assert 'src="img/' not in s, fn
print(len(PAGES), 'section pages,', len(towns), 'town pages,', len(urls), 'urls; odd links:', left[:5])

# old address for the giveaway page
_os.makedirs(OUT + 'free-items', exist_ok=True)
open(OUT + 'free-items/index.html','w').write('<!doctype html><meta charset="utf-8"><title>Too Good to Tip Giveaways</title><link rel="canonical" href="https://snowyskips.com.au/too-good-to-tip/"><meta http-equiv="refresh" content="0; url=/too-good-to-tip/"><a href="/too-good-to-tip/">Too Good to Tip Giveaways</a>')
