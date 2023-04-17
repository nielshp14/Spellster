# this is our files
import textToSpeech
import GUI 
import wordSuggestions
import keyboard
import time
import string
from concurrent.futures import ThreadPoolExecutor


# def suggestions(word, key):
   
#     suggestedWords = []
#     if key == 'space':
#                 word = ''
#     elif key == 'backspace':
#                 word = word[:-1]
#     elif len(key) == 1:
#                 print(key)
#                 word += key
#                 print('word ', word) 

#                 suggestedWords = wordSuggestions.t.autocomplete(word)
#                 print(suggestedWords)
#     return word, suggestedWords

word = ''
# with ThreadPoolExecutor() as executer:
#     secondTread = executer.submit(suggestions(word))

#GUI.showWords(word,["Hej", "but", "you", "do", "that", "every", "day"])

newestChar = ''
alreadyStarted = False
while (not keyboard.is_pressed("esc")):
      
        startButton = keyboard.is_pressed("ctrl") and keyboard.is_pressed("å")
        if(startButton and alreadyStarted == False):
            textToSpeech.speakSelected()
            alreadyStarted = True
     
        if(startButton == False):
            alreadyStarted = False
        
        for key in (list(string.ascii_lowercase) + list(string.digits)+ ['space', 'backspace', 'enter']):
            if keyboard.is_pressed(key) and not newestChar == key:
                newestChar = key
                word, suggestedWords = wordSuggestions.suggestions(word, key)
                GUI.showWords(word, suggestedWords)
        
        if (not newestChar == '' and not keyboard.is_pressed(newestChar)):
              newestChar = ''
        

        # Update the GUI 
        GUI.window.update_idletasks() 
        GUI.window.update()
        
        # Stop the program 
        if(not GUI.GUIOpen): 
            break 
        
        # stops the program from using too much computing power
        time.sleep(0.01)