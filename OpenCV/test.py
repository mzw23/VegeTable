import numpy as np
import cv2

width = 500
height = 355
contours = np.array( [ [50,50], [50,150], [150, 150], [150,50] ] )
img = np.zeros( (height,width) )
i = 0
while (i<height):
	j = 0
	while (j<width):
		if ( (j>100) and (j<400) and (i>100) and (i>200) ):
			img[i][j] = 1
		j = j + 1
	i = i + 1
#cv2.fillPoly(img, pts =[contours], color=(255,255,255))
cv2.imshow(" ", img)
cv2.waitKey()