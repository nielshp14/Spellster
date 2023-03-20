
# this is our file
import textToSpeach
import GUI 

import numpy
import math
import keyboard
import time


textToSpeach.setLanguage('english')

alreadyStarted = False
while (keyboard.is_pressed("esc") == False):
    startButton = keyboard.is_pressed("ctrl") and keyboard.is_pressed("å")
    
    if(startButton and alreadyStarted == False):
        textToSpeach.speakSelectet()
        alreadyStarted = True
    
    if(startButton == False):
        alreadyStarted = False
    
    
    # Update the GUI
    GUI.window.update_idletasks()
    GUI.window.update()
    
    # stops the program from using too much computing power
    time.sleep(0.05)
    
