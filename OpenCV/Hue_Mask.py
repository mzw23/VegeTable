import sys
import time
import cv2
import numpy as np
import cmath
import os
from matplotlib import pyplot as plt


def maskImage(image):
	thresh = 125
	height, width, channels = image.shape
	mask = np.zeros( (height,width) )
	i = 0
	for i in range(len(image)):
		row = image[i]
		j = 0
		for j in range(len(row)):
			pixel = row[j]
			total = abs(255 - int(pixel[0])) + abs(255-int(pixel[1])) + abs(255-int(pixel[2]))
			if ( total > thresh):
				mask[i][j] = 1
			j += 1
		i += 1
	return (mask)

def maskImageHue(image):
	thresh = 170
	height, width, channels = image.shape
	hue,sat,val = cv2.split(image)
	total = 0
	pixels = 0
	mask = np.zeros( (height,width) )
	i = 0
	for i in range(len(hue)):
		h = hue[i]
		j = 0
		for j in range(len(h)):
			pixel = h[j]
			if ( pixel < thresh):
				mask[i][j] = 1
				total += pixel
				pixels += 1
			j += 1
		i += 1
	avg_hue = total / pixels
	print (avg_hue)
	return (mask)

fp = os.path.dirname(__file__) + 'images/test/apple.jpg'
img = cv2.imread(fp)
mask = maskImage(img)
hue_mask = maskImageHue(img)
cv2.imshow('mask',mask)
cv2.moveWindow('mask',0,0)
cv2.imshow('hue mask',hue_mask)
cv2.moveWindow('hue mask',500,0)
cv2.waitKey(0)
