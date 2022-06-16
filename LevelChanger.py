"""
Module will make led lights flash a certain color based on state of DL100 sensor
Sensor Moving: Red
Sensor Ready: Green
Sensor Starting: Blue
Sensor Error: Red, Green, Blue combo

"""

import RPi.GPIO as GPIO
import time
import neopixel
import board



blue = (0, 0, 255)
green = (255, 0, 0)
red = (0, 255, 0)
white = (255, 255, 0)
off = (0, 0, 0)



def led_toggle():
    pixel_pin = board.D21
    num_pixels = 10
    ORDER = neopixel.RGB
    pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)
    
    return pixels


def led_cycle(combo_1, num):
    """
    Function controls the led color sequence
    Param: combo_1: led color based on DL100 State
    Param: num = determines if needs to activate color combo
    """
    global off, red, green, blue
    
    pixels = led_toggle()
    x = 0
    if num == 0:
        while x in range(5):
                pixels.fill(combo_1)
                pixels.show()
                time.sleep(.5)
                    
                pixels.fill(off)
                pixels.show()
                time.sleep(.5)
                
                x += 1
        
    if num == 1:   
        while x in range(5):
                pixels.fill(red)
                pixels.show()
                time.sleep(.5)
                
                pixels.fill(green)
                pixels.show()
                time.sleep(.5)
                
                pixels.fill(blue)
                pixels.show()
                time.sleep(.5)
                    
                pixels.fill(off)
                pixels.show()
                time.sleep(.5)
                
                x += 1
        
        
    
def starting():
    global off, red, green, blue
    
  
    #global blue
    
    GPIO.setmode(GPIO.BCM) #activate GPIO for level changer
    GPIO.setwarnings(False) #deactivate warnings
    
    GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
    time.sleep(.1)
    print('Level Changer On')
    GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
    
    #print('DL100 Starting')
    pixels = led_toggle()
    pixels.fill(blue)
    pixels.show()
    #led_cycle(blue, 0)
    
   

def ready():
    
    global green, off
    
    GPIO.setmode(GPIO.BCM) #activate GPIO for level changer
    GPIO.setwarnings(False) #deactivate warnings
    
    GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
    time.sleep(.05)
    print('Level Changer On')
    GPIO.setup(14, GPIO.OUT, initial=GPIO.HIGH)
    
    print('DL100 Ready')
    
    led_cycle(green, 0)
    

def moving():
               
    global red, off
    
    
    GPIO.setmode(GPIO.BCM) #activate GPIO for level changer
    GPIO.setwarnings(False) #deactivate warnings
    GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
    time.sleep(.05)
    print('Level Changer On')
    GPIO.setup(14, GPIO.OUT, initial=GPIO.HIGH)
    print('Sensor Moving')
    
    led_cycle(red, 0)
    
    
def error():
    
    global blue, red
    
    GPIO.setmode(GPIO.BCM) #activate GPIO for level changer
    GPIO.setwarnings(False) #deactivate warnings
    GPIO.setup(14, GPIO.OUT, initial=GPIO.LOW)
    time.sleep(.05)
    print('Level Changer On')
    GPIO.setup(14, GPIO.OUT, initial=GPIO.HIGH)
    print('DL100 Error!!!!!!')
#   print('Cause by Austin putting cream in his coffee')
    
    led_cycle(red, 1)



GPIO.setmode(GPIO.BCM) #activate GPIO for level changer
GPIO.setwarnings(False) #deactivate warnings

#GPIO.setup(27, GPIO.OUT, initial=GPIO.LOW)
#time.sleep(.1)
print('Level Changer On')
GPIO.setup(27, GPIO.OUT, initial=GPIO.HIGH)
time.sleep(1)

#GPIO.setup(21, GPIO.OUT, initial=GPIO.HIGH)

pixel_pin = board.D21
num_pixels = 23
ORDER = neopixel.RGB
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=1, auto_write=False, pixel_order=ORDER)

for x in range (30):
    pixels.fill((0, 255, 0))
    pixels.show()
    time.sleep(0.1)
    pixels.fill((255, 0, 0))
    pixels.show()
    time.sleep(0.1)
    pixels.fill((0, 0, 255))
    pixels.show()
    time.sleep(0.1)
    pixels.fill((0, 0, 0))
    pixels.show()
    time.sleep(0.1)
    
