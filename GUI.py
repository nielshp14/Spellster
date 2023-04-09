import tkinter as tk

import textToSpeech 
window = tk.Tk()
window.title("Spellster")

GUIOpen = True

# set windows always on top
window.attributes("-topmost", True)

# delead the existing title bar
window.overrideredirect(True)


titleBar = tk.Frame(window, relief="raised", bd=1)
titleBar.grid(sticky='EW')

suggestionPanel = tk.Frame(window,height=40,width=10,bg="red")
# suggestionPanel.grid(sticky='ew')


# ----------------------------------- configure titleBar
def moveApp(event):
    window.geometry("+" + str(event.x_root) + "+" + str(event.y_root))
    pass

# <B1-Motion> is when the moused is dragged on the titleBar with mouse button 1
titleBar.bind("<B1-Motion>", moveApp)


def playPressed():
    textToSpeech.speakSelected()
    print("Play button has been pressed")

playButton = tk.Button(titleBar, text="p", height=1, width=3, command=playPressed)
playButton.grid(row=0,column=0)


def optionPressed():
    clearWords()
    print("Options button has been pressed")

optionButton = tk.Button(titleBar, text="o", height=1, width=3, command=optionPressed)
optionButton.grid(row=0,column=1)


def languagePressed():
    print("Language button has been pressed")

languageButton = tk.Button(titleBar, text="L", height=1, width=3, command=languagePressed)
languageButton.grid(row=0,column=2)


# adds empty space for column nr 3
titleBar.columnconfigure(3, minsize=100)


def closeWindow():
    global GUIOpen
    
    window.destroy()
    GUIOpen = False
    print("close")

# add close button
closeWindow = tk.Button(titleBar, text="X", background="red", height=1, width=3,  command=closeWindow)
closeWindow.grid(row=0, column=4)


# -------------------------------- configure options panel

optionPanel = tk.Frame(window)
optionPanel.grid(sticky="ew")


fontSizeLabel = tk.Label(optionPanel,text="Font Size:               ")
fontSizeLabel.grid(column=0,row=0)


fontSizeVariable = tk.StringVar() 

def fontSizeChange(event) -> None:
    newFontSize = fontSizeVariable.get()
    print("New font size: " + newFontSize)
    
fontSizeInput = tk.Entry(optionPanel, textvariable=fontSizeVariable, width=10)
fontSizeInput.bind("<FocusOut>",fontSizeChange)
fontSizeInput.grid(column=1,row=0)


wordsPerMinuteLabel = tk.Label(optionPanel,text="Words Per Minute: ")
wordsPerMinuteLabel.grid(column=0,row=1)


wordsPerMinuteVariable = tk.StringVar() 

def setupWPM():
    

    def wordsPerMinuteChange(event) -> None:
        newWordsPerMinute = wordsPerMinuteVariable.get()
        print("New words er minute: " + newWordsPerMinute)
        
    wordsPerMinuteInput = tk.Entry(optionPanel, textvariable=wordsPerMinuteVariable, width=10)
    # Call wordsPerMinuteChange when the input losses focus
    wordsPerMinuteInput.bind("<FocusOut>",wordsPerMinuteChange)
    wordsPerMinuteInput.grid(column=1,row=1)

    # TODO Der er en error som gør at nedestående kode ikke fungere. Der står at det mugeligthis er en circular import error


    wordsPerMinute = textToSpeech.getWordsPerMinute() # could it be that this is used before anything ells regarding textToSpeach
    wordsPerMinuteInput.insert(0,200)


suggestionAmountLabel = tk.Label(optionPanel, text="Suggestion amount: ")
suggestionAmountLabel.grid(column=0,row=2)

suggestionAmountVariable = tk.StringVar()

def suggestionAmountChange(event):
    newSuggestionAmount = suggestionAmountVariable.get()
    print("New suggestionAmount: " + newSuggestionAmount)

suggestionAmountInput = tk.Entry(optionPanel, textvariable=suggestionAmountVariable, width=10)
suggestionAmountInput.bind("<FocusOut>", suggestionAmountChange)
suggestionAmountInput.grid(column=1,row=2)

# TODO få skrevet options koden smartere. fx kunne man lave en class som hed option. Men jeg skal nok vente til at at jeg har fået fixet den to do som er for oven

# -------------------------------- configure suggestionPanel

def buttonPressed(word: str):
    print(word)

fontSize = 12
wordsSuggestions = []
def showWords(words: list[str]):
    clearWords()

    for i,word in enumerate(words):
        callback = lambda word=word: buttonPressed(word)
        suggestionButton = tk.Button(suggestionPanel, text=word, font=('Arial', fontSize), command=callback, anchor=tk.W)
        suggestionButton.pack(fill='x', anchor='w')
        wordsSuggestions.append(suggestionButton)


def clearWords():
    for suggestion in wordsSuggestions:
        suggestion.destroy()
        


def updateGUI():
    window.update_idletasks()
    window.update()


setupWPM()