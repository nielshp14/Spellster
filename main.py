
# this is our file
import textToSpeach

import numpy
import math
import keyboard
import time


alreadyStarted = False

while (keyboard.is_pressed("esc") == False):
    startButton = keyboard.is_pressed("å") and keyboard.is_pressed("ctrl")
    
    if(startButton and alreadyStarted == False):
        textToSpeach.speakSelectet()
        alreadyStarted = True
    
    if(startButton == False):
        alreadyStarted = False
    
    # stops the program from using too much computing power
    time.sleep(0.05)
    