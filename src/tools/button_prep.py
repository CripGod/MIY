#!/usr/bin/env python3
"""Button assets.
Well… button (reference/originals/button-well-v2.png): the disc position was MEASURED by hand
(auto-detection kept snagging the wine text and the gold rim): cx=0.873 cy=0.475 r=0.0675 of the trimmed image.
 1. inpaint the baked arrow out of the disc (radial wine fill) so the standalone arrow can pass through
 2. lift the wine text into three word layers (Well… / that's / annoying.) and inpaint it out of the background
 3. write button-well.webp, circle.json, words.json
I'd check button (reference/originals/button-idcheck.png): disc detected automatically (it arrives empty)."""
from PIL import Image, ImageFilter; import numpy as np, json, pathlib
R=pathlib.Path(__file__).resolve().parents[2]; O=R/'src/assets'
def radial_fill(a, inside, light, dist, rad):
    out=a.copy(); bins=np.clip((dist/rad*24).astype(int),0,30)
    for ch in range(3):
        prof=np.full(31,100.0)
        for bi in range(31):
            m=inside&(~light)&(bins==bi)
            if m.sum()>0: prof[bi]=a[:,:,ch][m].mean()
        prof=np.convolve(prof,np.ones(3)/3,mode='same'); out[:,:,ch][light]=prof[bins[light]]
    o2=np.asarray(Image.fromarray(out.astype(np.uint8),'RGBA').filter(ImageFilter.GaussianBlur(2))).astype(np.int32); out[light,:3]=o2[light,:3]
    return out
# ---------- Well… ----------
im=Image.open(R/'reference/originals/button-well-v2.png').convert('RGBA'); im=im.crop(im.getbbox())
a=np.asarray(im).astype(np.int32); H,W=a.shape[:2]; r,g,b,al=a[:,:,0],a[:,:,1],a[:,:,2],a[:,:,3]; lum=0.299*r+0.587*g+0.114*b
yy,xx=np.mgrid[0:H,0:W]
cxn,cyn,rn=0.873,0.475,0.0675; cx,cy,rad=cxn*W,cyn*H,rn*W
# text layer (dark wine ink on the cream panel, quail feet excluded)
notquail=~((xx<W*0.128)&(yy>H*0.54))
region=(xx>W*0.114)&(xx<W*0.79)&(yy>H*0.30)&(yy<H*0.70)&(al>200)&notquail
dark=np.clip((135-lum)/45.0,0,1); raw=np.where(region,np.clip((r-g-30)/70.0,0,1)*dark,0); t=np.clip((raw-0.10)/0.45,0,1)
text=np.zeros((H,W,4),np.uint8); ink=t>0.35
text[:,:,0]=np.where(ink,r,124); text[:,:,1]=np.where(ink,g,40); text[:,:,2]=np.where(ink,b,54); text[:,:,3]=(t*255).astype(np.uint8)
timg=Image.fromarray(text,'RGBA')
mask=raw>0.05; mk=Image.fromarray((mask*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(11)); mask2=(np.asarray(mk)>0)&(lum<200)&region
panel=region&(~mask2)&(lum>190); cream_mean=np.array([a[:,:,c][panel].mean() for c in range(3)])
filled=a.copy(); filled[mask2,:3]=cream_mean
bl=np.asarray(Image.fromarray(filled.astype(np.uint8),'RGBA').filter(ImageFilter.GaussianBlur(9))).astype(np.int32)
out=a.copy(); out[mask2,:3]=bl[mask2,:3]
grain=np.random.default_rng(7).normal(0,3.2,(H,W,1)); out[mask2,:3]=np.clip(out[mask2,:3]+grain[mask2].repeat(3,axis=1),0,255)
# disc: remove the baked arrow
dist=np.sqrt((xx-cx)**2+(yy-cy)**2); inside=dist<rad*0.92
core=inside&(lum>92); mm=Image.fromarray((core*255).astype(np.uint8)).filter(ImageFilter.MaxFilter(7)); light=(np.asarray(mm)>0)&inside
out=radial_fill(out,inside,light,dist,rad)
Image.fromarray(out.astype(np.uint8),'RGBA').resize((820,int(H*820/W)),Image.LANCZOS).save(O/'buttons/button-well.webp','WEBP',quality=90,method=6)
json.dump({"cx":cxn,"cy":cyn,"r":rn},open(O/'geometry/circle.json','w'))
WORDS=[[193,634],[670,891],[915,1321]]   # x ranges of Well… / that's / annoying. in the trimmed 1672-wide image
rows=(raw>0.35).sum(axis=1); ry=np.nonzero(rows>0)[0]; y0,y1=int(ry.min()),int(ry.max()); words=[]
for i,(x0,x1) in enumerate(WORDS):
    pad=10; crop=timg.crop((max(0,x0-pad),max(0,y0-pad),min(W,x1+pad),min(H,y1+pad)))
    ww=int(crop.width*0.75); crop=crop.resize((ww,int(crop.height*ww/crop.width)),Image.LANCZOS); crop.save(O/f'words/word{i}.webp','WEBP',quality=94,method=6)
    words.append({"x":(x0-pad)/W,"y":(y0-pad)/H,"w":(x1-x0+2*pad)/W})
json.dump(words,open(O/'geometry/words.json','w')); print('Well… button + words + circle.json written')
# ---------- I'd check ----------
im=Image.open(R/'reference/originals/button-idcheck.png').convert('RGBA'); im=im.crop(im.getbbox())
a=np.asarray(im).astype(np.int32); H,W=a.shape[:2]; r,g,b,al=a[:,:,0],a[:,:,1],a[:,:,2],a[:,:,3]; yy,xx=np.mgrid[0:H,0:W]
burg=(xx>W*0.74)&(al>200)&(r>70)&(r<160)&(g<70)&(b<90)&(r-g>45)
ys,xs=np.nonzero(burg); cx,cy=np.median(xs),np.median(ys); dist=np.sqrt((xx-cx)**2+(yy-cy)**2); rad=None
for Rr in range(30,400,2):
    ann=(dist>=Rr-2)&(dist<Rr); frac=burg[ann].mean() if ann.sum()>0 else 0
    if Rr>60 and frac<0.35: rad=Rr; break
json.dump({"cx":cx/W,"cy":cy/H,"r":rad/W},open(O/'geometry/circle2.json','w'))
im.resize((820,int(H*820/W)),Image.LANCZOS).save(O/'buttons/button-idcheck.webp','WEBP',quality=90,method=6); print("I'd check button + circle2.json written")
