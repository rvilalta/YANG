import numpy as np
import cv2
import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be


cap = cv2.VideoCapture(0)
class IntrusiondetectionImpl:

	def put(cls, intrusiondetectionschema):
        	print str(intrusiondetectionschema)
        	print 'handling put'
        	be.intrusiondetection = intrusiondetectionschema


		#capture from camera at location 0
		cap = cv2.VideoCapture(0)
		#set the width and height, and UNSUCCESSFULLY set the exposure time
		cap.set(3,1280)
		cap.set(4,1024)
		cap.set(15, 0.1)

		while True:
    		ret, img = cap.read()
    		cv2.imshow("input", img)
    		#cv2.imshow("thresholded", imgray*thresh2)

    		key = cv2.waitKey(10)
    		if key == 27:
        		break


		cv2.destroyAllWindows() 
		cv2.VideoCapture(0).release()
	

