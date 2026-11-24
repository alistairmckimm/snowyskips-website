from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, white
from reportlab.platypus import Paragraph, Frame
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
pdfmetrics.registerFont(TTFont('LS','/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf'))
pdfmetrics.registerFont(TTFont('LSB','/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf'))
from reportlab.lib.fonts import addMapping
addMapping('LS',0,0,'LS'); addMapping('LS',1,0,'LSB')
W,H=A4
NAVY=HexColor('#0C2140'); GREEN=HexColor('#3D7B35'); GREY=HexColor('#7A8494')
c=canvas.Canvas('p3.pdf',pagesize=A4)
hh=H*0.06
c.drawImage('/tmp/hdr.png',0,H-hh,W,hh)
L=40; R=W-40
body=ParagraphStyle('b',fontName='LS',fontSize=10.5,leading=14.5,textColor=HexColor('#222222'))
h2=ParagraphStyle('h',fontName='LSB',fontSize=15,leading=19,textColor=NAVY)
def para(txt,st,x,y,w,h):
    f=Frame(x,y,w,h,leftPadding=0,rightPadding=0,topPadding=0,bottomPadding=0,showBoundary=0)
    p=Paragraph(txt,st); f.addFromList([p],c)
y=H-hh-40
c.setFont('LSB',20); c.setFillColor(NAVY); c.drawString(L,y,'Too Good to Tip Giveaways')
c.setFont('LS',12); c.setFillColor(GREEN); c.drawString(L,y-18,'Our community reuse program')
para('Some items that come out of your bin are simply too good to go to landfill. When we find good-quality furniture, tools, building materials or other items, we may set them aside and give them away free to locals who need them through our <b>Too Good to Tip Giveaways</b> program, instead of tipping them. It keeps good things out of landfill and helps people in the community.',body,L,y-100,R-L,72)
# notice box
bx_top=y-112; bh=152
c.setFillColor(HexColor('#FBEBE7')); c.roundRect(L,bx_top-bh,R-L,bh,6,stroke=0,fill=1)
c.setFillColor(HexColor('#B03024')); c.rect(L,bx_top-bh,5,bh,stroke=0,fill=1)
c.setFont('LSB',13); c.setFillColor(HexColor('#B03024')); c.drawString(L+18,bx_top-24,'Everything must go to landfill? Tell us.')
para('If any items in your bin <b>must not be reused</b>, or if <b>everything has to go to landfill</b> (for example for privacy, security, warranty, insurance or contract reasons), you must let us know when you book, or before we pick up the bin.<br/><br/>Unless you tell us otherwise, by hiring a Snowy Skips bin you acknowledge and agree that items we consider suitable may be set aside and given away through the Too Good to Tip Giveaways program.',body,L+18,bx_top-bh+8,R-L-36,bh-40)
y2=bx_top-bh-30
c.setFont('LSB',13); c.setFillColor(NAVY); c.drawString(L,y2,'Good to know')
items=['<b>Personal items:</b> please remove documents, photos, hard drives, phones and anything with personal information before your bin is collected. We don\'t give away anything containing personal information.',
'<b>What we never give away:</b> gas appliances, child safety items (cots, car seats, prams, helmets), recalled or damaged items, unclean mattresses, anything that may contain asbestos, and untested electrical items unless clearly marked.',
'<b>Free for people who need them:</b> items are given to locals who will use them. Anyone found reselling is banned from the program.',
'<b>Unclaimed items</b> are recycled or disposed of properly after about 4 weeks.',
'See what\'s available: <b>snowyskips.com.au/too-good-to-tip</b>']
yy=y2-12
bul=ParagraphStyle('bl',parent=body,leftIndent=12,bulletIndent=0)
for t in items:
    p=Paragraph(t,bul,bulletText='•'); w,h=p.wrap(R-L,200); p.drawOn(c,L,yy-h); yy-=h+7
# CTA band
cy=yy-30; ch=62
c.setFillColor(NAVY); c.roundRect(L,cy-ch,R-L,ch,6,stroke=0,fill=1)
c.setFillColor(white); c.setFont('LSB',13); c.drawString(L+16,cy-22,'Questions? Get in touch.')
c.setFont('LS',11); c.drawString(L+16,cy-42,'Phone 0408 632 007   •   Email bookings@snowyskips.com.au   •   snowyskips.com.au')
# footer
c.setFont('LS',8.5); c.setFillColor(GREY)
c.drawString(L,34,'Snowy Skips • a McKimm Civil Pty Ltd business • 0408 632 007 • bookings@snowyskips.com.au')
c.drawRightString(R,34,'Page 3 of 3')
c.setFont('LS',7.5); c.drawString(L,22,'Landfill fees are set by Snowy Monaro Regional Council and change each July. This guide is general information only.')
c.showPage(); c.save()
