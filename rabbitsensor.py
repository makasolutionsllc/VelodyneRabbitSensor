"""
Module is for the 55100 sensor attached to the RPI
If sensor touches magnet it will tell the rabbit to stop moving and
activate error led combo
"""



import RPi.GPIO as GPIO
import time
import neopixel
import board
import LevelChanger as led


pin = 17 #GPIO pin sensor is connected to


def my_callback():
    """
    Protocol when sensor has been activated
    param: pin: GPIP pin sensor is connected to
    """
    pin = 17
    detect = GPIO.event_detected(pin)
    ena_pin = 5
    if detect == True:
        #<----will place stop cmd for rabbit      
        print('Magnet Detected')
        GPIO.output(ena_pin, GPIO.LOW)
        GPIO.cleanup()
        
                
    
    

def Sensor():
    
    global pin
    ena_pin = 5
    
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    
    if GPIO.input(pin): #test GPIO input
        print("Input set high")
    else:
        print("Input set low")
    
    
    #places gpio pin into waiting status until it detects magnet
    #todo this function will start when rabbit is moving, timeout maybe adjusted with range loop
    
    GPIO.add_event_detect(pin, GPIO.RISING, callback=my_callback, bouncetime=10000)
    
    '''
    while(True):
        try:
            print('Magnet Detected')
            GPIO.output(ena_pin, GPIO.LOW)
            #led.error()
            GPIO.cleanup()
        except Exception as e:
            print(e)
    '''  
    #adding rising edge detection on a pin
    #time.sleep(.05)
    #GPIO.add_event_detect(pin, GPIO.BOTH, callback=my_callback)
    #time.sleep(1)
    
    
    
        


#Sensor()
    

