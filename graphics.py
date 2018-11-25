from tkinter import *
from Word import *
import audio as speechRecognizer

class LiveThesaurus(object):
    def __init__(self, master):
        self.timerDelay = 100
        self.currentWordObj = None
        self.currentWordList = [None]
        self.currentWordIndex = ""
        
        self.antonymsMode = False
        self.currentSynDict = None
        self.currentSyn = None
        self.currentAntDict = None        
        self.currentAnt = None
        self.currentListBoxIndex = 0
        
        self.currentDefList = [None]
        self.currentDef = None
        self.currentDefIndex = 0
        
        ## Master
        self.master = master
        master.title("LiveThesaurus, powered by thesaurus.com")
        master.option_add("*font", ("Times New Roman", 15))
        # CITATION: Code from: https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        # makes the application window full screen
        screenWidth = master.winfo_screenwidth()
        screenHeight = master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screenWidth, screenHeight))
        
        self.master.config(background="black")
        self.master.bind("<Command-z>", self.undo)
        
        ## Left Frame
        self.leftFrame = Frame(self.master)
        self.instructionsLabel = Label(self.leftFrame, 
                       text="Welcome to LiveThesaurus!\n" +
                       "Type text below. Highlight a word to get its synonyms.",
                       anchor=N, borderwidth=2, relief="solid")
        self.textFrame = Frame(self.leftFrame, borderwidth=2, relief="solid")
        self.audioFrame = Frame(self.leftFrame, borderwidth=2, relief="solid")
        
        # creates the widgets on left side of the screen
        self.textBox = Text(self.textFrame, borderwidth=2, relief="sunken")
        self.textScrollBar = Scrollbar(self.textFrame)
        self.audioButton = Button(self.audioFrame, width=35, height=1, 
                                  text="Audio", command=self.runAudio)
        
        self.textScrollBar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.textScrollBar.set)
        
        self.leftFrame.config(background="coral")
        
        # packs all widgets in the left frame of the application
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=8)
        self.instructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=(3,0))
        self.textFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=(3,0))
        self.textBox.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        self.textScrollBar.pack(side=LEFT, fill=Y)
        self.audioFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.audioButton.pack(side=TOP)
        
        ## Right Frame
        self.rightFrame = Frame(self.master)
        self.wordAndDefFrame = Frame(self.rightFrame)
        self.wordInfoFrame = Frame(self.wordAndDefFrame, borderwidth=2, 
                                   relief="solid")
        self.defInfoFrame = Frame(self.wordAndDefFrame, borderwidth=2, 
                                  relief="solid")
        self.innerDefFrame = Frame(self.defInfoFrame)
        self.termFrame = Frame(self.rightFrame)
        self.innerTermFrame = Frame(self.termFrame, borderwidth=2, 
                                    relief="solid")
        self.modeFrame = Frame(self.innerTermFrame)
        
        # creates the widgets on the right side of the screen
        self.currentWordLabel = Label(self.wordInfoFrame, 
                            text="Selected Word: " + str(self.currentWordObj),
                            anchor=N)
        self.definitionLabel = Label(self.innerDefFrame, text="Definition: ", 
                                     anchor=N)
        self.termInstructionsLabel = Label(self.termFrame, 
               text="Pick a synonym and press the Enter key to change the word",
               borderwidth=2, relief="solid", anchor=N)
        self.synonymTitle = Label(self.modeFrame, text="List", anchor=N)
        self.toggleSynOrAntButton = Button(self.modeFrame, width=8, height=1, 
                             text="Synonyms", 
                             command=self.switchModes)
        self.colonLabel = Label(self.modeFrame, text=": ", anchor=N)
        self.termListBox = Listbox(self.termFrame, borderwidth=2, 
                                   relief="solid")
        self.termScrollBar = Scrollbar(self.termListBox)
        
        # CITATION: Option Menu Code from: https://stackoverflow.com/questions/35132221/tkinter-optionmenu-how-to-get-the-selected-choice
        # creates and packs an option menu for definitions
        self.definitons = StringVar()
        self.definitionMenu = OptionMenu(self.innerDefFrame, self.definitons,
                              *self.currentDefList)
        self.definitons.set(self.currentDefList[0])
        
        self.rightFrame.config(background="black")
        self.wordAndDefFrame.config(background="coral")
        self.termFrame.config(background="coral")
        self.definitionMenu.config(width=35)
        self.termScrollBar.config(command=self.termListBox.yview)
        self.termListBox.config(yscrollcommand=self.termScrollBar.set)
        self.termListBox.bind("<<ListboxSelect>>", self.updateCurrentSynOrAnt)
        self.termListBox.bind("<Return>", self.replaceWordWithSynOrAnt)
        
        # packs all widgets in the right frame of the application
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(0,5), 
                                                                pady=5)
        self.wordAndDefFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.wordInfoFrame.pack(side=TOP, fill=BOTH, padx=3, pady=(3,0))
        self.currentWordLabel.pack(side=TOP, padx=2, pady=2)
        self.defInfoFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.innerDefFrame.pack(side=TOP, padx=2, pady=2)
        self.definitionLabel.pack(side=LEFT, fill=BOTH, pady=(3,0))
        self.definitionMenu.pack(side=LEFT, fill=BOTH)
        self.termFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=3)
        self.termInstructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=(3,0))
        self.innerTermFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.modeFrame.pack(side=TOP, padx=2)
        self.synonymTitle.pack(side=LEFT, pady=2)
        self.toggleSynOrAntButton.pack(side=LEFT, padx=2, pady=2)
        self.colonLabel.pack(side=LEFT, pady=2)
        self.termListBox.pack(side=TOP, fill=BOTH, expand=YES, padx=3, 
                                                               pady=(0,3))
        self.termScrollBar.pack(side=RIGHT, fill=Y)
        
        self.timerFiredWrapper()
    
    # CITATION: timerFiredWrapper from Course Notes: Animation Part 2: Time-Based Animations in Tkinter
    # CITATION: Code that Keeps ScrollBar in same location from:
    # https://stackoverflow.com/questions/36086474/python-tkinter-update-scrolled-listbox-wandering-scroll-position
    # constantly updates highlighted words in TextBox every 100 milliseconds
    def timerFiredWrapper(self):
        currentView = self.termListBox.yview()
        self.updateCurrentWord()
        self.termListBox.yview_moveto(currentView[0])
        self.master.after(self.timerDelay, self.timerFiredWrapper)
        
    # switches between synonym and antonym mode
    def switchModes(self):
        self.antonymsMode = not self.antonymsMode
        if not self.antonymsMode:
            self.toggleSynOrAntButton.config(text="Synonyms")
        else:
            self.toggleSynOrAntButton.config(text="Antonyms")
        self.generateTermList()
    
    # undoes a word replacement
    def undo(self, *args):
        if self.currentWordList != [None]:
            lastWordObj = None
            if len(self.currentWordList) > 1:
                self.currentWordList.pop()
                lastWordObj = self.currentWordList[len(self.currentWordList)-1]
            else:
                lastWordObj = self.currentWordList[0]
            self.replaceWordInTextBox(lastWordObj.word)
            self.currentWordObj = lastWordObj
    
    # updates the current synonym/antonym whenever mouse is in the ListBox
    def updateCurrentSynOrAnt(self, event):
        try:
            indexTuple = self.termListBox.curselection()
            self.currentListBoxIndex = indexTuple[0]
            self.termListBox.activate(self.currentListBoxIndex)
            if not self.antonymsMode:
                defDict = self.currentSynDict[self.currentDef]
                self.currentSyn = defDict[self.currentListBoxIndex]["term"]
            else:
                defDict = self.currentAntDict[self.currentDef]
                self.currentAnt = defDict[self.currentListBoxIndex]["term"]
        except:
            pass
    
    # replaces word in text box with the chosen synonym
    def replaceWordWithSynOrAnt(self, event):
        try:
            synOrAnt = None
            if not self.antonymsMode:
                synOrAnt = self.currentSyn
            else:
                synOrAnt = self.currentAnt
            self.replaceWordInTextBox(synOrAnt)
            self.currentWordObj = Word(synOrAnt)
            self.addToWordList(self.currentWordObj)
        except:
            pass
    
    # adds a Word object to a list of user-chosen Word objects if the last 
    # element of the list is not the Word
    def addToWordList(self, word):
        if word != self.currentWordList[len(self.currentWordList)-1]:
            self.currentWordList += [word]
    
    # repalces the current word with another word in the textBox
    def replaceWordInTextBox(self, newWord):
        textBoxRow = getDigitsBeforeDecPt(self.currentWordIndex)
        textBoxCol = getDigitsAfterDecPt(self.currentWordIndex)
        endofcurrWordCol = textBoxCol + len(self.currentWordObj.word)
        endofcurrWordIndex = str(textBoxRow) + "." + str(endofcurrWordCol)
        textBoxText = self.textBox.get(self.currentWordIndex, endofcurrWordIndex)
        self.textBox.replace(self.currentWordIndex, endofcurrWordIndex, newWord)
    
    # gets the user's highlighted word, creates a Word object of that word, 
    # updates the current word label, and sets all variables to the 
    # corresponding instance variable of the Word object 
    def updateCurrentWord(self):
        try:
            highlightedWord = self.textBox.get(SEL_FIRST, SEL_LAST)
            self.currentWordObj = Word(highlightedWord)
            self.currentWordList = [None]
            self.currentWordList[0] = self.currentWordObj
            if self.currentWordObj.hasSynOrAnt():
                self.currentWordLabel.config(text="Selected Word: \"" + \
                                             self.currentWordObj.word + "\"")
                self.currentWordIndex = self.textBox.index("sel.first")
                self.currentSynDict = self.currentWordObj.synonymDict
                self.currentAntDict = self.currentWordObj.antonymDict
                self.currentDefList = self.currentWordObj.definitionList
            else:
                self.currentWordLabel.config(text="Selected Word has no " + 
                                                  "synonyms")
                self.currentWordObj = None
                self.currentWordList = [None]
                self.currentDefList = [None]
                self.currentDef = None
                self.currentDefIndex = 0
                self.definitons.set(None)
                self.termListBox.delete(0, "end")
                if not self.antonymsMode:
                    self.termListBox.insert(END, "No Synonyms!")
                else:
                    self.termListBox.insert(END, "No Antonyms!")
            self.updateDefMenu(self.currentDefList)
        except:
            pass
    
    # CITATION: code from: https://stackoverflow.com/questions/26084620/tkinter-option-menu-update-options-on-fly
    # updates the definition menu according to the user's choice
    def updateDefMenu(self, defList):
        menu = self.definitionMenu["menu"]
        menu.delete(0, "end")
        if defList != None:
            for d in defList:
                menu.add_command(label=d, 
                        command=lambda value=d: self.definitons.set(value))
            # gives all options a command associated with updateCurrentDef
            self.definitons.trace("w", self.updateCurrentDef)
            # loads definition menu at the index of the current definition
            self.definitons.set(defList[self.currentDefIndex])
    
    # CITATION: Some code from: https://stackoverflow.com/questions/37704176/how-to-update-the-command-of-an-optionmenu
    # Changes the definition label according to the user's choice
    def updateCurrentDef(self, *args):
        if self.currentDefList != [None]:
            self.currentDef = str(self.definitons.get())
            self.currentDefIndex = self.currentDefList.index(self.currentDef)
            self.generateTermList()
    
    # draws and creates a list made out of non-changeable entry boxes that
    # contain synonyms or antonyms, depending on the mode
    def generateTermList(self):
        self.termListBox.delete(0, "end")
        if not self.antonymsMode and self.currentSynDict != None:
            if self.currentSynDict[self.currentDef] == []: # no synonyms
                self.termListBox.insert(END, "No Synonyms!")
            else:
                for synDict in self.currentSynDict[self.currentDef]:
                    self.termListBox.insert(END, synDict["term"])
        elif self.antonymsMode and self.currentAntDict != None:
            if self.currentAntDict[self.currentDef] == []: # no antonyms
                self.termListBox.insert(END, "No Antonyms!")
            else:
                for antDict in self.currentAntDict[self.currentDef]:
                    self.termListBox.insert(END, antDict["term"])
        self.termListBox.select_set(self.currentListBoxIndex)
        self.termListBox.activate(self.currentListBoxIndex)
    
    # records audio and displays it on the TextBox
    def runAudio(self):
        audioText = speechRecognizer.getAudio()
        if audioText != None:
            self.textBox.insert(END, audioText)

# returns the digits after the decimal point in a string representation of a 
# float
def getDigitsAfterDecPt(strNum):
    indexOfDecPt = strNum.find(".")
    afterDecimal = int(strNum[indexOfDecPt + 1:])
    return afterDecimal

# returns the digits before the decimal point in a string representation of a 
# float
def getDigitsBeforeDecPt(strNum):
    indexOfDecPt = strNum.find(".")
    beforeDecimal = int(strNum[:indexOfDecPt])
    return beforeDecimal

root = Tk()
application = LiveThesaurus(root)
mainloop()