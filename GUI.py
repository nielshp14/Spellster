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
suggestionPanel.grid(sticky='ew')

testButton = tk.Button(suggestionPanel,text="test")
testButton.pack(fill='x',anchor='w')
testButton2 = tk.Button(suggestionPanel,text="test")
testButton2.pack(fill='x',anchor='w')

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

# -------------------------------- configure suggestionPanel

def buttonPressed(word: str):
    print(word)

fontSize = 12
wordsSuggestions = []
def showWords(words: list[str]):
    clearWords()
    suggestionPanel.grid()
    for i,word in enumerate(words):
        callback = lambda word=word: buttonPressed(word)
        suggestionButton = tk.Button(suggestionPanel, text=word, font=('Arial', fontSize), command=callback, anchor=tk.W)
        suggestionButton.grid(column=0,row=i,sticky="nsew")
        wordsSuggestions.append(suggestionButton)


def clearWords():
    suggestionPanel.grid_forget()
    for suggestion in wordsSuggestions:
        suggestion.destroy()
        





