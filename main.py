
# this is our file
import textToSpeach
import wordSuggestions
import numpy
import math
import keyboard
import time


textToSpeach.setLanguage('danish')
word = ''
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
    
    key = keyboard.read_event()
    if key.event_type == 'down':
        if key.name == 'space':
            word = ''
        elif key.name == 'backspace':
            word = word[:-1]
        elif len(key.name) == 1:
            print(key.name)
            word += key.name
            print('word ', word) 

            print(wordSuggestions.t.autocomplete(word))
