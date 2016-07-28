import os.path, sys
sys.path.append(os.path.join('/'.join(os.path.dirname(os.path.realpath(__file__)).split('/')[:-1])))
import backend.backend as be
import pygame

class TriggeralarmImpl:

    @classmethod
    def post(cls, ):
        print 'handling RPC operation'
        if be.alarm:
	    pygame.mixer.init()
	    pygame.mixer.music.load("alarm.wav")
	    pygame.mixer.music.play()
	    while pygame.mixer.music.get_busy()==True:
		continue
	    return be.alarm 
