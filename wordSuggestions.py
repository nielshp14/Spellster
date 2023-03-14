
import numpy as np



fullformWordlist = np.loadtxt("ods_fullforms_2020-08-26.csv", dtype="str", delimiter="\t", encoding='UTF-8', )



def suggestWord(letters):
    letters = letters.lower()

    print("letters: ", letters)
    result = [[],[]]
    for word in fullformWordlist:
        if len(result[0]) >= 5:
            return result
        elif word[0].lower().startswith(letters):
            result[0].append(word[0].lower())
            result[1].append(word[3])

            #print("word: ", word[0].lower(), ", ordklasse", word[3])
        

print(suggestWord("del"))

#print(fullformWordlist[0,3])




#print(fullformWordlist[:100, 0])

