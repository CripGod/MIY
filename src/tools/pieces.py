#!/usr/bin/env python3
"""Export the eight plate pieces (reference/originals/plate-pieces/piece-N.png, 941x1672 RGBA)
to src/assets/pieces/pN.webp at 840px wide. The engine uses p2,p3,p4,p5,p7,p8.
p1 (cream well) and p6 (left rose) are replaced by the procedural drips but kept for reference."""
from PIL import Image; import pathlib
R=pathlib.Path(__file__).resolve().parents[2]; SRC=R/'reference/originals/plate-pieces'; OUT=R/'src/assets/pieces'
for i in range(1,9):
    im=Image.open(SRC/f'piece-{i}.png').convert('RGBA'); w=840; im=im.resize((w,int(im.height*w/im.width)),Image.LANCZOS)
    im.save(OUT/f'p{i}.webp','WEBP',quality=84,method=6); print('p%d'%i, im.size)
