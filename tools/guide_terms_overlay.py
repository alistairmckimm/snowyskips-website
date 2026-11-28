"""Skip Bin Guide v2: add terms-and-conditions pointers (footer on every page + box on page 3)."""
import io
from pypdf import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import Color, white, HexColor
from reportlab.platypus import Paragraph
from reportlab.lib.styles import ParagraphStyle

SRC = '/home/claude/guide2/Snowy-Skips-Skip-Bin-Guide.pdf'
OUT = '/home/claude/guide3/Snowy-Skips-Skip-Bin-Guide.pdf'
W, H = 595.276, 841.89
NAVY = HexColor('#0C2140'); GREEN = HexColor('#3D7B35'); GREY = Color(122/255, 132/255, 148/255)
URL = 'https://snowyskips.com.au/terms/'


def y(top):
    return H - top


def footer(c, n):
    c.setFillColor(white); c.rect(30, y(831), W - 60, 831 - 793, stroke=0, fill=1)
    c.setStrokeColor(HexColor('#E3E6EA')); c.setLineWidth(0.6); c.line(40, y(795), W - 40, y(795))
    c.setFillColor(GREY); c.setFont('Helvetica', 7.4)
    c.drawString(40, y(803.5), 'Snowy Skips • a McKimm Civil Pty Ltd business • 0408 632 007 • bookings@snowyskips.com.au')
    c.setFont('Helvetica', 8.5); c.drawRightString(W - 40, y(803.5), f'Page {n} of 3')
    c.setFont('Helvetica', 6.3)
    c.drawString(40, y(812.5), 'Prices marked + GST exclude GST. Landfill fees are set by Snowy Monaro Regional Council and change each July. This guide is general information only.')
    t1 = 'Terms and conditions: '; t2 = 'snowyskips.com.au/terms'; t3 = '  •  please read them before you hire. By booking or accepting delivery, you agree to them.'
    x = 40; base = y(823)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 7.6); c.drawString(x, base, t1); x += c.stringWidth(t1, 'Helvetica-Bold', 7.6)
    c.setFillColor(GREEN); c.drawString(x, base, t2)
    w2 = c.stringWidth(t2, 'Helvetica-Bold', 7.6)
    c.linkURL(URL, (x, base - 2, x + w2, base + 8), relative=0)
    c.setStrokeColor(GREEN); c.setLineWidth(0.5); c.line(x, base - 1.2, x + w2, base - 1.2)
    x += w2
    c.setFillColor(NAVY); c.setFont('Helvetica', 7.6); c.drawString(x, base, t3)


def page3_box(c):
    top, h = 655, 92
    L, R = 40, W - 40
    c.setFillColor(HexColor('#EEF3E6')); c.roundRect(L, y(top + h), R - L, h, 6, stroke=0, fill=1)
    c.setFillColor(GREEN); c.rect(L, y(top + h), 5, h, stroke=0, fill=1)
    c.setFillColor(NAVY); c.setFont('Helvetica-Bold', 13); c.drawString(L + 18, y(top + 22), 'Before you hire: our terms and conditions')
    st = ParagraphStyle('b', fontName='Helvetica', fontSize=10.5, leading=14.5, textColor=HexColor('#222222'))
    p = Paragraph('All bookings are subject to our hire conditions, including payment, cancellations, waiting time, '
                  'overfilled bins, banned items, bin damage and unpaid bins. Please read them on our website at '
                  f'<a href="{URL}" color="#3D7B35"><u><b>snowyskips.com.au/terms</b></u></a>. '
                  '<b>By booking or accepting delivery, you agree to them.</b>', st)
    w, hh = p.wrap(R - L - 36, 200)
    p.drawOn(c, L + 18, y(top + 32) - hh)


r = PdfReader(SRC)
w = PdfWriter(clone_from=r)
for i, pg in enumerate(w.pages):
    buf = io.BytesIO(); c = canvas.Canvas(buf, pagesize=(W, H))
    footer(c, i + 1)
    if i == 2:
        page3_box(c)
    if i == 0:
        c.setFillColor(HexColor('#9FB3C8')); c.setFont('Helvetica', 9.5)
        c.drawRightString(W - 40, y(66), 'Before you hire, read our terms and conditions:')
        c.setFillColor(white); c.setFont('Helvetica-Bold', 12)
        c.drawRightString(W - 40, y(83), 'snowyskips.com.au/terms')
        tw = c.stringWidth('snowyskips.com.au/terms', 'Helvetica-Bold', 12)
        c.linkURL(URL, (W - 40 - tw, y(83) - 3, W - 40, y(83) + 11), relative=0)
    c.save()
    ov = PdfReader(io.BytesIO(buf.getvalue())).pages[0]
    pg.merge_page(ov)
    # keep the overlay's link annotation
w.add_metadata({'/Title': 'Snowy Skips - Skip Bin Guide', '/Author': 'Snowy Skips'})
with open(OUT, 'wb') as f:
    w.write(f)
print('wrote', OUT)
