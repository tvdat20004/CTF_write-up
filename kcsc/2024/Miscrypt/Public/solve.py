from PIL import Image
import numpy as np
import galois
from tqdm import trange
GF256 = galois.GF(2**8)

img = Image.open('qr_flag_encrypt.png')
pixels = img.load()
width, height = img.size

M = GF256([pixels[0,0], pixels[0,1], pixels[0,2]]) - GF256([[255, 255,255]]*3)
for x in trange(width):
    for y in range(0,height,3):
        A = GF256([pixels[x, y], pixels[x, y+1], pixels[x, y+2]])
        res = A - M 
        M = A  
        pixels[x, y], pixels[x, y+1], pixels[x, y+2] = [tuple([int(i) for i in j]) for j in res]
img.save("qr_flag_rgb.png")