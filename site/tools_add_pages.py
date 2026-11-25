# One-off edit script (25 Nov 2026): farm & commercial page, deceased estate page,
# trailer hire text on single item page, transport section on Equipment page.
p = 'project/Equipment.dc.html'; s = open(p).read()
a = '<p style="margin: 40px 0 0 0; font-size: 17px; background: #F5F2EC; border-radius: 10px; padding: 16px 18px"><strong style="color: #52372A">Excavated soil to move?</strong>'
assert s.count(a) == 1
sec = ('<div id="transport" style="margin-top: 48px"><h3 style="font-family: \'Sora\', sans-serif; font-weight: 800; font-size: 32px; color: #52372A; margin: 0">Machinery &amp; large item transport</h3>'
       '<p style="margin: 10px 0 0 0; font-size: 18px; max-width: 820px">Need a machine, container or something big moved? We run drop deck floats with ramps for machinery, plant, site sheds, containers and other large items, and our trucks for smaller loads. We carry transit insurance on the load, up to $370,000, so your gear is covered while it\'s on our trucks.</p>'
       '<ul style="margin: 12px 0 0 0; padding-left: 20px; font-size: 17px; max-width: 820px"><li>Excavators, loaders, tractors and other machinery</li><li>Site sheds, shipping containers and water tanks</li><li>Farm equipment, building materials and large one-off items</li></ul>'
       '<p style="margin: 10px 0 0 0; font-size: 16px; color: #555555">Tell us what it is, roughly how big and heavy, and where it\'s going, and we\'ll give you a price. Smaller items? See <a href="#single-item-pickup">single item pickups</a>.</p></div>\n')
s = s.replace(a, sec + a, 1); open(p, 'w').write(s)

p = 'gen_pages.py'; s = open(p).read()
a = '''f'<a href="{pre}#single-item-pickup" style="{a}">Single item pickups</a></div></details>')'''
b = '''f'<a href="{pre}#farm-commercial-clean-ups" style="{a}">Farm &amp; commercial clean-ups</a>'
            f'<a href="{pre}#deceased-estate-clean-outs" style="{a}">Deceased estate &amp; pre-sale clean-outs</a>'
            f'<a href="{pre}#single-item-pickup" style="{a}">Single item pickups</a></div></details>')'''
assert s.count(a) == 1; s = s.replace(a, b, 1)
a = """footer = footer.replace(_FL, _FL + '<br><a href="#insurance-accident-clean-ups" style="color: #e8e2d9">Insurance &amp; accident clean-ups</a>', 1)"""
b = """footer = footer.replace(_FL, _FL + '<br><a href="#insurance-accident-clean-ups" style="color: #e8e2d9">Insurance &amp; accident clean-ups</a><br><a href="#farm-commercial-clean-ups" style="color: #e8e2d9">Farm &amp; commercial clean-ups</a><br><a href="#deceased-estate-clean-outs" style="color: #e8e2d9">Deceased estate clean-outs</a>', 1)"""
assert s.count(a) == 1; s = s.replace(a, b, 1)

BTN = '<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 28px"><a href="tel:0408632007" style="background: #4F7230; color: #fff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a><a href="#contact" style="background: #fff; color: #52372A; text-decoration: none; font-weight: 700; padding: 12px 20px; border-radius: 8px; border: 2px solid #52372A">Get a quote</a></div>'

def hero(kicker, h1, lead):
    return ('<section style="background: #F5F2EC">\n<div style="max-width: 860px; margin: 0 auto; padding: 56px 24px">\n'
            f'<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">{kicker}</div>\n'
            f'<h1 style="{{HS}}; font-size: 42px; line-height: 1.1; margin: 10px 0 0 0">{h1}</h1>\n'
            f'<p style="margin: 16px 0 0 0; font-size: 20px">{lead}</p>\n{BTN}\n</div>\n</section>')

UL = '<ul style="margin: 14px 0 0 0; padding-left: 22px; font-size: 18px; line-height: 1.7">'
farm = hero('FARM &amp; COMMERCIAL CLEAN-UPS',
            'Big clean-up on the farm or at the business? We bring the bins, machines and crew.',
            'Old machinery, sheds, wire, scrap steel, car batteries and years of built-up rubbish. We clear large farm and commercial sites right across the Snowy Monaro, Upper Murray and far East Gippsland.') + f'''
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<h2 style="{{H2}}">What we clear</h2>
{UL}
<li>Old machinery, vehicles, implements and heavy scrap steel</li>
<li>Fencing wire, posts, old yards and collapsed or unwanted sheds</li>
<li>Large numbers of car and truck batteries</li>
<li>General rubbish, timber, tyres and green waste from around the property</li>
<li>Commercial sites: warehouse and shop clean-outs, end-of-lease strip-outs and yard clean-ups</li>
</ul>
<h2 style="{{H2}}">Scrap steel and batteries have value</h2>
<p style="{{P}}">Heavy scrap steel and batteries go to authorised scrap metal recyclers in the cities, not landfill. Because the scrap is worth something, on <strong>large jobs</strong> the bins and pickup <strong>may be free or reduced</strong>, depending on how much there is and where the property is. Give us a call and we'll take a look. (This is for big clean-ups only, not small loads of steel.)</p>
<p style="{{P}}">Batteries are packed to meet the legal requirements for transport and taken off site separately. They never go in a skip bin.</p>
<h2 style="{{H2}}">Machines, crew and bins on site</h2>
<p style="{{P}}">We bring the excavator or loader, the trucks and bins, and a crew to load it all. While the machine is on site, it can also do other jobs around the property: clearing, tidying up yards, digging or moving material. Ask us when you book.</p>
<p style="{{P}}">For ongoing work, a <a href="#pricing">permanent bin</a> on the farm is much cheaper than one-off bins: no set pickups, just give us a few days' notice and we fit it into our regular runs.</p>
<p style="{{P}}">Machinery or sheds to move rather than scrap? We also run drop deck floats. See <a href="#transport">machinery &amp; large item transport</a>.</p>
<h2 style="{{H2}}">Every load tracked</h2>
<p style="{{P}}">You get weighbridge dockets and a record of where everything went: scrap to the recycler, rubbish to landfill. Handy for your records, your accountant or a business's environmental reporting. See <a href="#tracking">waste tracking</a>.</p>
{BTN}
</section>'''

estate = hero('DECEASED ESTATE &amp; PRE-SALE CLEAN-OUTS',
              "Clearing a loved one's home, or getting a property ready for sale? We can take care of it.",
              "We've cleared many homes for families, executors and solicitors over the years. We handle the whole clean-out with care, keep anything personal aside for the family, and leave the property ready to list.") + f'''
<section style="max-width: 860px; margin: 0 auto; padding: 8px 24px 56px 24px">
<h2 style="{{H2}}">How we help</h2>
{UL}
<li>Full house, shed and yard clean-outs, done by our own crew</li>
<li>Personal papers, photos and anything that looks valuable set aside for the family, as you direct</li>
<li>Good furniture and household items passed on to locals through our <a href="#too-good-to-tip">Too Good to Tip Giveaways</a>, or to charity, instead of landfill</li>
<li>Cleaning once the house is empty, plus a garden and yard tidy-up</li>
<li>Bins, trucks and machinery for big properties and farms</li>
</ul>
<p style="{{P}}">Family interstate? We can work with the executor, solicitor or real estate agent, send photo updates as we go, and hand the keys back when we're done.</p>
<h2 style="{{H2}}">Selling the property? Pay from the settlement</h2>
<p style="{{P}}">If the property is being sold, you don't need to find the money up front. We can do the clean-out now and be <strong>paid from the sale at settlement</strong>: our invoice goes to the conveyancer or solicitor with the settlement figures. This needs a short written agreement signed by the executor or owner before we start. Just ask when you call.</p>
<p style="{{P}}">This works for any home being cleared for sale, not just deceased estates.</p>
<h2 style="{{H2}}">For solicitors, executors and real estate agents</h2>
<p style="{{P}}">One local contractor for the whole job: the clean-out, the rubbish, the cleaning and the yard. Every load is weighed and you get the dockets and an itemised invoice for the estate's records. Call Al on <a href="tel:0408632007">0408 632 007</a> or email <a href="mailto:bookings@snowyskips.com.au">bookings@snowyskips.com.au</a>.</p>
{BTN}
</section>'''

def block(pid, html):
    assert "'''" not in html
    return f"# ---------- {pid} ----------\nmains['{pid}'] = f'''{html}'''\nPAGES.append('{pid}')\n\n"
a2 = "# ---------- Single item pickup ----------"
assert s.count(a2) == 1
s = s.replace(a2, block('farm-commercial-clean-ups', farm) + block('deceased-estate-clean-outs', estate) + a2, 1)

a3 = " 'insurance-accident-clean-ups': ("
assert s.count(a3) == 1
meta = (" 'farm-commercial-clean-ups': ('Farm & Commercial Clean-Ups | Scrap Steel, Machinery & Batteries | Snowy Skips',\n"
        "   'Large farm and commercial clean-ups across the Snowy Monaro: old machinery, sheds, scrap steel and car batteries. Bins, machines and crew, with every load tracked.'),\n"
        " 'deceased-estate-clean-outs': ('Deceased Estate & Pre-Sale Clean-Outs | Snowy Monaro | Snowy Skips',\n"
        "   'Respectful deceased estate and pre-sale house clean-outs across the Snowy Monaro. Personal items kept aside, cleaning and yard tidy, and the option to pay from the sale at settlement.'),\n")
s = s.replace(a3, meta + a3, 1)

a4 = '<h2 style="{H2}">What it costs</h2>'
assert s.count(a4) == 1
b4 = ('<h2 style="{H2}">Thinking of hiring a trailer?</h2>\n'
      '<p style="{P}">Before you pay for trailer hire or trailer rental, give us a call. If the fridge, couch or mattress won\'t fit in your trailer, or you\'d rather not hire one, load it and drive it to the tip yourself, we\'ll come and get it. It\'s quick and painless: we pick it up from your place and take it away, or move it from one place to another for you.</p>\n'
      '<p style="{P}">Bigger or heavier things to move, like machinery, site sheds or containers? We also run drop deck floats with ramps. See <a href="#transport">machinery &amp; large item transport</a>.</p>\n')
s = s.replace(a4, b4 + a4, 1)
old_meta = "'Fridge, mattress, couch or desk to go? Snowy Skips picks up"
assert s.count(old_meta) == 1
s = s.replace(old_meta, "'Fridge, mattress, couch or desk to go? No need for trailer hire: Snowy Skips picks up", 1)
open(p, 'w').write(s)
print('ok')
