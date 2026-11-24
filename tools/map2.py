import math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
exec(open('/home/claude/map/zones.py').read().split('LON0')[0])  # towns, outline
LON0,LON1,LAT0,LAT1=146.55,150.20,-35.05,-38.00
C=math.cos(math.radians(36.5)); K=520
W=int((LON1-LON0)*K*C); H=int((LAT0-LAT1)*K)
def P(lon,lat): return ((lon-LON0)*K*C,(LAT0-lat)*K)
def chaikin(pts,n=3):
    for _ in range(n):
        q=[]
        for i in range(len(pts)):
            a=pts[i]; b=pts[(i+1)%len(pts)]
            q+=[(0.75*a[0]+0.25*b[0],0.75*a[1]+0.25*b[1]),(0.25*a[0]+0.75*b[0],0.25*a[1]+0.75*b[1])]
        pts=q
    return pts
img=Image.new('RGBA',(W,H),(255,255,255,255)); d=ImageDraw.Draw(img)
# NSW/VIC border (approx): Murray from Albury upstream, then straight line to Cape Howe
border=[(146.80,-36.10),(147.05,-36.02),(147.40,-35.98),(147.70,-35.95),(147.93,-36.04),(147.99,-36.14),(148.08,-36.28),(148.14,-36.45),(148.20,-36.79),(149.976,-37.505)]
# coast (approx) for context
coast=[(150.20,-35.70),(150.15,-35.95),(150.08,-36.20),(150.05,-36.45),(149.98,-36.70),(149.92,-36.90),(149.93,-37.10),(149.976,-37.505),(149.70,-37.70),(149.40,-37.78),(149.10,-37.80),(148.80,-37.80),(148.40,-37.82),(148.00,-37.85),(147.70,-37.92),(147.40,-38.00)]
cp=[P(*p) for p in coast]
sea=cp+[(W,H),(W,0)]
d.polygon(cp+[P(147.40,-38.10),(W,H+5),(W+5,0)],fill=(233,241,247,255))
d.line(cp,fill=(190,210,225,255),width=3)
# outer quote area
outer=[(148.70,-35.62),(148.35,-35.70),(147.95,-35.78),(147.60,-35.82),(147.48,-36.02),(147.60,-36.30),(147.95,-36.44),(148.08,-36.72),(148.45,-37.08),(148.80,-37.32),(149.02,-37.62),(149.25,-37.70),(149.47,-37.55),(149.56,-37.25),(149.52,-36.95),(149.58,-36.60),(149.66,-36.20),(149.55,-35.90),(149.35,-35.66),(149.10,-35.55)]
op=chaikin([P(*p) for p in outer],3)
d.polygon(op,fill=(236,228,214,255))
# dashed outer border
for i in range(len(op)):
    if i%6<3: d.line([op[i],op[(i+1)%len(op)]],fill=(150,120,100,255),width=4)
bp=[P(*p) for p in border]
for i in range(len(bp)-1):
    x0,y0=bp[i];x1,y1=bp[i+1];L=math.hypot(x1-x0,y1-y0);n=int(L//18)
    for k in range(n):
        if k%2==0:
            a=k/n;b=min((k+1)/n,1)
            d.line([(x0+(x1-x0)*a,y0+(y1-y0)*a),(x0+(x1-x0)*b,y0+(y1-y0)*b)],fill=(170,170,170,255),width=3)
# zones
poly=chaikin([P(*p) for p in outline],3)
mask=Image.new('L',(W,H),0); ImageDraw.Draw(mask).polygon(poly,fill=255); m=np.array(mask)>0
zs=['C','1','2','3','4']
tp=np.array([P(lo,la) for lo,la,z in towns.values()]); tz=np.array([zs.index(z)+1 for lo,la,z in towns.values()])
yy,xx=np.mgrid[0:H,0:W]
best=np.zeros((H,W),np.uint8); bd=np.full((H,W),1e18)
for (tx,ty),zi in zip(tp,tz):
    dd=(xx-tx)**2+(yy-ty)**2; sel=dd<bd; bd[sel]=dd[sel]; best[sel]=zi
lab=Image.fromarray(best).filter(ImageFilter.ModeFilter(37)); lp=np.array(lab)
cols={1:(79,114,48),2:(156,192,111),3:(232,197,90),4:(217,139,74),5:(127,169,207)}
arr=np.array(img)
for zi,(r,g,b) in cols.items():
    sel=m&(lp==zi); arr[sel]=(r,g,b,255)
edge=np.zeros((H,W),bool); e=(lp[:-2,:-2]!=lp[2:,:-2])|(lp[:-2,:-2]!=lp[:-2,2:]); edge[:-2,:-2]=e
edge&=m; arr[edge]=(255,255,255,255)
img=Image.fromarray(arr); d=ImageDraw.Draw(img)
d.line(poly+[poly[0]],fill=(82,55,42,255),width=5,joint='curve')
FP='/usr/share/fonts/truetype/google-fonts/ofl/sourcesans3/SourceSans3[wght].ttf'
FI='/usr/share/fonts/truetype/google-fonts/ofl/sourcesans3/SourceSans3-Italic[wght].ttf'
def font(sz,w='Bold',it=False):
    f=ImageFont.truetype(FI if it else FP,sz)
    try: f.set_variation_by_name(w)
    except Exception: pass
    return f
fb=font(30,'Bold'); fs=font(27,'SemiBold'); fr=font(30,'SemiBold',True); fst=font(34,'Bold')
def label(lon,lat,text,f,side='r',fill=(31,31,31),dot=(31,31,31),sq=False):
    x,y=P(lon,lat); r=7
    if sq: d.rectangle([x-r,y-r,x+r,y+r],fill=dot,outline=(255,255,255),width=3)
    else: d.ellipse([x-r,y-r,x+r,y+r],fill=dot,outline=(255,255,255),width=3)
    tw=d.textlength(text,font=f); th=f.size
    if side=='r': tx,ty=x+14,y-th*0.62
    elif side=='l': tx,ty=x-14-tw,y-th*0.62
    elif side=='u': tx,ty=x-tw/2,y-th*1.55
    else: tx,ty=x-tw/2,y+10
    d.text((tx,ty),text,font=f,fill=fill,stroke_width=5,stroke_fill=(255,255,255))
main=[('Cooma',149.1246,-36.2353,'r'),('Berridale',148.829,-36.365,'r'),('Jindabyne',148.623,-36.416,'d'),('Thredbo',148.306,-36.505,'l'),
 ('Adaminaby',148.771,-35.997,'r'),('Bredbo',149.15,-35.958,'r'),('Michelago',149.165,-35.711,'r'),('Nimmitabel',149.283,-36.512,'r'),
 ('Dalgety',148.833,-36.504,'r'),('Bombala',149.238,-36.912,'r'),('Delegate',148.942,-37.044,'l')]
for t,lo,la,s in main: label(lo,la,t,fb,s)
outert=[('Khancoban',148.13,-36.22,'r'),('Corryong',147.90,-36.20,'d'),('Walwa',147.73,-35.96,'u'),
 ('Cabramurra',148.38,-35.94,'r'),('Bendoc',148.88,-37.15,'d'),('Cann River',149.15,-37.57,'d')]
for t,lo,la,s in outert: label(lo,la,t,fs,s,fill=(82,55,42),dot=(82,55,42))
refs=[('Canberra',149.13,-35.28,'r'),('Albury–Wodonga',146.91,-36.10,'d'),('Bairnsdale',147.61,-37.82,'u'),('Merimbula',149.90,-36.89,'l')]
for t,lo,la,s in refs: label(lo,la,t,fr,s,fill=(120,120,120),dot=(150,150,150),sq=True)
for t,lo,la in [('NSW',147.45,-35.55),('VIC',147.35,-36.75)]:
    x,y=P(lo,la); d.text((x,y),t,font=fst,fill=(185,185,185),anchor='mm')
img.convert('RGB').save('service-map.png',optimize=True)
img.convert('RGB').resize((W//2,H//2),Image.LANCZOS).save('/tmp/sm.png')
print(W,H)
