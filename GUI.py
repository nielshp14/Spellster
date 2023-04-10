import tkinter as tk
from typing import Callable, Union

window = tk.Tk()
suggestionPanel = tk.Frame(window,height=40,width=10,bg="red")
optionPanel = tk.Frame(window)

optionsOpened = False

window.title("Spellster")

GUIOpen = True
fontSize = 12

# set windows always on top
window.attributes("-topmost", True)

# delead the existing title bar
window.overrideredirect(True)


titleBar = tk.Frame(window, relief="raised", bd=1)
titleBar.grid(sticky='EW')

suggestionPanel.grid(sticky='ew')


def setupTitleBar() -> None:
    def moveApp(event):
        window.geometry("+" + str(event.x_root) + "+" + str(event.y_root))
        pass

    # <B1-Motion> is when the moused is dragged on the titleBar with mouse button 1
    titleBar.bind("<B1-Motion>", moveApp)


    def playPressed():
        from textToSpeech import speakSelected
        speakSelected()
        print("Play button has been pressed")

    playButton = tk.Button(titleBar, text="p", height=1, width=3, command=playPressed)
    playButton.grid(row=0,column=0)


    def optionPressed():
        if (not optionsOpened):
            openOptions()
            print("options Opened")
        else:
            closeOptions()
            print("options closed")
        print("Options button has been pressed")

    optionButton = tk.Button(titleBar, text="o", height=1, width=3, command=optionPressed)
    optionButton.grid(row=0,column=1)


    def languagePressed():
        from textToSpeech import setLanguage,isInDanish
        setLanguage(not isInDanish)
        print("Language button has been pressed")

    languageButton = tk.Button(titleBar, text="L", height=1, width=3, command=languagePressed)
    languageButton.grid(row=0,column=2)


    # adds empty space for column nr 3
    titleBar.columnconfigure(3, minsize=120)


    def closeWindow():
        global GUIOpen
        
        window.destroy()
        GUIOpen = False
        print("close")

    # add close button
    closeWindow = tk.Button(titleBar, text="X", background="red", height=1, width=3,  command=closeWindow)
    closeWindow.grid(row=0, column=4)

setupTitleBar()
# -------------------------------- configure options panel

class Option:
    def __init__(self,parentFrame,text: str,gridRow: int, command: Callable[[Union[tk.Event,None],tk.StringVar],None], startValue:str = ""):
        self.label = tk.Label(parentFrame,text=text,font=('Arial', fontSize),anchor="w")
        self.label.grid(column=0,row=gridRow)

        self.command = command

        self.optionVariable = tk.StringVar()
        self.optionInput = tk.Entry(parentFrame,textvariable=self.optionVariable,font=('Arial', fontSize),width=10,justify="right")
        self.optionInput.insert(0,startValue)
        self.optionInput.bind("<FocusOut>",lambda event: command(event,self.optionInput))
        self.optionInput.grid(column=1,row=gridRow)
    
    def lockOption(self):
        self.optionInput.config(state="disabled")
    
    def unlockOption(self):
        self.optionInput.config(state="normal")
    
    def saveOption(self):
        self.command(None,self.optionVariable)



fontSizeOption: Option
wordsPerMinuteOption: Option
suggestionAmountOption: Option


def setupOptionPanel() -> None:
    def fontSizeChange(event: Union[tk.Event,None],optionResult:tk.StringVar):
        newFontSize: str = optionResult.get()
        if(not newFontSize.isdigit()):
            print("please insert valid number")
            return
        
        global fontSize
        fontSize = int(newFontSize)
        print("new font Size: " + str(fontSize))

    global fontSizeOption
    fontSizeOption = Option(optionPanel,"FontSize:                   ",0,fontSizeChange,str(fontSize))

    def wordsPerMinuteChange(event: Union[tk.Event,None],optionResult:tk.StringVar):
        newWordsPerMinute:str = optionResult.get()
        if(not newWordsPerMinute.isdigit()):
            print("please insert valid number")
            return
        
        newWordsPerMinute: int = int(newWordsPerMinute)
        print("new words per minute: " + str(newWordsPerMinute))

        from textToSpeech import setWordsPerMinute
        setWordsPerMinute(newWordsPerMinute)

    from textToSpeech import wordsPerMinute
    global wordsPerMinuteOption
    wordsPerMinuteOption = Option(optionPanel,"Words per minute:    ", 1, wordsPerMinuteChange, str(wordsPerMinute))


    def suggestionAmountChange(event: Union[tk.Event,None],optionResult:tk.StringVar):
        newSuggestionAmount: str = optionResult.get()
        if(not newSuggestionAmount.isdigit()):
            print("please insert valid number")
            return
        
        newSuggestionAmount: int = int(newSuggestionAmount)
        print("new suggestionAmount: " + str(newSuggestionAmount))
    
    global suggestionAmountOption
    suggestionAmountOption = Option(optionPanel,"Suggestion size:        ",2,suggestionAmountChange)


    onTopLabel = tk.Label(optionPanel,text="Show window on top:",font=('Arial', fontSize),anchor="w")
    onTopLabel.grid(column=0, row=3)

    onTopVar = tk.IntVar(value=1)

    def onTopChange():
        onTop = onTopVar.get()
        if (onTop == 1):
            window.attributes("-topmost", True)
        else:
            window.attributes("-topmost", False)

    onTopCheckbox = tk.Checkbutton(optionPanel,variable=onTopVar,onvalue=1,offvalue=0,command=onTopChange)
    onTopCheckbox.grid(column=1,row=3)
    





setupOptionPanel()

def openOptions() -> None:
    global optionsOpened

    fontSizeOption.unlockOption()
    wordsPerMinuteOption.unlockOption()
    suggestionAmountOption.unlockOption()
    
    suggestionPanel.grid_forget()
    optionPanel.grid(sticky="ew")
    optionsOpened = True

def closeOptions() -> None:
    global optionsOpened

    fontSizeOption.saveOption()
    fontSizeOption.lockOption()
    wordsPerMinuteOption.saveOption()
    wordsPerMinuteOption.lockOption()
    suggestionAmountOption.saveOption()
    suggestionAmountOption.lockOption()

    optionPanel.grid_forget()
    suggestionPanel.grid(sticky='ew')
    optionsOpened = False



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

