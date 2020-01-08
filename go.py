#!/usr/bin/python
# -*- coding: utf8 -*-
# 11 mars 2015 - Tristan Le Toullec  

import bathy
import numpy
import matplotlib.pyplot as plt
from PIL import Image

bathy = bathy.etopo2('etopo2.nc')

print(bathy.about())

long, lat = -4.86774, 48.15
width = 2300
height = 1500
nbframe = 1 * 30

tab = numpy.zeros((height,width))

for i in range(0,height):
        for j in range(0,width):
            tab[i,j]=bathy.getLevel(long+j/30.0,lat+i/30.0)

for framenum in range(nbframe):
    plt.imshow(tab)
    plt.savefig('frames/frame'+str(framenum)+'.png')

    long = long + 30
    lat = lat
    tab = numpy.roll(tab, -5, axis=1)

    for i in range(0,height):
            tab[i,0] = bathy.getLevel(long, lat+i/30.0)

plt.savefig('frames/THEEND.png')
