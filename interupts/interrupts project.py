#!/usr/bin/env python
#code from https://circuitdigest.com/microcontroller-projects/raspberry-pi-adc-tutorial
# code fromhttps://www.sunfounder.com/learn/Basic-Kit-for-Raspberry-Pi/basic-kit-for-rpi11.html
# changes by eric jones

#import tools because u need them to make it work
import RPi.GPIO as IO
import Adafruit_CharLCD as LCD
import subprocess
import ADC0832
import time

lcd = LCD.Adafruit_CharLCDPlate()

#eliminate warnings
IO.setwarnings(False)

#addd pin config stuff use pin 5 instead of 29
IO.setmode(IO.BCM)

# set pin config
IO.setup(18, IO.IN)
IO.setup(23, IO.IN)
IO.setup(24, IO.IN)
ADC0832.setup()
IO.setup(4, IO.IN, pull_up_down=IO.PUD_UP)
IO.setup(22, IO.IN, pull_up_down=IO.PUD_UP)

Name = subprocess.check_output(['hostname']).strip()
displaytext = Name
IPaddr = subprocess.check_output(['hostname', '-I']).split()
display = IPaddr


def my_callback(channel):
        global ADC0832
        res = ADC0832.getResult()
        v = res * (3.3 / 255)
        print ('Current voltage: %.2f V' % v)
        time.sleep(0.2)


def my_callback2(channel):
    lcd.clear
    lcd.message(displaytext)
    refresh = True

    IO.add_event_detect(4, IO.FALLING, callback=my_callback2, bouncetime=300)
    IO.add_event_detect(22, IO.FALLING, callback=my_callback, bouncetime=300)

    while(True):
        pass