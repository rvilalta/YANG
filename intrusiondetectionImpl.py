import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import cv2
import sys
class IntrusiondetectionImpl:
     
    @classmethod
    def put(cls, intrusiondetectionschema):
        print str(intrusiondetectionschema)
        print 'handling put'
	if "disarmed" in str(intrusiondetectionschema):
		sys.exit(0)
	elif "armed" in str(intrusiondetectionschema):	
		cap = cv2.VideoCapture(0)

		cap.set(4,1024)
	
		while True:
   			ret, img = cap.read()
    			cv2.imshow("input", img)

    			key = cv2.waitKey(10)
    			if key == 27:
        			break
	               

		cv2.destroyAllWindows() 	
		cv2.VideoCapture(0).release()
    	
    @classmethod
    def post(cls, intrusiondetectionschema):
        print str(intrusiondetectionschema)
        print 'handling post'
        be.intrusiondetection = intrusiondetectionschema

    @classmethod
    def delete(cls, ):
        print 'handling delete'
        if be.intrusiondetection:
            del be.intrusiondetection
        else:
            raise KeyError('')

    @classmethod
    def get(cls, ):
        print 'handling get'
        if be.intrusiondetection:
            return be.intrusiondetection
        else:
            raise KeyError('')


