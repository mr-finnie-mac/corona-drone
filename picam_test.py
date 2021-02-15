#RPi PiCam Test Script
#Auth: Fin Mead [Meadeor]
#Desc: PiCam test script for Covid-19 project

#Imports
from picamera import PiCamera
from time import sleep

#Def
camera = PiCamera()

#c o n t e n t

def prev(): # display camera window for 1 minute
    camera.start_preview() 
    sleep(60)
    camera.stop_preview()
    
    
def pic(): # ntake a picture after 5 seconds
    camera.start_preview()
    sleep(3)
    camera.capture('/home/pi/Desktop/PiPic2.jpg')
    camera.stop_preview()
    
def seq(): # take 5 pictures with 2 second intervals
    camera.start_preview()
    for i in range(5):
        sleep(2)
        camera.capture('/home/pi/Desktop/firstSequenceImages_%s.jpg' % i)
    camera.stop_preview()

def rec(): # record 5 seconds of video
    camera.start_preview()
    sleep (2)
    camera.start_recording('/home/pi/Desktop/video1.h264')
    sleep(10)
    camera.stop_recording()
    sleep(2)
    camera.stop_preview()


pic()
#pic()
#seq()
#rec()
    
