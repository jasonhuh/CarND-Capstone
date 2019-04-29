#!/usr/bin/python
import cv2
import os
import re

imgDir       = 'labeledImages/'
xmlDir       = 'imgLabels/'
imgFileNames = os.listdir(imgDir)
#print (imgFileNames)

for imgFileName in imgFileNames:

	#imgFileName = imgFileNames[0]
	xmlFileName = imgFileName.replace("png", "xml")
	if (not os.path.isfile(xmlDir+xmlFileName)):
		continue
	#print (imgFileName, xmlFileName)

	##-- flip img and write out to file ----------------------------------------#
	img = cv2.imread(imgDir+imgFileName)
	H, W, channels = img.shape
	print ("MIKE  Img size:", H, W, channels)
	#cv2.imshow('Test image',img)
	#cv2.waitKey(3*1000)
	#cv2.destroyAllWindows()

	img = cv2.flip( img, 1 )
	cv2.imwrite(imgDir+"flip"+imgFileName, img)
	#cv2.imshow('Test image',img)
	#cv2.waitKey(3*1000)
	#cv2.destroyAllWindows()


	##-- read in xml file...  Modify... Write out as flip file ------------------#
	with open(xmlDir+xmlFileName, 'r') as content_file:
		content = content_file.read()
	print (content)

	xmin = int(re.search('<xmin>(.*)<', content).group(1))
	ymin = int(re.search('<ymin>(.*)<', content).group(1))
	xmax = int(re.search('<xmax>(.*)<', content).group(1))
	ymax = int(re.search('<ymax>(.*)<', content).group(1))

	print (xmin ,ymin ,xmax ,ymax)

	xmaxFlip = W-1-xmin+1
	xminFlip = W-1-xmax-1

	print (xminFlip ,ymin ,xmaxFlip ,ymax)
	print ('<xmin>'+str(xmin)+'<', '<xmin>'+str(xminFlip)+'<')
	content = content.replace('<xmin>'+str(xmin)+'<', '<xmin>'+str(xminFlip)+'<')
	content = content.replace('<xmax>'+str(xmax)+'<', '<xmax>'+str(xmaxFlip)+'<')
	print (content)

	f= open(xmlDir+'flip'+xmlFileName,"w")
	f.write(content)


