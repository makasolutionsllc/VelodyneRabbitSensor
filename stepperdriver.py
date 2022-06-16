import time
import RPi.GPIO as GPIO
#import LevelChanger as led
import rabbitsensor as rb


pul_pin = 6
ena_pin = 13
dir_pin = 5
hall = 17

GPIO.setmode(GPIO.BCM)

GPIO.setup(pul_pin, GPIO.OUT)
GPIO.setup(dir_pin, GPIO.OUT)
GPIO.setup(ena_pin, GPIO.OUT)
GPIO.setup(hall, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print('Initialization Completed')

#testing durations could be changed at a later time
durationFWD = 100
durationBWD = 100

delay = 0.01
cycles = 1000
cyclecount = 0
steptoMM = 1.6 #number of steps to produce 1 mm of distance form system
#            ^^^ Original was 400 steps = 0.8s/m. 
ramp = .002
maxVelocity = 0.00080 #maximum speed

GPIO.output(ena_pin, GPIO.LOW)
time.sleep(0.1)
print('controller enabled')




def moveMotor(direction,distance):
    '''
    param direction; false = lower range value, true farther
    param distance; distance to move in mm
    
    '''
    #led.starting()
    #led.ready()
    speedctl = 75
    if(distance > 600):
        speedctl = 1100 #was 300
    elif(distance < 100):
        speedctl = 3
    steps = int(distance * steptoMM) #calculate # of steps to move
    
    if(direction):
        GPIO.output(dir_pin, GPIO.HIGH)
        #steps = steps+5
        #print('Direction = Closer')
    else:
        GPIO.output(dir_pin, GPIO.LOW)
        #print('Direction = Farther')
        
    time.sleep(0.1)
    stepTime = delay
    #led.moving()
    print('steps',steps)
    
    for x in range(steps):
        rb.Sensor()
        
        GPIO.output(pul_pin, GPIO.HIGH)
        time.sleep(stepTime)
        GPIO.output(pul_pin, GPIO.LOW)
        time.sleep(stepTime)
        
        #speed up for acceleration
        if ((x < speedctl) and (stepTime > maxVelocity)):
            stepTime = stepTime/1.0035
            #print("f:", stepTime)
        elif((x > (steps-speedctl)) and (stepTime < delay)):
            stepTime = stepTime*1.0035
            #print("s:", stepTime)
    
    #led.ready()

for x in range (50):    
    print('Move #',x)
    moveMotor(False,1150)
    time.sleep(10)
    moveMotor(True,1150)
    time.sleep(10)
GPIO.cleanup()

