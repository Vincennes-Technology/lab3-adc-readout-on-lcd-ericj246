#!/usr/bin/env python
#code from https://circuitdigest.com/microcontroller-projects/raspberry-pi-adc-tutorial
# code fromhttps://www.sunfounder.com/learn/Basic-Kit-for-Raspberry-Pi/basic-kit-for-rpi11.html
# changes by eric jones


import RPi.GPIO as GPIO
import subprocess
import time
import Adafruit_CharLCD as LCD
import ADC0832
GPIO.setmode(GPIO.BCM)
lcd = LCD.Adafruit_CharLCDPlate()
while True:
 IPaddr = subprocess.check_output(['hostname','-I'])
 if len(IPaddr) > 8:
  break
 else:
  time.sleep(2)
Name = subprocess.check_output(['hostname']).strip()
displayText = IPaddr + Name
Select = False
oldmessage = None
# GPIO 23 & 24 set up as inputs, pulled up to avoid false detection.
# Both ports are wired to connect to GND on button press.
# So we'll be setting up falling edge detection for both
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

# now we'll define two threaded callback functions
# these will run in another thread when our events are detected
def my_callbackIP(channel):
    global Select
    #print "falling edge detected on 24"
    Select = False
def my_callbackADC(channel):
    global Select
    #print "falling edge detected on 23"
    Select = True

# when a falling edge is detected on port 24, regardless of whatever
# else is happening in the program, the function my_callback will be run
GPIO.add_event_detect(24, GPIO.FALLING, callback=my_callbackIP, bouncetime=300)
# when a falling edge is detected on port 23, regardless of whatever
# else is happening in the program, the function my_callback2 will be run
# 'bouncetime=300' includes the bounce control written into interrupts2a.py
GPIO.add_event_detect(23, GPIO.FALLING, callback=my_callbackADC, bouncetime=300)
try:
    while True:
        if Select:
            value = ADC0832.getADC(0)
            VoltText = 'current voltage\n %f' % value
            Thismessage = VoltText
        else :
            Thismessage = displayText
        if oldmessage == Thismessage:
            pass
        else:
            lcd.clear()
            lcd.message(Thismessage)
            oldmessage = Thismessage
        time.sleep(0.2)


except KeyboardInterrupt:
    GPIO.cleanup()       # clean up GPIO on CTRL+C exit
GPIO.cleanup()           # clean up GPIO on normal exit

