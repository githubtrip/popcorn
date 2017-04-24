#!/usr/bin/python
# -*- coding: utf8 -*-
# 11 mars 2015 - Tristan Le Toullec  

import matplotlib.pyplot as plt
from PIL import Image

img = Image.open("logo.png")

for i in range(0,360):
    img2 = img.rotate(i)
    img2.save("frames/frame-%s.png" % str(i))

img.save("frames/THEEND.png")
