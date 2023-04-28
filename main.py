import time
import wordSuggestions
import keyboard 

# this is our files
import textToSpeech
import GUI 



while (not keyboard.is_pressed("esc")):
    textToSpeech.speakIfShortcutIsPressed()

    wordSuggestions.updateSuggestions()
    
    
    # Update the GUI 
    GUI.window.update_idletasks() 
    GUI.window.update()
    
    GUI.saveActiveWindow()
    
    # Stop the program
    if(not GUI.GUIOpen): 
        break 
    
    
    # stops the program from using too much computing power
    time.sleep(0.01)