
# this is our files
import textToSpeech
import GUI 

import keyboard
import time

# GUI.showWords(["Hej", "med", "dig.", "you", "be", "lokking", "cute", "today.", "but", "you", "do", "that", "avry", "day"])

alreadyStarted = False
while (not keyboard.is_pressed("esc")):
 
    startButton = keyboard.is_pressed("ctrl") and keyboard.is_pressed("å")
    if(startButton and alreadyStarted == False):
        textToSpeech.speakSelected()
        alreadyStarted = True
    
    if(startButton == False):
        alreadyStarted = False
    
    if(keyboard.is_pressed('b')):
        GUI.clearWords()
    
    # Update the GUI
    GUI.window.update_idletasks()
    GUI.window.update()
    
    # Stop the program
    if(not GUI.GUIOpen):
        break
    
    # stops the program from using too much computing power
    time.sleep(0.01)