#!/usr/bin/python
#Example using a character LCD connnected to a Rapsberry Pi
import time
import threading
import Adafruit_CharLCD as LCD
import RPi.GPIO as GPIO
import os
from datetime import datetime
from pytz import timezone
from tzlocal import get_localzone
#configure the GPIO used for the LEDs
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(16,GPIO.OUT)
GPIO.setup(11,GPIO.OUT)
#Raspberry Pi pin configuration:
lcd_rs=25
lcd_en=24
lcd_d4=23
lcd_d5=17
lcd_d6=18
lcd_d7=22
lcd_backlight=4
lcd_columns=16
lcd_rows=2
#define LCD column and row size for 16x2 LCD
lcd_columns=16
lcd_rows=2
#initialize the LCD using the pins above
lcd=LCD.Adafruit_CharLCD(lcd_rs,lcd_en,lcd_d4,lcd_d5,lcd_d6,lcd_d7,lcd_columns,lcd_rows,lcd_backlight)
#define the text file where the weather output is stored
datafile=file('output.txt')
weather=''#empty string that will store the current weather
sound=''#empty string that will store the current sound to be played
#function to get the current time in hours,minutes,seconds,am/pm format in the correct timezone
def getcurrenttime():
    Format='%H:%M:%S%P'
    now_utc=datetime.now(timezone('UTC'))
    now_local=now_utc.astimezone(get_localzone())
    #print the time and weather to the LCD
    lcd.message('Time:'+now_local.strftime(format)+'\nWeather:'+weather)
    #play the weather sound
    os.system('mpg321 '+sound+' &')
    #sleep for one second
    time.sleep(1)
    #refresh the LCD
    lcd.clear()
#check what the current weather is
for line in datafile:
    if 'clear' in line:
        weather='Sunny'
        sound='sunshinesound.mp3'
        GPIO.output(11,GPIO.HIGH)
        GPIO.output(16,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
    if 'cloudy' in line:
        weather='Cloudy'
        sound='wind-sand.mp3'
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
    if 'overcast' in line:
        weather='Cloudy'
        sound='wind-sand.mp3'
        GPIO.output(16,GPIO.HIGH)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(21,GPIO.LOW)
    if 'rain' in line:
        weather='Rain'
        sound='rainSound.mp3'
        GPIO.output(16,GPIO.LOW)
        GPIO.output(11,GPIO.LOW)
        GPIO.output(21,GPIO.HIGH)
turnedOn=True
while turnedOn==True:
    getcurrenttime()
