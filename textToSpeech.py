import pyautogui
import pyperclip
import pyttsx3
import time
import re
import keyboard
import threading
from concurrent.futures import ThreadPoolExecutor

isInDanish = True
wordsPerMinute = 300

def setWordsPerMinute(newWordsPerMinute: int) -> None:
    global wordsPerMinute
    wordsPerMinute = newWordsPerMinute

def setLanguage(toDanish:bool) -> None:
    global isInDanish
    isInDanish = toDanish

canceled = False

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

# this function was taken form https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences made by user D Greenberg 19 july 2015
def split_into_sentences(text) -> list:
    text = " " + text + "  "
    text = text.replace("\n"," ")
    text = re.sub(prefixes,"\\1<prd>",text)
    text = re.sub(websites,"<prd>\\1",text)
    text = re.sub(digits + "[.]" + digits,"\\1<prd>\\2",text)
    if "..." in text: text = text.replace("...","<prd><prd><prd>")
    if "Ph.D" in text: text = text.replace("Ph.D.","Ph<prd>D<prd>")
    text = re.sub("\s" + alphabets + "[.] "," \\1<prd> ",text)
    text = re.sub(acronyms+" "+starters,"\\1<stop> \\2",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>\\3<prd>",text)
    text = re.sub(alphabets + "[.]" + alphabets + "[.]","\\1<prd>\\2<prd>",text)
    text = re.sub(" "+suffixes+"[.] "+starters," \\1<stop> \\2",text)
    text = re.sub(" "+suffixes+"[.]"," \\1<prd>",text)
    text = re.sub(" " + alphabets + "[.]"," \\1<prd>",text)
    if "”" in text: text = text.replace(".”","”.")
    if "\"" in text: text = text.replace(".\"","\".")
    if "!" in text: text = text.replace("!\"","\"!")
    if "?" in text: text = text.replace("?\"","\"?")
    text = text.replace(".",".<stop>")
    text = text.replace("?","?<stop>")
    text = text.replace("!","!<stop>")
    text = text.replace("<prd>",".")
    sentences = text.split("<stop>")
    sentences = sentences[:-1]
    sentences = [s.strip() for s in sentences]
    return sentences


    
def setDanish(engine) -> pyttsx3.Engine:
    voices = engine.getProperty('voices')
    
    danishId = ""
    for voice in voices:
        if(voice.name == "Microsoft Helle - Danish (Denmark)"):
            danishId = voice.id
    
    
    if(danishId == ""):
        print("no danish voice found. Continuing in english")
    
    print("Danish: " + danishId)
    
    engine.setProperty('voice', danishId)
    print("Danish set")
    return engine


    
# this function is being called fo run in a different thread than main.
# this is becurse engine.runAndWait() takes a long time to return
def speakSentences(sentences:list[str], stopEvent: threading.Event) -> None:
    engine = pyttsx3.init()
    
    # english is set by default
    if(isInDanish):
        engine = setDanish(engine)
    
    if(wordsPerMinute != 200):
        engine.setProperty('rate', wordsPerMinute)
    
    for sentence in sentences:
        if(stopEvent.is_set()):
            return
        
        engine.say(sentence)
        engine.runAndWait()       
        


def initSpeakSentences(sentences:list[str]) -> None:
    with ThreadPoolExecutor() as executer:
        print(sentences)
        
        # boolean that can be passed by reference to other thread
        stopEvent = threading.Event()
        
        # deferred import to avoid circular import
        from GUI import updateGUI
        
        # Call the speak function in a second thread
        secondThread = executer.submit(speakSentences, sentences, stopEvent)
        
        while (not secondThread.done()):
            updateGUI()
            # if 'p' is pressed, then stop the text to speech
            if(keyboard.is_pressed("p")):
                print("stopping the speech")
                stopEvent.set()
                break
            
            time.sleep(0.01)
            


# TODO this function does not copy the text correctly if the windows where the text is located,
# is inactive. This is very noticeable when using the gui button 
# a possible fix is just to constantly copy what is selected but that seems like a bad solution
def speakSelected() -> None:
    # copy selected text
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.05)
    clipboardText = pyperclip.paste()
    print(clipboardText)
    
    # makes sure the clibordtext ends with either '.','!' or '?'
    lastChar = clipboardText[-1]
    if (lastChar not in ('.','!','?')):
        clipboardText += '.'
    
    sentences = split_into_sentences(clipboardText)
    
    initSpeakSentences(sentences)
    print("done speaking")