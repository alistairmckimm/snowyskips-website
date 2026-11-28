import json
HEAD = '''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>{title}</title>
<script src="./support.js"></script>
</head>
<body>
<x-dc>
<helmet>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@500;600;700;800&amp;family=Source+Sans+3:wght@400;600;700&amp;display=swap" rel="stylesheet">
<style>
body{{margin:0;background:#ffffff}}
a{{color:#3d5a24}}a:hover{{color:#52372A}}
</style>
</helmet>
<div id="{id}" style="font-family: 'Source Sans 3', sans-serif; color: #1f1f1f; background: #ffffff; font-size: 18px; line-height: 1.5">
'''
FOOT = '''</div>
</x-dc>
<script type="text/x-dc" data-dc-script data-props='{{"$preview":{{"width":1440,"height":{h}}}}}'>
class Component extends DCLogic {{
renderVals() {{ return {{}}; }}
}}
</script>
</body>
</html>
'''
def H2(t):
    return f'''<h3 style="font-family: 'Sora', sans-serif; font-weight: 800; font-size: 32px; color: #52372A; margin: 0">{t}</h3>'''
def PH(t, h=300):
    return f'<div style="flex: 1 1 440px; min-width: 0; height: {h}px; background: #d9d6cf; border-radius: 10px; display: flex; align-items: center; justify-content: center; text-align: center; padding: 24px; box-sizing: border-box; color: #4a4a4a; font-weight: 600">[PHOTO: {t}]</div>'
def hero(kicker, title, sub, btns, img):
    b = ''
    for i, (t, h) in enumerate(btns):
        if i == 0:
            b += f'<a href="{h}" style="background: #4F7230; color: #ffffff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">{t}</a>'
        else:
            b += f'<a href="{h}" style="background: #ffffff; color: #52372A; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px; border: 2px solid #52372A">{t}</a>'
    return f'''<section style="background: #F5F2EC">
<div style="max-width: 1240px; margin: 0 auto; padding: 64px 24px; display: flex; flex-wrap: wrap; gap: 40px; align-items: center">
<div style="flex: 1 1 480px; min-width: 0">
<div style="font-weight: 700; letter-spacing: 2px; font-size: 14px; color: #4F7230">{kicker}</div>
<h2 style="font-family: 'Sora', sans-serif; font-weight: 800; font-size: 44px; line-height: 1.1; color: #52372A; margin: 10px 0 0 0">{title}</h2>
<p style="margin: 14px 0 0 0; font-size: 20px">{sub}</p>
<div style="display: flex; flex-wrap: wrap; gap: 12px; margin-top: 24px">{b}</div>
</div>
{img}
</div>
</section>
'''
def CTA(t, s):
    return f'''<section style="background: #52372A; color: #ffffff">
<div style="max-width: 1240px; margin: 0 auto; padding: 48px 24px; display: flex; flex-wrap: wrap; gap: 24px; align-items: center; justify-content: space-between">
<div><h3 style="font-family: 'Sora', sans-serif; font-weight: 800; font-size: 32px; margin: 0">{t}</h3><p style="margin: 6px 0 0 0; font-size: 18px; color: #EADFD2">{s}</p></div>
<div style="display: flex; flex-wrap: wrap; gap: 12px">
<a href="#contact" style="background: #4F7230; color: #ffffff; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Request a quote</a>
<a href="tel:0408632007" style="background: #ffffff; color: #52372A; text-decoration: none; font-weight: 700; padding: 14px 22px; border-radius: 8px">Call 0408 632 007</a>
</div>
</div>
</section>
'''
def card(title, items, note='', accent='#4F7230'):
    li = ''.join(f'<li>{i}</li>' for i in items)
    n = f'<p style="margin: 10px 0 0 0; font-size: 15px; color: #555555">{note}</p>' if note else ''
    return f'''<div style="border-top: 6px solid {accent}; background: #F5F2EC; border-radius: 10px; padding: 22px">
<h4 style="font-family: 'Sora', sans-serif; font-weight: 700; font-size: 20px; color: #52372A; margin: 0">{title}</h4>
<ul style="margin: 10px 0 0 0; padding-left: 20px; font-size: 17px">{li}</ul>{n}
</div>
'''
def GRID(inner, mn=300):
    return f'<div style="display: grid; grid-template-columns: repeat(auto-fit, minmax({mn}px, 1fr)); gap: 20px; margin-top: 24px">\n{inner}</div>\n'
def SEC(inner, pad='56px 24px'):
    return f'<section style="max-width: 1240px; margin: 0 auto; padding: {pad}">\n{inner}</section>\n'
IMG = lambda b, alt, h=380: f'<img src="/_blob/{b}" alt="{alt}" style="flex: 1 1 440px; min-width: 0; height: {h}px; object-fit: cover; border-radius: 10px; display: block">'

# Equipment
eq = HEAD.format(title='Snowy Skips — Equipment hire', id='equipment-hire')
eq += hero('EQUIPMENT HIRE', 'Small plant to hire, machines with an operator',
           "From jackhammers and water pumps to a 12-inch tree chipper — the gear you'd expect a civil contractor to own, ready to hire. Our bigger machines come with one of our experienced operators.",
           [('Request a quote', '#contact'), ('Call 0408 632 007', 'tel:0408632007')],
           IMG('073f0cf9e1ce3f3131300e783b648eec', 'Snowy Skips truck and excavator on a job'))
eq += SEC(H2('Two ways to hire') + GRID(
    card('Small plant — dry hire', ['Water pumps', 'Road saws and demolition saws', 'Jackhammers and breakers', 'Other small site gear', 'Tree chippers — up to 12-inch'], "Pick up, or we can deliver. Ask us what's available for your job.") +
    card('Earthmoving — wet hire only', ['Loaders', 'Excavators', 'Other earthmoving machines'], 'Our large machines are only hired with one of our operators. You get the machine and someone who knows how to run it safely.', '#52372A') +
    card('Portable site toilets', ['Delivered and set up on site by our truck', "Picked up when you're done"], 'Good for building sites, events and long jobs.', '#D98B4A')))
eq += SEC(f'''<div style="display: flex; flex-wrap: wrap; gap: 24px">
{IMG('195317894a951704f755526369aa8b47', 'Skip truck lifting a portable site toilet into place', 300)}
{PH('small plant — pumps, saws, jackhammers, chipper')}
</div>
<div style="margin-top: 28px; background: #EEF3E6; border-radius: 10px; padding: 20px 22px; font-size: 17px"><strong style="color: #52372A">Rates:</strong> hire rates depend on the gear, how long you need it and where it's going — call us or send a quote request and we'll give you a price.</div>
<p style="margin: 18px 0 0 0; font-size: 16px">Bigger job? Earthworks and civil construction by our sister company <a href="https://mckimmcivil.com.au">McKimm Civil</a>.</p>
''', '8px 24px 56px 24px')
eq += CTA('Need some gear on site?', "Tell us what you need and when — we'll sort it.")
eq += FOOT.format(h=2400)
open('project/Equipment.dc.html', 'w').write(eq)

# Labour
lb = HEAD.format(title='Snowy Skips — Labour hire', id='labour-hire')
lb += hero('LABOUR HIRE', 'Hands on site, when you need them',
           'From a hand loading your skip bin to trades assistants and concrete finishers — our crew can take the hard work off your hands.',
           [('Request a quote', '#contact'), ('Call 0408 632 007', 'tel:0408632007')], PH('crew loading a skip bin', 380))
lb += SEC(H2('What our crew can do') + GRID(
    card('Loading and clean-ups', ['Loading your skip bin', 'Site and yard clean-ups', 'Household and estate clear-outs', 'Rubbish removal with bin and machine'], 'Send us a few clear photos and we can generally quote the whole job — bin, crew and machine.') +
    card('General labour', ["Builders' labourers", 'Site preparation and tidy-ups', 'Digging, barrowing and moving materials', 'Short or long jobs'], '', '#52372A') +
    card('Specialist trades support', ['Plumbing trades assistants', 'Concrete finishers', 'Other skilled hands on request'], "Tell us what the job needs and we'll match the right person.", '#D98B4A')))
lb += SEC('''<div style="background: #EEF3E6; border-radius: 10px; padding: 20px 22px; font-size: 17px"><strong style="color: #52372A">Rates:</strong> labour hire is priced on the job — what you need done, how many people and for how long. Call us or send a quote request and we'll work it out with you.</div>
''', '0 24px 56px 24px')
lb += CTA('Need a hand on site?', "Tell us about the job and we'll put the right crew on it.")
lb += FOOT.format(h=2200)
open('project/Labour.dc.html', 'w').write(lb)

# About + contact
ab = HEAD.format(title='Snowy Skips — About and contact', id='about')
ab += hero('ABOUT US', 'Ten years of keeping the Snowy Mountains clean',
           "Snowy Skips is locally owned and operated in Berridale. For ten years we've been delivering skip bins, loading jobs and clearing sites right across the Snowy Monaro — from town blocks in Cooma to building sites in Jindabyne and the high country beyond.",
           [('Get in touch', '#contact')], IMG('320c2a81a137934be2026ab3c17e3243', 'Snowy Skips bin on the truck'))
stats = ''.join(f'''<div style="text-align: center; padding: 10px"><div style="font-family: 'Sora', sans-serif; font-weight: 800; font-size: 44px; color: #4F7230">{a}</div><div style="font-weight: 700; color: #52372A">{b}</div></div>''' for a, b in [('10 years', 'servicing the Snowy Monaro'), ('Every job', 'waste tracked, dockets supplied'), ('Local', 'owned and operated in Berridale')])
ab += SEC(GRID(stats, 220) + '''<div style="max-width: 860px; margin: 36px auto 0 auto; font-size: 19px">
<p style="margin: 0">We started Snowy Skips to give the region a skip bin service that turns up when it says it will and does the job properly. Ten years on, that hasn't changed. We know the roads, the landfills and the weather up here, and we know that a job on a steep Jindabyne block or at a resort in winter takes a bit more planning.</p>
<p style="margin: 16px 0 0 0">We're more than skip bins. Our own crew and machines can load anything for you, and we hire out the small plant you'd expect a civil contractor to own. Every load is tracked from collection to disposal, weighed at the landfill, and you get the docket — so you only pay for what you got rid of.</p>
<p style="margin: 16px 0 0 0">Snowy Skips is part of McKimm Civil Pty Ltd, and brings the same standard of safety, quality and care for the environment from our civil construction work to every bin we drop off.</p>
</div>
''', '56px 24px 40px 24px')
inp = 'display: block; width: 100%; box-sizing: border-box; margin-top: 4px; padding: 12px; border: 1px solid #cfc8bb; border-radius: 8px; font: inherit'
ab += f'''<section id="contact" style="background: #F5F2EC">
<div style="max-width: 1240px; margin: 0 auto; padding: 56px 24px; display: flex; flex-wrap: wrap; gap: 40px">
<div style="flex: 1 1 380px; min-width: 0">
{H2('Contact us')}
<p style="margin: 12px 0 0 0; font-size: 18px">Call, email or send us your job details and we'll get back to you.</p>
<div style="margin-top: 20px; font-size: 19px; line-height: 1.9">
<div><strong style="color: #52372A">Phone</strong> &nbsp;<a href="tel:0408632007" style="font-weight: 700">0408 632 007</a></div>
<div><strong style="color: #52372A">Email</strong> &nbsp;<a href="mailto:alistair@snowyskips.com.au">alistair@snowyskips.com.au</a></div>
<div><strong style="color: #52372A">Depot</strong> &nbsp;8–10 Basalt Street, Berridale NSW 2628</div>
<div><strong style="color: #52372A">Hours</strong> &nbsp;[business hours to confirm]</div>
</div>
<p style="margin: 18px 0 0 0; font-size: 15px; color: #555555">Snowy Skips is part of McKimm Civil Pty Ltd · ABN 15 650 293 780</p>
</div>
<form style="flex: 1 1 520px; min-width: 0; background: #ffffff; border-radius: 12px; padding: 26px; display: grid; gap: 14px">
<label style="font-weight: 700; color: #52372A">Name<input type="text" style="{inp}"></label>
<div style="display: grid; grid-template-columns: 1fr 1fr; gap: 14px">
<label style="font-weight: 700; color: #52372A">Phone<input type="tel" style="{inp}"></label>
<label style="font-weight: 700; color: #52372A">Email<input type="email" style="{inp}"></label>
</div>
<label style="font-weight: 700; color: #52372A">What do you need?<select style="{inp}"><option>Skip bin</option><option>Skip bin + loading</option><option>Equipment hire</option><option>Labour hire</option><option>Portable toilet</option><option>Something else</option></select></label>
<label style="font-weight: 700; color: #52372A">Job address<input type="text" style="{inp}"></label>
<label style="font-weight: 700; color: #52372A">Tell us about the job<textarea rows="4" style="{inp}"></textarea></label>
<label style="font-weight: 700; color: #52372A">Photos of what's going (helps us quote)<input type="file" multiple accept="image/*" style="display: block; margin-top: 6px; font: inherit"></label>
<button type="button" style="background: #4F7230; color: #ffffff; font: inherit; font-weight: 700; padding: 14px 22px; border: none; border-radius: 8px; cursor: pointer; justify-self: start">Send</button>
</form>
</div>
</section>
'''
ab += FOOT.format(h=2400)
open('project/About.dc.html', 'w').write(ab)

c = json.load(open('project/canvas.json'))
y = 18500
for f, t, h in [('Equipment.dc.html', 'Equipment Hire page', 2400), ('Labour.dc.html', 'Labour Hire page', 2200), ('About.dc.html', 'About & Contact page', 2400)]:
    c['boards'][f] = {'x': 0, 'y': y, 'w': 1440, 'h': h, 'title': t, 'expand': 'fill'}
    if f not in c['order']:
        c['order'].append(f)
    y += h + 200
c['notes']['s5'] = {'x': 1540, 'y': 18500, 'w': 460, 'text': 'Equipment: small plant dry hire (pumps, saws, jackhammers, up to 12-inch chipper); loaders/excavators wet hire only (Al, 24 Nov). Rates by quote. Grey boxes = photos still needed (small plant, crew loading). Business hours still to confirm.', 'fill': 'orange'}
json.dump(c, open('project/canvas.json', 'w'))
print('ok')
