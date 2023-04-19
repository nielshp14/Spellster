import keyboard
import numpy as np
import string

fullform = np.loadtxt("ods_fullforms_2020-08-26.csv", dtype="str", delimiter="\t", encoding='UTF-8', )
misspelled = np.loadtxt("ddo_misspellings_2020-08-26.csv", dtype= "str", delimiter="\t", encoding='UTF-8')
wordFrq = np.loadtxt("lemma-30k-2017.txt", dtype="str", delimiter="\t", encoding="UTF-8")

startSuggestionSize = 3
def suggestions(word, key):
    
    suggestedWords = []
    if key == 'space' or key == 'enter':
                word = ''
    elif key == 'backspace':
                word = word[:-1]
    elif len(key) == 1:
                print(key)
                word += key
                print('word ', word) 

                suggestedWords = t.autocomplete(word)
                print(suggestedWords)
    return word, suggestedWords
def changeSuggestionSize(size):
    t.suggestionSize = size
    
    
word = ''
newestChar = ''
def updateSuggestions():
    global newestChar, word
    
    for key in (list(string.ascii_lowercase) + list(string.digits)+ ['space', 'backspace', 'enter']):
        if keyboard.is_pressed(key) and not newestChar == key:
            newestChar = key
            word, suggestedWords = suggestions(word, key)
            
            
            from GUI import showWords
            showWords(word, suggestedWords)
        
    if (not newestChar == '' and not keyboard.is_pressed(newestChar)):
        newestChar = ''    
    
class Node:
      def __init__(self, char):
        self.char = char
        self.children = {}
        self.endOfWord = False
        self.correctSpelling = ""

class Trie:
    def __init__(self, suggestionSize):
        
        self.root = Node("")
        self.suggestionSize = suggestionSize
        
        
    def insertWord(self, word, correctSpelling): 
      
        node = self.root
        for letter in word: 
            if letter in node.children:
                node = node.children[letter] 
            else:
                newNode  = Node(letter)
                node.children[letter] = newNode
                node = newNode

        node.endOfWord = True # when there are no more letters
        node.correctSpelling = correctSpelling

    def goThrough(self, node, word):
        if node.endOfWord:
            if len(self.output) >= self.suggestionSize:
                return 0 
            self.output.append(node.correctSpelling)
        for child in node.children.values():
            self.goThrough(child, word + node.char)
      
     
                 
    def autocomplete(self, word):
        node = self.root
        self.output = []
        for i, letter in enumerate(word):
            if letter in node.children:
                node = node.children[letter]
            else:
                self.goThrough(node, word[:(i-1)])

                
        self.goThrough(node, word[:-1])

        return self.output
    



t = Trie(startSuggestionSize)

for w in wordFrq[:,1][:]:
    try:
        w = w.strip().lower()
        t.insertWord(w, w) 
    except:
        print(w)
print('first file')
for row in misspelled:
    try:
        
        #w = w.strip().lower()
        t.insertWord(row[0], row[1]) 
    except:
        print(w)
print('second file')
for w in fullform[:,0][:]:
    try:
        w = w.strip().lower()
        t.insertWord(w, w) 
    except:
        print(w)
print('done')


