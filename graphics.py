from tkinter import *
from Word import *
import audio as speechRecognizer

class LiveThesaurus(object):
    def __init__(self, master):
        self.master = master
        master.title("LiveThesaurus, powered by thesaurus.com")
        master.option_add("*font", ("Times New Roman", 14))
        
        self.timerDelay = 1000
        self.currentWordObj = None
        self.currentWordIndex = 0
        self.currentDef = None
        self.currentSynDict = None
        self.currentSyn = None
        self.currentSynIndex = 0
        self.currentDefList = [None]
        
        # Code from: https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        # makes the application window full screen
        screenWidth = master.winfo_screenwidth()
        screenHeight = master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screenWidth, screenHeight))
        
        self.master.bind('<Return>', self.replaceWordWithSyn)
        
        self.leftFrame = Frame(self.master, borderwidth=2, relief="solid")
        # creates a text box and scroll bar, along with a button that will
        # print synonyms on the right side of the window
        self.textScrollBar = Scrollbar(self.leftFrame)
        self.textBox = Text(self.leftFrame, width=20, height=40, 
                            borderwidth=1, relief="sunken")
        self.leftInstructionsLabel = Label(self.leftFrame, 
                            text="Welcome to LiveThesaurus!\n"+
                            "Type text below, highlight a word, and click" + 
                            " on the Get Synonyms button to get started!",
                            borderwidth=2, relief="solid", anchor=N)
        self.getSynButton = Button(self.leftFrame, width=20, height=1, 
                             text="Get Synonyms!", 
                             command=self.updateCurrentWord)
        self.audioButton = Button(self.leftFrame, width=20, height=1, 
                             text="Audio", 
                             command=self.runAudio)
        self.textScrollBar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.textScrollBar.set)
        
        # packs the textbox, scroll bar, and button all on the left side of the 
        # screen
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.textScrollBar.pack(side=RIGHT, fill=Y)
        self.leftInstructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.textBox.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.getSynButton.pack(side=TOP, fill=BOTH)
        self.audioButton.pack(side=TOP, fill=BOTH)
        
        
        # creates the right frame of the window
        self.rightFrame = Frame(self.master, borderwidth=2, relief="solid")
        self.wordInfoFrame = Frame(self.rightFrame, borderwidth=2, 
                                  relief="solid")
        self.synFrame = Frame(self.rightFrame, borderwidth=2, relief="solid")
        
        # Option Menu Code from: https://stackoverflow.com/questions/35132221/tkinter-optionmenu-how-to-get-the-selected-choice
        # creates and packs an option menu for definitions
        self.definitons = StringVar()
        self.definitionMenu = OptionMenu(self.wordInfoFrame, self.definitons, 
                              *self.currentDefList)
        self.definitons.set(self.currentDefList[0])
        
        # labels for the selected word, current definition, and synonyms
        self.currentWordLabel = Label(self.wordInfoFrame, 
                                 text="Selected Word: " + str(self.currentWordObj),
                                 borderwidth=1, relief="solid", anchor=N)
        self.definitionLabel = Label(self.wordInfoFrame, 
                          text="Definiton: " + str(self.currentDefList[0]),
                          borderwidth=1, relief="solid", anchor=N)
        self.defInstructionsLabel = Label(self.wordInfoFrame, 
                    text="Change Definitions Below!",
                    borderwidth=2, relief="solid", anchor=N)
        self.synInstructionsLabel = Label(self.synFrame, 
                text="Pick a synonym and press the Enter key to change the word",
                borderwidth=2, relief="solid", anchor=N)
        self.synonymTitle = Label(self.synFrame, text="List of Synonyms:",
                                  borderwidth=1,
                                  relief="solid", anchor=N)
        self.synList = Listbox(self.synFrame, borderwidth=1, relief="solid")
        self.synList.config(exportselection=False)
        
        self.synScrollBar = Scrollbar(self.synList)
        self.synScrollBar.config(command=self.synList.yview)
        self.synList.config(yscrollcommand=self.synScrollBar.set)
        
        # draws everything in the right frame of application
        self.rightFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.wordInfoFrame.pack(side=TOP, fill=X, padx=3, pady=3)
        self.currentWordLabel.pack(side=TOP, fill=X, padx=2, pady=2)
        self.definitionLabel.pack(side=TOP, fill=X, padx=2, pady=2)
        self.defInstructionsLabel.pack(side=TOP, fill=X, padx=2, pady=2)
        self.definitionMenu.pack(side=TOP, fill=X)
        self.synFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=3)
        self.synInstructionsLabel.pack(side=TOP, fill=X, padx=2, pady=2)
        self.synonymTitle.pack(side=TOP, fill=X, padx=2, pady=2)
        self.synList.pack(side=TOP, fill=BOTH, expand=YES, padx=2)
        self.synScrollBar.pack(side=RIGHT, fill=Y)
        self.generateSynonymList()
        
        self.timerFiredWrapper()
        
    def timerFiredWrapper(self):
        self.updateCurrentWord()
        self.master.after(self.timerDelay, self.timerFiredWrapper)
    
    # replaces word in text box with the chosen synonym
    def replaceWordWithSyn(self, event):
        try:
            indexTuple = self.synList.curselection()
            self.currentSynIndex = indexTuple[0]
            currentSynList = self.currentSynDict[self.currentDef]
            self.currentSyn = currentSynList[self.currentSynIndex]["term"]
            textBoxText = self.textBox.get("1.0", END)
            textBoxText = textBoxText[:self.currentWordIndex] + self.currentSyn + \
                          textBoxText[self.currentWordIndex + \
                                      len(self.currentWordObj.word):]
            textBoxText = textBoxText[:-1] # removes "\n"
            self.textBox.replace("1.0", END, textBoxText)
            self.currentWordObj = Word(self.currentSyn)
        except:
            pass
            
    # gets the prints the highlighted word when button is pressed and sets 
    # the above labels corresponding to the word
    def updateCurrentWord(self):
        try:
            highlightedWord = self.textBox.get(SEL_FIRST, SEL_LAST)
            self.currentWordObj = Word(highlightedWord)
            if self.currentWordObj.isValidWord():
                self.currentWordLabel.config(text="Selected Word: \"" + \
                                             self.currentWordObj.word + "\"")
                selFirstPos = float(self.textBox.index("sel.first"))
                self.currentWordIndex = getDigitsAfterDecPt(selFirstPos)
                self.currentWordObj = Word(highlightedWord)
                self.currentSynDict = self.currentWordObj.synonymDict
                self.currentDefList = list(self.currentSynDict.keys())
                self.updateDefMenu(self.currentDefList)
            else:
                self.currentWordLabel.config(text="Selected Word: Not a word!")
                self.currentWordObj = None
        except:
            pass

    # Code from: https://stackoverflow.com/questions/37704176/how-to-update-the-command-of-an-optionmenu
    # Changes the definition label according to the user's choice
    def changeDefLabel(self, *args):
        self.currentDef = str(self.definitons.get())
        self.definitionLabel.config(text="Definiton: \"" + self.currentDef + "\"")
        self.generateSynonymList()
    
    # updates the definition menu according to the user's choice
    def updateDefMenu(self, defList):
        menu = self.definitionMenu["menu"]
        menu.delete(0, "end")
        for d in defList:
            menu.add_command(label=d, 
                    command=lambda value=d: self.definitons.set(value))
        # gives all options a command associated with changeDefLabel
        self.definitons.trace("w", self.changeDefLabel)
        # loads menu with first definition
        self.definitons.set(defList[0])
    
    # draws and creates a synonym list made out of non-changeable entry boxes
    def generateSynonymList(self):
        self.synList.delete(0,'end')
        if self.currentSynDict != None:
            for syn in self.currentSynDict[self.currentDef]:
                self.synList.insert(END, syn["term"])
    
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