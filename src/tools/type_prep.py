#!/usr/bin/env python3
"""Type lockups.
Splash lockup (reference/originals/type-lockup-splash.png, wine type on WHITE): knock the white out to alpha,
then split into quail / MAYBE / IT'S YOU by the three clean horizontal bands (rows 258-484, 572-812, 853-1164).
Page-2 headline (reference/originals/type-lockup-p2-headline.png, RGBA): used whole; its two lines overlap where
the 'y' descends, so a straight split nicks glyphs. Animate it as one piece."""
from PIL import Image; import numpy as np, pathlib
R=pathlib.Path(__file__).resolve().parents[2]; O=R/'src/assets/type'
im=Image.open(R/'reference/originals/type-lockup-splash.png').convert('RGB'); a=np.asarray(im).astype(np.float32)
lum=0.299*a[:,:,0]+0.587*a[:,:,1]+0.114*a[:,:,2]; alpha=np.clip((255-lum)*1.9,0,255); alpha[alpha<26]=0
ko=Image.fromarray(np.dstack([np.asarray(im).astype(np.uint8),alpha.astype(np.uint8)]),'RGBA')
for y0,y1,nm in [(258,484,'quail'),(572,812,'maybe'),(853,1164,'itsyou')]:
    c=ko.crop((0,max(0,y0-6),ko.width,min(ko.height,y1+6))); c=c.crop(c.getbbox()); w=560; c=c.resize((w,int(c.height*w/c.width)),Image.LANCZOS)
    c.save(O/f'{nm}.webp','WEBP',quality=92,method=6); print(nm,c.size)
h=Image.open(R/'reference/originals/type-lockup-p2-headline.png').convert('RGBA'); h=h.crop(h.getbbox()); w=1100; h=h.resize((w,int(h.height*w/h.width)),Image.LANCZOS)
h.save(O/'headline-p2.webp','WEBP',quality=92,method=6); print('headline-p2',h.size)
