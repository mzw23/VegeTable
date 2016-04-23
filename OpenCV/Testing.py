import sys
import time
import cv2
import numpy as np
import cmath
import os
from matplotlib import pyplot as plt

def perimeter(points):
	length = 0
	for element in points:
		for e in element:
			a = e[0]
			b = e[1]
			c = (a**2)+(b**2)
			c = c**0.5
			length = length + c
	return(length)

def getContours(image,mask):
	orig = image.copy()
	mask = np.array(mask * 255, dtype = np.uint8)
	contours, hierarchy = cv2.findContours(mask,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)
	sizes = []
	for i in range(len(contours)):
		perim = perimeter(contours[i])
		sizes.append([perim,i])
	sizes.sort(key=lambda x: x[0],reverse=True)
	contour = contours[sizes[0][1]]
	cv2.drawContours(image, contour, -1, (0,0,255), 3)
	return (image,contour)

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
	cv2.destroyAllWindows()
	return (mask)

def getColor(mask,image):
	pixels = 0
	b = 0
	g = 0
	r = 0
	for i in range(len(mask)):
		mask_row = mask[i]
		row = image[i]
		for j in range(len(mask_row)):
			mask_column = mask_row[j]
			column = row[j]
			if (mask_column == 1):
				pixels += 1
				b = b + column[0]
				g = g + column[1]
				r = r + column[2]
	b_avg = b / pixels
	g_avg = g / pixels
	r_avg = r / pixels
	return (b_avg, g_avg, r_avg)

def getArea(mask):
	total = 0
	for row in mask:
		for pixel in row:
			total += pixel
	return (total)

def processImage(image):
	img = None
	if (str(type(image))=='<type \'str\'>'):
		img = cv2.imread(image)
	if (str(type(image))=='<type \'numpy.ndarray\'>'):
		img = image.copy()
	height, width, channels = img.shape
	orig = img.copy()
	mask = maskImage(img)
	img, contour = getContours(img,mask)
	b, g, r = getColor(mask,img)
	convex_hull = cv2.convexHull(contour,returnPoints=True)
	perim = perimeter(contour)
	total_convex = (perim)/ (perimeter(convex_hull))
	perim_area = (perim/
(mask))
	return ([total_convex,perim_area,b,g,r])

def parseLine(line):
	s = ''
	field = 0
	d = 0
	data = []
	for c in line:
		if (c != ','):
			s = s + c
		else:
			if ( field == 0 ):
				d = s
			elif ( (field == 1) or (field == 2) ):
				d = float(s)
			else:
				d = int(s)
			field += 1
			s = ''
			data.append(d)
	d = int(s)
	data.append(d)
	return (data)

def getData(data_source):
	all_data = []
	with open(data_source,'r') as f:
		for line in f:
			data = parseLine(line)
			all_data.append(data)
	return (all_data)

def identifyObject (image_data,data_source):
	data = getData(data_source)
	convex_ratio = image_data[0]
	area_ratio = image_data[1]
	b = float(image_data[2])
	g = float(image_data[3])
	r = float(image_data[4])
	matches = []
	for d in data:
		ident = d[0]
		convex_ratio_src = d[1]
		area_ratio_src = d[2]
		b_src = float(d[3])
		g_src = float(d[4])
		r_src = float(d[5])
		convex_ratio_pct = abs((convex_ratio - convex_ratio_src)/convex_ratio_src)
		area_ratio_pct = abs((area_ratio - area_ratio_src)/area_ratio_src)
		b_pct = abs((b - b_src)/b_src)
		g_pct = abs((g - g_src)/g_src)
		r_pct = abs((r - r_src)/r_src)
		pct_dif_avg = (convex_ratio_pct + area_ratio_pct + b_pct + g_pct + r_pct ) / 5
		match = [ident,pct_dif_avg]
		matches.append(match)
	best_id = 0
	best_pct = 100
	for m in matches:
		if (m[1] < best_pct):
			best_id = m[0]
			best_pct = m[1]
	return (best_id,best_pct)

def main(obj_id,path):
	results = []
	files = os.listdir(path)
	for f in files:
		file_path = path + f
		img = cv2.imread(file_path)
		data = processImage(img)
		identity, pct_dif = identifyObject(data,'data.txt')
		results.append([obj_id,identity])
	summary = []
	for result in results:
		i = 0
		actual_id = result[0]
		result_id = result[1]
		in_list = False
		for i in range(len(summary)):
			s = summary[i]
			if (actual_id == s[0]):
				in_list = True
				s[1] += 1
				if (actual_id == result_id):
					s[2] += 1
		if (in_list == False):
			correct = False
			if (actual_id == result_id):
				summary.append([actual_id,1,1])
			else:
				summary.append([actual_id,1,0])
	overall_total = 0
	overall_correct = 0
	for element in summary:
		overall_total += element[1]
		overall_correct += element[2]
		total = float(element[1])
		correct = float(element[2])
		pct_correct = (correct / total) * 100
		pct_correct = round(pct_correct,2)
		output = str(element[0]) + ' - ' + str(pct_correct) + '% correct (' + str(element[2]) + '/' + str(element[1]) + ')'
		print (output)
		return correct, total	
		
fp = os.path.dirname(__file__) + 'images/simple/testing/'
folders = os.listdir(fp)
overall_total = 0
overall_correct = 0
for folder in folders:
	dir_path = fp + folder + '/'
	obj_id = folder
	correct, total = main(obj_id,dir_path)
	overall_total += total
	overall_correct += correct
overall_pct = round((float(overall_correct)/float(overall_total)) * 100,2)
print ('Total - ' + str(overall_pct) + '% correct (' + str(int(overall_correct)) + '/' + str(int(overall_total)) + ')')
