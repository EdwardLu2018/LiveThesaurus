from tkinter import *
from Word import *
import audio as speechRecognizer

class LiveThesaurus(object):
    def __init__(self, master):
        self.master = master
        master.title("LiveThesaurus, powered by thesaurus.com")
        master.option_add("*font", ("Times New Roman", 15))
        
        self.timerDelay = 100
        self.currentWordObj = None
        self.currentWordIndex = 0
        
        self.antonymsMode = False
        self.currentSynDict = None
        self.currentSyn = None
        self.currentAntDict = None        
        self.currentAnt = None
        self.currentListBoxIndex = 0
        
        self.currentDefList = [None]
        self.currentDef = None
        self.currentDefIndex = 0
                
        # CITATION: Code from: https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        # makes the application window full screen
        screenWidth = master.winfo_screenwidth()
        screenHeight = master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screenWidth, screenHeight))
        self.master.config(background='black')
        
        self.leftFrame = Frame(self.master)
        # creates a text box and scroll bar, along with a button that will
        # print synonyms on the right side of the window
        self.textScrollBar = Scrollbar(self.leftFrame)
        self.textBox = Text(self.leftFrame, width=40, height=37, 
                            borderwidth=3, relief="sunken")
        self.leftInstructionsLabel = Label(self.leftFrame, 
                        text="Welcome to LiveThesaurus!\n" +
                        "Type text below. Highlight a word to get its synonyms.",
                        anchor=N)
        self.audioButton = Button(self.leftFrame, width=40, height=1, 
                             text="Audio", 
                             command=self.runAudio)
        self.textScrollBar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.textScrollBar.set)
        
        # packs all widgets in the left frame of the application
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=8, pady=8)
        self.textScrollBar.pack(side=RIGHT, fill=Y)
        self.leftInstructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.textBox.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.audioButton.pack(side=TOP, fill=BOTH)
        
        
        # creates the right frame of the window
        self.rightFrame = Frame(self.master)
        self.wordAndDefFrame = Frame(self.rightFrame)
        self.wordInfoFrame = Frame(self.wordAndDefFrame, borderwidth=1, relief="solid")
        self.defInfoFrame = Frame(self.wordAndDefFrame, borderwidth=1, relief="solid")
        self.innerDefFrame = Frame(self.defInfoFrame)
        self.synFrame = Frame(self.rightFrame)
        
        # labels for the selected word, current definition, and synonyms
        self.currentWordLabel = Label(self.wordInfoFrame, 
                            text="Selected Word: " + str(self.currentWordObj),
                            anchor=N)
        self.definitionLabel = Label(self.innerDefFrame, text="Definition: ", 
                                     anchor=N)
        self.synInstructionsLabel = Label(self.synFrame, 
                text="Pick a synonym and press the Enter key to change the word",
                borderwidth=1, relief="solid", anchor=N)
        self.synonymTitle = Label(self.synFrame, text="List of Synonyms:",
                                  anchor=N)
        self.toggleSynOrAnt = Button(self.synFrame, width=10, height=1, 
                             text="Synonyms", 
                             command=self.switchModes)
        self.termBox = Listbox(self.synFrame, borderwidth=2, relief="solid")
        
        # CITATION: Option Menu Code from: https://stackoverflow.com/questions/35132221/tkinter-optionmenu-how-to-get-the-selected-choice
        # creates and packs an option menu for definitions
        self.definitons = StringVar()
        self.definitionMenu = OptionMenu(self.innerDefFrame, self.definitons,
                              *self.currentDefList)
        self.definitons.set(self.currentDefList[0])
        
        self.rightFrame.config(background="black")
        self.definitionMenu.config(width=35)
        self.synScrollBar = Scrollbar(self.termBox)
        self.synScrollBar.config(command=self.termBox.yview)
        self.termBox.config(yscrollcommand=self.synScrollBar.set)
        self.termBox.bind("<<ListboxSelect>>", self.updateCurrentSynOrAnt)
        self.termBox.bind("<Return>", self.replaceWordWithSynOrAnt)
        
        # packs all widgets in the right frame of the application
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.wordAndDefFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.wordInfoFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.currentWordLabel.pack(side=TOP, padx=2, pady=2)
        self.defInfoFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.innerDefFrame.pack(side=TOP, pady=2)
        self.definitionLabel.pack(side=LEFT, fill=BOTH, pady=2)
        self.definitionMenu.pack(side=LEFT, fill=BOTH)
        self.synFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=3)
        self.synInstructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.synonymTitle.pack(side=TOP, padx=2, pady=2)
        self.toggleSynOrAnt.pack(side=TOP, padx=2, pady=2)
        self.termBox.pack(side=TOP, fill=BOTH, expand=YES, padx=2)
        self.synScrollBar.pack(side=RIGHT, fill=Y)

        self.generateSynOrAntList()
        self.timerFiredWrapper()
    
    # CITATION: timerFiredWrapper from Course Notes: Animation Part 2: Time-Based Animations in Tkinter
    # CITATION: Code that Keeps ScrollBar in same location from:
    # https://stackoverflow.com/questions/36086474/python-tkinter-update-scrolled-listbox-wandering-scroll-position
    # constantly updates highlighted words in TextBox every 100 milliseconds
    def timerFiredWrapper(self):
        currentView = self.termBox.yview()
        self.updateCurrentWord()
        self.termBox.yview_moveto(currentView[0])
        self.master.after(self.timerDelay, self.timerFiredWrapper)
    
    def switchModes(self):
        self.antonymsMode = not self.antonymsMode
        if not self.antonymsMode:
            self.toggleSynOrAnt.config(text="Synonyms")
        else:
            self.toggleSynOrAnt.config(text="Antonyms")
        self.generateSynOrAntList()
    
    # updates the current synonym whenever mouse is in the synonym ListBox
    def updateCurrentSynOrAnt(self, event):
        try:
            indexTuple = self.termBox.curselection()
            self.currentListBoxIndex = indexTuple[0]
            self.termBox.activate(self.currentListBoxIndex)
            if not self.antonymsMode:
                currenttermBox = self.currentSynDict[self.currentDef]
                self.currentSyn = currenttermBox[self.currentListBoxIndex]["term"]
            else:
                currentAntList = self.currentAntDict[self.currentDef]
                self.currentAnt = currentAntList[self.currentListBoxIndex]["term"]
        except:
            pass
    
    # replaces word in text box with the chosen synonym
    def replaceWordWithSynOrAnt(self, event):
        synOrAnt = None
        if not self.antonymsMode:
            synOrAnt = self.currentSyn
        else:
            synOrAnt = self.currentAnt
        textBoxText = self.textBox.get("1.0", END)
        textBoxText = textBoxText[:self.currentWordIndex] + \
                    synOrAnt + textBoxText[self.currentWordIndex + \
                    len(self.currentWordObj.word):]
        textBoxText = textBoxText[:-1] # removes "\n"
        self.textBox.replace("1.0", END, textBoxText)
        self.currentWordObj = Word(synOrAnt)
    
    # gets the highlighted word when button is pressed and sets  the above 
    # labels corresponding to the word
    def updateCurrentWord(self):
        try:
            highlightedWord = self.textBox.get(SEL_FIRST, SEL_LAST)
            self.currentWordObj = Word(highlightedWord)
            if self.currentWordObj.isValidWord():
                self.currentWordLabel.config(text="Selected Word: \"" + \
                                             self.currentWordObj.word + "\"")
                selFirstPos = float(self.textBox.index("sel.first"))
                self.currentWordIndex = getDigitsAfterDecPt(selFirstPos)
                self.currentSynDict = self.currentWordObj.synonymDict
                self.currentAntDict = self.currentWordObj.antonymDict
                self.currentDefList = list(self.currentSynDict.keys())
            else:
                self.currentWordLabel.config(text="Selected Word has no synonyms")
                self.currentWordObj = None
                self.currentDefList = [None]
                self.currentDef = None
                self.termBox.delete(0, "end")
                self.currentSynDict = None
                self.currentAntDict = None
                self.definitons.set(None)
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
            self.generateSynOrAntList()
    
    # draws and creates a synonym list made out of non-changeable entry boxes
    def generateSynOrAntList(self):
        self.termBox.delete(0, "end")
        if not self.antonymsMode:
            if self.currentSynDict != None:
                for syn in self.currentSynDict[self.currentDef]:
                    self.termBox.insert(END, syn["term"])
        else:
            if self.currentAntDict != None:
                for ant in self.currentAntDict[self.currentDef]:
                    self.termBox.insert(END, ant["term"])
        self.termBox.select_set(self.currentListBoxIndex)
        self.termBox.activate(self.currentListBoxIndex)
    
    # records audio and displays it on the TextBox
    def runAudio(self):
        textBoxText = self.textBox.get("1.0", END)
        audioText = speechRecognizer.getAudio()
        if audioText != None:
            self.textBox.replace("1.0", END, textBoxText[:-1] + audioText)

# returns the digits after the decimal point in a float as an int
def getDigitsAfterDecPt(flt):
    strFloat = str(flt)
    indexOfDecPt = strFloat.find(".")
    afterDecimal = int(strFloat[indexOfDecPt + 1:])
    return afterDecimal

root = Tk()
application = LiveThesaurus(root)
mainloop()