#RPi based Coronavirus Test/Vaccine delivery sys
#auth - fin mead
#desc - a script controlling the main functionality of the transport system

## Declarations 

#Imports
import RPi.GPIO as GPIO
from picamera import PiCamera
from time import sleep

#Externals - From drone and internet i.e telem data, patientID from app/website - some parts yet to be implemented [psuedo: droneActivity relates to drone and QGround Control, jobActivity relates to App/website]
patientID = jobActivity.getPatientID()
status = droneActivty.status()
destination = droneActivity.waypoint() #handled by QGroundcontrol?
startPoint = droneActivity.startPoint()


#Definitions - local variables; bool, int, method [declarations]
camera = PiCamera()
landed = False
collected = False
delivered = False

#Setup for GPIO - servos and limit switch stuff
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.setup(10, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(12, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(3, GPIO.OUT)
pwm=GPIO.PWM(3, 50)
pwm.start(0)

##

#Methods

def setPos(angle):
    duty = angle/18+2
    GPIO.output(3, True)
    pwm.ChangeDutyCycle(duty)
    sleep(1)
    GPIO.output(3, False)
    pwm.ChangeDutyCycle(0)

def sense_payload(): # decides whether to open or close the servo and register activities based on limit switch/servo positions
    if GPIO.input(10) == GPIO.LOW:
        print("PAYLOAD AQUIRED")
        setPos(40)
        if bool(collected) == False:
            print("collecting")
            registerCollection()
    
    if GPIO.input(10) == GPIO.HIGH and GPIO.input(12) == GPIO.LOW:
        print("NO PAYLOAD, OPEN")
        setPos(120)
        if delivered == False:
            registerDelivery()
        
    if GPIO.input(12) == GPIO.LOW:
        landed = True
        print("IDLE, landed =")
        print(landed)
        
    if GPIO.input(12) == GPIO.HIGH:
        landed = False
        print("IN FLIGHT, landed =")
        print(landed)
        
def registerCollection(): # register the collection by taking a photo when human triggers payload acceptance (payload is aquired)
    camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/Desktop/covid drone/' + patientID + ' delivery_%s.jpg' % i)
    camera.stop_preview()
    print("collection registered: Patient ID: " + patientID)
    collected = True
    print(collected)
    
def registerDelivery(): # register the delivery by taking a photo when human triggers payload release
    camera.start_preview()
    sleep(1)
    camera.capture('/home/pi/Desktop/covid drone/' + patientID + 'collection_%s.jpg' % i)
    camera.stop_preview()
    print("delivery registered: Patient ID: "  + patientID)
    delivered = True
        
        
        
#getTheBallRolling        
while True:
    sense_payload()
    