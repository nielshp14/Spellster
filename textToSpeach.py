import pyautogui
import pyperclip
import pyttsx3
import time
import re
import keyboard
from concurrent.futures import ThreadPoolExecutor

# creates ttx engine
engine = pyttsx3.init()

canseled = False

alphabets= "([A-Za-z])"
prefixes = "(Mr|St|Mrs|Ms|Dr)[.]"
suffixes = "(Inc|Ltd|Jr|Sr|Co)"
starters = "(Mr|Mrs|Ms|Dr|He\s|She\s|It\s|They\s|Their\s|Our\s|We\s|But\s|However\s|That\s|This\s|Wherever)"
acronyms = "([A-Z][.][A-Z][.](?:[A-Z][.])?)"
websites = "[.](com|net|org|io|gov)"
digits = "([0-9])"

# this funktion was taken form https://stackoverflow.com/questions/4576077/how-can-i-split-a-text-into-sentences made by user D Greenberg 19 july 2015
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

def setWordsPerMinut(wordsPerMinut: int):
    engine.setProperty('rate', wordsPerMinut)
    
def setLanguage(language:str) -> None:
    voices = engine.getProperty('voices')
    
    danishId = ""
    englishId = ""
    for voice in voices:
        print(voice.name)
        if(voice.name == "Microsoft Helle - Danish (Denmark)"):
            danishId = voice.id
        elif (voice.name == "Microsoft Hazel Desktop - English (Great Britain)"):
            englishId = voice.id
            
    print("Danish: " + danishId)
    print("English: " + englishId)
    
    if (language == "danish"):
        engine.setProperty('voice', danishId)
        print("Danish set")
    
    if (language == "english"):
        engine.setProperty('voice', englishId)
        print("Englis set")

# funktion is beeing called on a seperate thread 
def chekForCanseled() -> None:
    global canseled
    while (True):
        cansleShortCut = keyboard.is_pressed("p")
        if(cansleShortCut or canseled):
            print("stoping the speach")
            canseled = True
            break
        time.sleep(0.01)
    

def speakSelectet() -> None:
    global canseled 
    canseled = False
    
    # copy selectet text
    pyautogui.hotkey('ctrl','c')
    time.sleep(0.01)
    clibordText = pyperclip.paste()
    
    # makes sure the clibordtext ends with either '.','!' or '?'
    lastChar = clibordText[len(clibordText)-1]
    if (not (lastChar == '.' or lastChar == '!' or lastChar == '?')):
        clibordText += '.'
    
    sentences = split_into_sentences(clibordText)
    
    with ThreadPoolExecutor() as executer:
        # calls chekForCanseled on a seperate thread
        executer.submit(chekForCanseled)
        
        # Say sentences on at a time
        for sentence in sentences:
            if (canseled):
                break
            print("saying: " + str(sentence) + " \n")
            engine.say(sentence)
            engine.runAndWait()
        
        # Stopes the second tread
        canseled = True