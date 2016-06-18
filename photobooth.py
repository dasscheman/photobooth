#!/usr/bin/env python

import RPi.GPIO as GPIO
import atexit
import config
import glob
import os
import subprocess
import sys
import time
from time import sleep

########################
### Variables Config ###
########################
led1_pin_get_ready = 15 # LED 1
led2_pin_smile = 19 # LED 2
led3_pin_process = 21 # LED 3
led4_pin_print = 23 # LED 4
led5_pin_button = 13
button1_pin_start = 22 # pin for the big red button
button2_pin_shutdown = 18 # pin for button to shutdown the pi
button3_pin_reset = 16 # pin for button to end the program, but not shutdown the pi

####################
### Other Config ###
####################
GPIO.setmode(GPIO.BOARD)
GPIO.setup(led1_pin_get_ready, GPIO.OUT) # LED 1
GPIO.setup(led2_pin_smile, GPIO.OUT) # LED 2
GPIO.setup(led3_pin_process, GPIO.OUT) # LED 3
GPIO.setup(led4_pin_print, GPIO.OUT) # LED 4
GPIO.setup(led5_pin_button, GPIO.OUT) # LED 5
GPIO.setup(button1_pin_start, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 1
GPIO.setup(button2_pin_shutdown, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 2
GPIO.setup(button3_pin_reset, GPIO.IN, pull_up_down=GPIO.PUD_UP) # falling edge detection on button 3
GPIO.output(led1_pin_get_ready, False);
GPIO.output(led2_pin_smile, False);
GPIO.output(led3_pin_process, False);
GPIO.output(led4_pin_print, False);
GPIO.output(led5_pin_button, False); #for some reason the pin turns on at the beginning of the program. why?????????????????????????????????

#################
### Functions ###
#################

def cleanup():
  print('Ended abruptly')
  GPIO.cleanup()
atexit.register(cleanup)

def shut_it_down(channel):  
  print "Shutting down..." 
  GPIO.output(led1_pin_get_ready, True);
  GPIO.output(led2_pin_smile, True);
  GPIO.output(led3_pin_process, True);
  GPIO.output(led4_pin_print, True);
  GPIO.output(led5_pin_button, True);
  time.sleep(3)
  os.system("sudo halt")

def exit_photobooth(channel):
  print "Photo booth app ended. RPi still running" 
  GPIO.output(led1_pin_get_ready, True);
  time.sleep(3)
  sys.exit()
    
def clear_pics(foo): #why is this function being passed an arguments?
  #delete files in folder on startup
    files = glob.glob(config.file_path + '*')
    for f in files:
      os.remove(f) 
    #light the lights in series to show completed
    print "Deleted previous pics"
    GPIO.output(led1_pin_get_ready, False); #turn off the lights
    GPIO.output(led2_pin_smile, False);
    GPIO.output(led3_pin_process, False);
    GPIO.output(led4_pin_print, False);
    GPIO.output(led5_pin_button, False);
    pins = [led1_pin_get_ready, led2_pin_smile, led3_pin_process, led4_pin_print, led5_pin_button]
    for p in pins:
      GPIO.output(p, True); 
      sleep(0.25)
      GPIO.output(p, False);
      sleep(0.25) 
				
# define the photo taking function for when the big button is pressed 
def start_photobooth(): 
  
  GPIO.output(led5_pin_button, False)
  # delete files in folder on startup
  files = glob.glob(config.file_path + '*')
  for f in files:
    os.remove(f)
  ################################# Begin Step 1 ################################# 
  print "Get Ready"
  GPIO.output(led1_pin_get_ready, True);
  sleep(config.prep_delay) 
  sleep(2) #warm up camera
  GPIO.output(led1_pin_get_ready, False)
        
  ################################# Begin Step 2 #################################
  print "Taking pics" 
  for i in range(0, config.total_pics):
      GPIO.output(led2_pin_smile, True) #turn on the LED
      now = time.strftime("%Y-%m-%d-%H:%M:%S") #get the current date and time for the start of the filename
      gpout = subprocess.check_output("gphoto2 --capture-image-and-download --filename " + config.file_path + now + ".jpg", stderr=subprocess.STDOUT, shell=True)
      print(gpout)
      sleep(0.25) #pause the LED on for just a bit
      GPIO.output(led2_pin_smile, False) #turn off the LED
      sleep(config.capture_delay) # pause in-between shots
      if i == config.total_pics-1:
        break

  ########################### Begin Step 3 #################################  
  if config.post_online:
      print "Creating an animated gif" 

      GPIO.output(led3_pin_process, True) #turn on the LED
      graphicsmagick = "gm convert -delay " + str(config.gif_delay) + " " + config.file_path + "*.jpg " + config.file_path_gif + now + ".gif" 
      os.system(graphicsmagick) #make the .gif
      print "Uploading to pibooth."

      GPIO.output(led3_pin_process, False) #turn off the LED
	
  ########################### Begin Step 4 #################################
	
  subprocess.call("sudo /home/pi/scripts/photobooth/assemble.sh", shell=True)
  if config.print_pic:
      print "Start printing"
      GPIO.output(led4_pin_print, True) #turn on the LED
      subprocess.call("sudo /home/pi/scripts/photobooth/print.sh", shell=True)
      GPIO.output(led4_pin_print, False) #turn off the LED

  time.sleep(config.restart_delay)
  GPIO.output(led5_pin_button, True)

####################
### Main Program ###
####################

# when a falling edge is detected on button2_pin and button3_pin, regardless of whatever   
# else is happening in the program, their function will be run   
GPIO.add_event_detect(button2_pin_shutdown, GPIO.FALLING, callback=shut_it_down, bouncetime=300) 

#choose one of the two following lines to be un-commented
GPIO.add_event_detect(button3_pin_reset, GPIO.FALLING, callback=exit_photobooth, bouncetime=300) #use third button to exit python. Good while developing
#GPIO.add_event_detect(button3_pin, GPIO.FALLING, callback=clear_pics, bouncetime=300) #use the third button to clear pics stored on the SD card from previous events

print "Photo booth app running..." 
GPIO.output(led1_pin_get_ready, True); #light up the lights to show the app is running
GPIO.output(led2_pin_smile, True);
GPIO.output(led3_pin_process, True);
GPIO.output(led4_pin_print, True);
GPIO.output(led5_pin_button, True);
time.sleep(3)
GPIO.output(led1_pin_get_ready, False); #turn off the lights
GPIO.output(led2_pin_smile, False);
GPIO.output(led3_pin_process, False);
GPIO.output(led4_pin_print, False);
GPIO.output(led5_pin_button, False);

while True:
    GPIO.wait_for_edge(button1_pin_start, GPIO.FALLING)
    time.sleep(0.2) #debounce
    start_photobooth()
