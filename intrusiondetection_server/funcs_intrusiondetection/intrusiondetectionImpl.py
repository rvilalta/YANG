import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import cv2
import sys
import imutils
import threading 
import numpy as np
import datetime

def video_name(video_counter):
    video_name='test'+str(video_counter)+'.avi'
    return video_name

def init_video_recorder(h,w,fps):
    fourcc = cv2.cv.FOURCC(*'H264')
    zeros = None
    print "Starting video recording: " + video_name(video_counter)
    writer = cv2.VideoWriter(video_name(video_counter), fourcc, fps, (w, h), True)
    zeros = np.zeros((h, w), dtype="uint8")
    return writer

def deinit_video_recorder(writer):
    print "Stoping video recording"
    writer.release()
    is_video_init=False
    writer = None

def transfer_file(filename):
    #request to connect to storage server
    print "transfer file " + filename
    maxRetries = 20

video_counter=1
is_video_init=False
writer = None
thread1 = None


class MyThread (threading.Thread):

    

    def __init__(self, thread_id, name, video_url, thread_lock):
        threading.Thread.__init__(self)
        self.thread_id = thread_id
        self.name = name 
        self.video_url = video_url
        self.thread_lock = thread_lock
        self._stop = threading.Event()
        
    def run(self):
        print "Starting " + self.name
        window_name = self.name
        cv2.namedWindow(window_name)
        video = cv2.VideoCapture(self.video_url)
        video.set(4,1024)
        firstFrame=None
        is_video_init=False
        writer = None
        #GET FPS
        fps=video.get(cv2.cv.CV_CAP_PROP_FPS)
        MIN_AREA=250

        while True:
            grabbed,frame= video.read()
            text="Unoccupied"

                       
            # resize the frame, convert it to grayscale, and blur it
            frame_resized = imutils.resize(frame, width=500)
            gray = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            # if the first frame is None, initialize it
            if firstFrame is None:
                firstFrame = gray
                continue
                    
            # compute the absolute difference between the current frame and
            # first frame
            frameDelta = cv2.absdiff(firstFrame, gray)
            thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
         
            # dilate the thresholded image to fill in holes, then find contours
            # on thresholded image
            thresh = cv2.dilate(thresh, None, iterations=2)
            (cnts, _) = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE)

            # loop over the contours
            for c in cnts:
                # if the contour is too small, ignore it
                if cv2.contourArea(c) < MIN_AREA:
                    continue
         
                # compute the bounding box for the contour, draw it on the frame,
                # and update the text
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(frame_resized, (x, y), (x + w, y + h), (0, 255, 0), 2)
                text = "Occupied"
                
            global video_counter
            #Intrusion detected!    
            if (text=="Occupied" and is_video_init==False):
                (h, w) = frame.shape[:2]
                writer=init_video_recorder(h,w,fps)
                is_video_init=True
            #During intrusion we record
            if text=="Occupied":
                writer.write(frame)
                #No longer intrusion - We store and transfer
            if text=="Unoccupied" and is_video_init==True:
                deinit_video_recorder(writer)
                transfer_file(video_name(video_counter))
                is_video_init=False
                video_counter+=1

            cv2.putText(frame, "Room Status: {}".format(text), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)    
            cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"), (10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
            cv2.imshow(window_name, frame)
            cv2.imshow("Thresh", thresh)
            cv2.imshow("Frame Delta", frameDelta)
            cv2.imshow("Security Feed", frame_resized)

            #update first frame
            del(firstFrame)
            firstFrame = gray
            del (frame)

            key = cv2.waitKey(50)      
            
            if self._stop.isSet():
                break
            if key == 27:# initialize the first frame in the video stream
    		firstFrame = None

                break
        cv2.destroyAllWindows() 
	cv2.VideoCapture(self.video_url).release()

        print self.name + " Exiting"

    def stop(self):
        self._stop.set()

class IntrusiondetectionImpl:

    @classmethod
    def put(cls, intrusiondetectionschema):
        print str(intrusiondetectionschema)
        print 'handling put'
        if "disarmed" in str(intrusiondetectionschema):
            #sys.exit(0)
            # Stop the thread
            print "Stop thread"
            global thread1
            thread1.stop()
            
        elif "armed" in str(intrusiondetectionschema):	
        	#Start the thread
        	thread_lock = threading.Lock()
        	global thread1
        	thread1 = MyThread(1, "Thread 1", 0, thread_lock)
        	thread1.start()
        	










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


