#!/usr/bin/env python3
"""Full-sheet fill textures for the two drips (sampled by canvas position, so the shape reveals
them like a mask):  cream.webp = the well's own paper extended to a full sheet;
rose.webp = soft blurred rose marble base with the real rose pieces composited on top."""
from PIL import Image, ImageFilter; import numpy as np, pathlib
R=pathlib.Path(__file__).resolve().parents[2]; S=R/'reference/originals/plate-pieces'; O=R/'src/assets/fills'
W,H=941,1672
w=Image.open(S/'piece-1.png').convert('RGBA'); wa=np.asarray(w).astype(np.float32)
rng=np.random.default_rng(3); base=np.array([241,230,206],np.float32)[None,None,:]+rng.normal(0,5.5,(H,W,1))
a=wa[:,:,3:4]/255.0; cream=wa[:,:,:3]*a+base*(1-a)
Image.fromarray(np.clip(cream,0,255).astype(np.uint8)).resize((840,1493),Image.LANCZOS).save(O/'cream.webp','WEBP',quality=84,method=6)
rose3=Image.open(S/'piece-3.png').convert('RGBA'); rose6=Image.open(S/'piece-6.png').convert('RGBA')
ra=np.asarray(rose3); ys,xs=np.nonzero(ra[:,:,3]>250)
y0,y1=np.percentile(ys,15).astype(int),np.percentile(ys,60).astype(int); x0,x1=np.percentile(xs,25).astype(int),np.percentile(xs,85).astype(int)
patch=Image.fromarray(ra[y0:y1,x0:x1,:3]); pw,ph=patch.size; sheet=Image.new('RGB',(W,H))
for j,yy in enumerate(range(0,H,ph)):
    for i,xx in enumerate(range(0,W,pw)):
        t=patch
        if i%2: t=t.transpose(Image.FLIP_LEFT_RIGHT)
        if j%2: t=t.transpose(Image.FLIP_TOP_BOTTOM)
        sheet.paste(t,(xx,yy))
sheet=sheet.filter(ImageFilter.GaussianBlur(26))
g=np.random.default_rng(5).normal(0,4,(H,W,1)); sheet=Image.fromarray(np.clip(np.asarray(sheet).astype(np.float32)+g,0,255).astype(np.uint8)).convert('RGBA')
sheet.alpha_composite(rose6); sheet.alpha_composite(rose3)
sheet.convert('RGB').resize((840,1493),Image.LANCZOS).save(O/'rose.webp','WEBP',quality=84,method=6); print('fills written')
