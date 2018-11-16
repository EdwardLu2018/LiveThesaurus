from Word import *

firstWord = Word("set")
print("Synonym Dictionary for: \"" + firstWord.word + "\":")
if firstWord.isValidWord():
    print(firstWord.getSynonymDict())
else:
    print("Not a word!")