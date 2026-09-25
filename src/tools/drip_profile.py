#!/usr/bin/env python3
"""Derive src/assets/geometry/drip.json from the cream well silhouette (piece-1).
The profile is a polar radius r(theta) around the well centroid, measured in SCREEN-polar
coordinates for the iPhone 17 canvas (402x874): clip position = center + s*(cos(th)/ASP, sin(th)).
That is what lets the shader morph a *perfect on-screen circle* (constant s) into the drip (s = r[theta])."""
from PIL import Image; import numpy as np, json, pathlib
R=pathlib.Path(__file__).resolve().parents[2]
W,H=941,1672; ASP=402/874; SX=(941/1672)/ASP          # SX = half-width of a plate quad in clip space ("cover" fit)
well=np.asarray(Image.open(R/'reference/originals/plate-pieces/piece-1.png').convert('RGBA'))[:,:,3]
ys,xs=np.nonzero(well>128); cxp,cyp=xs.mean(),ys.mean()
cx=(cxp/W*2-1)*SX; cy=-(cyp/H*2-1)
N=180; prof=[]
for i in range(N):
    th=2*np.pi*i/N; dx,dy=np.cos(th)/ASP,np.sin(th); last=0.0
    for s in np.arange(0.0,1.6,0.003):
        px=int(round((((cx+dx*s)/SX)+1)/2*(W-1))); py=int(round((1-((cy+dy*s)+1)/2)*(H-1)))
        if 0<=px<W and 0<=py<H and well[py,px]>128: last=s
    prof.append(last)
p=np.array(prof); k=np.array([1,2,3,2,1])/9.0
ps=[float(np.dot(k,[p[(i+j)%N] for j in range(-2,3)])) for i in range(N)]
json.dump({"cx":round(float(cx),4),"cy":round(float(cy),4),"sx":round(SX,4),"asp":round(ASP,4),"r":[round(v,4) for v in ps]},open(R/'src/assets/geometry/drip.json','w'))
print('drip.json: center',round(cx,3),round(cy,3),'r range',round(min(ps),3),round(max(ps),3))
