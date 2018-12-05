## LiveThesaurus class. Creates the main application

from tkinter import *
from tkinter import messagebox
from Word import *
import audio as speechRecognizer

class LiveThesaurus(object):
    def __init__(self, master):
        self.instructions = "Click HERE to type text!\n" + \
                            "Please read ALL the Instructions on this " + \
                            "Text Box and on the Right!\n" + \
                            "Insert text and Highlight a word to get its " + \
                            "Synonyms or Antonyms.\n" + \
                            "Try clicking on the \"Record Audio\" button " + \
                            "below and asking for the Synonyms or Antonyms " + \
                            "of a specific word!"
        
        self.timerDelay = 100

        self.currentWordObj = None
        self.previousWordObj = None
        self.currentWordList = []
        self.previousWordList = []
        self.currentWordIndex = ""
        self.previousWordIndex = ""
        
        self.antonymsMode = False
        self.currentSynDict = None
        self.currentSyn = None
        self.currentAntDict = None
        self.currentAnt = None
        self.currentListBoxIndex = 0
        
        self.defInstructions = "Click HERE to Choose Definitions!"
        self.currentDefList = [self.defInstructions]
        self.currentDef = None
        self.currentDefIndex = 0

        self.prevKey = ""
        
        ## Master
        self.master = master
        master.title("LiveThesaurus, powered by thesaurus.com")
        master.option_add("*font", ("Times New Roman", 15))
        # CITATION: Code from: https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        # makes the application window full screen
        screenWidth = master.winfo_screenwidth()
        screenHeight = master.winfo_screenheight()
        self.master.geometry("%dx%d+0+0" % (screenWidth, screenHeight))
        
        self.master.config(background="gainsboro")
        
        self.master.bind("<Command-z>", self.undo)
        self.master.bind("<Command-y>", self.redo)
        self.master.bind("<Command-a>", self.selectAll)
        
        self.master.bind("<Control-z>", self.undo)
        self.master.bind("<Control-y>", self.redo)
        self.master.bind("<Control-a>", self.selectAll)
        
        ## Instructions Frame
        self.instructionsFrame = Frame(self.master)
        self.instructionsLabel = Label(self.instructionsFrame, 
                                    text="Welcome to LiveThesaurus!",
                                    anchor=N, borderwidth=5, relief="ridge")
        self.instructionsFrame.pack(side=TOP, fill=BOTH, padx=5, pady=(5,0))
        self.instructionsLabel.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        
        self.instructionsFrame.config(background="orange")
        self.instructionsLabel.config(font=("Arial", 22, "bold"))
        
        ## Left Frame
        self.leftFrame = Frame(self.master)
        self.textFrame = Frame(self.leftFrame, borderwidth=2, relief="solid")
        self.audioFrame = Frame(self.leftFrame, borderwidth=2, relief="solid")
        
        # creates the widgets on left side of the screen
        self.textBox = Text(self.textFrame, borderwidth=2, relief="sunken", 
                            cursor="pencil", wrap=WORD)
        self.makePlaceHolderText()
        self.audioLabel = Label(self.audioFrame, text="Hit Button Below to " + \
                                "Record Audio:", borderwidth=2, relief="solid")
        self.audioButton = Button(self.audioFrame, width=35, height=1, 
                                  text="Record Audio", command=self.runAudio)
        self.textScrollBar = Scrollbar(self.textFrame)
        
        self.textScrollBar.config(command=self.textBox.yview)
        self.audioLabel.config(font=("Arial", 15, "bold"))
        self.textBox.config(yscrollcommand=self.textScrollBar.set)
        self.textBox.tag_configure("highlight", background="lightskyblue1")
        self.textBox.bind("<FocusIn>", self.deletePlaceHolderText)
        self.textBox.bind("<FocusOut>", self.addPlaceHolderText)
        self.textBox.bind("<KeyPress>", self.keyPressedInTextBox)

        self.leftFrame.config(background="orange")
        self.textFrame.config(background="gainsboro")
        
        # packs all widgets in the left frame of the application
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.textFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=(3,0))
        self.textBox.pack(side=LEFT, fill=BOTH, expand=YES, padx=2, pady=2)
        self.textScrollBar.pack(side=LEFT, fill=Y)
        self.audioFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.audioLabel.pack(side=TOP, fill=BOTH, padx=2, pady=(2,0))
        self.audioButton.pack(side=TOP, padx=2, pady=2)
        
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
        self.listBoxFrame = Frame(self.innerTermFrame, borderwidth=2, 
                                    relief="solid")
        
        # creates the widgets on the right side of the screen
        self.currentWordLabel = Label(self.wordInfoFrame, 
                            text="Selected Word: " + str(self.currentWordObj),
                            anchor=N, font=("Arial", 15, "bold"))
        self.definitionLabel = Label(self.innerDefFrame, text="Definition: ", 
                                     anchor=N, font=("Arial", 15, "bold"))
        self.synonymTitle = Label(self.modeFrame, text="List", anchor=N,
                                  font=("Arial", 15, "bold"))
        self.toggleSynOrAntButton = Button(self.modeFrame, width=8, height=1, 
                                           text="Synonyms", 
                                           command=self.switchModes)
        self.colonLabel = Label(self.modeFrame, text=":", anchor=N,
                                font=("Arial", 15, "bold"))
        self.termListBox = Listbox(self.listBoxFrame, borderwidth=0, 
                                   relief="solid", cursor="hand2")
        self.termScrollBar = Scrollbar(self.listBoxFrame)
        # CITATION: Option Menu Code from: https://stackoverflow.com/questions/35132221/tkinter-optionmenu-how-to-get-the-selected-choice
        # creates and packs an option menu for definitions
        self.definitons = StringVar()
        self.definitionMenu = OptionMenu(self.innerDefFrame, self.definitons,
                              *self.currentDefList)
        # initially loads definition menu
        self.definitons.set(self.currentDefList[0])
        
        self.rightFrame.config(background="gainsboro")
        self.wordAndDefFrame.config(background="orange")
        self.termFrame.config(background="orange")
        self.definitionMenu.config(width=40)
        self.termScrollBar.config(command=self.termListBox.yview)
        self.termListBox.config(yscrollcommand=self.termScrollBar.set)
        
        self.termListBox.bind("<<ListboxSelect>>", self.updateCurrentSynOrAnt)
        self.termListBox.bind("<Return>", self.replaceWordWithSynOrAnt)
        self.termListBox.bind("<Double-Button-1>", self.replaceWordWithSynOrAnt)
        self.termListBox.bind("<Left>", self.replaceWordWithSynOrAnt) 
        
        # packs all widgets in the right frame of the application
        self.rightFrame.pack(side=RIGHT, fill=BOTH, expand=YES, padx=(0,5), 
                                                                pady=2)
        self.wordAndDefFrame.pack(side=TOP, fill=BOTH, padx=(3,0), pady=3)
        self.wordInfoFrame.pack(side=TOP, fill=BOTH, padx=3, pady=(3,0))
        self.currentWordLabel.pack(side=TOP, padx=2, pady=2)
        self.defInfoFrame.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.innerDefFrame.pack(side=TOP, padx=2, pady=2)
        self.definitionLabel.pack(side=LEFT, fill=BOTH, pady=(2,0))
        self.definitionMenu.pack(side=LEFT)
        self.termFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=(3,0), pady=3)
        self.innerTermFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, 
                                                                  pady=3)
        self.modeFrame.pack(side=TOP, padx=2)
        self.synonymTitle.pack(side=LEFT, pady=2)
        self.toggleSynOrAntButton.pack(side=LEFT, pady=2)
        self.colonLabel.pack(side=LEFT, pady=2)
        self.listBoxFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, 
                                                                pady=(0,3))
        self.termListBox.pack(side=LEFT, fill=BOTH, expand=YES)
        self.termScrollBar.pack(side=LEFT, fill=Y)
    
    # run function
    def run(self):
        print("Running LiveThesaurus...")
        self.timerFiredWrapper()
        self.master.mainloop()
        print("Thank you for using LiveThesaurus!")
    
    # CITATION: Code below is a modifid timerFiredWrapper from Course Notes: Animation Part 2: Time-Based Animations in Tkinter
    # CITATION: Code that Keeps ScrollBar in same location from:
    # https://stackoverflow.com/questions/36086474/python-tkinter-update-scrolled-listbox-wandering-scroll-position
    # constantly updates highlighted words in TextBox every 100 milliseconds
    def timerFiredWrapper(self):
        self.addTermBoxInstr()

        currentView = self.termListBox.yview()
        self.updateCurrentWord()
        self.termListBox.yview_moveto(currentView[0])

        # if the index of the word or the word changes, remove the highlight 
        # from previous location
        if self.currentWordObj != self.previousWordObj or \
           self.previousWordIndex != self.currentWordIndex:
            self.highlight(False, self.previousWordIndex, self.previousWordObj)
        else:
            self.highlight(True, self.currentWordIndex, self.currentWordObj)
        
        self.master.after(self.timerDelay, self.timerFiredWrapper)
    
    # Highlight Code From: https://stackoverflow.com/questions/29495911/change-color-of-certain-words-in-tkinter-text-widget-based-on-position-in-list
    # handles highlights, which help users locate their current word
    def highlight(self, add, index, wordObj):
        try:
            textBoxLine = getDigitsBeforeDecPt(index)
            textBoxCol = getDigitsAfterDecPt(index)
            endofcurrWordCol = textBoxCol + len(wordObj.word)
            endofcurrWordIndex = str(textBoxLine) + "." + str(endofcurrWordCol)
            if add == True:
                self.textBox.tag_remove("highlight", "1.0", END)
                self.textBox.tag_add("highlight", index, endofcurrWordIndex)
            else:
                self.textBox.tag_remove("highlight", index, endofcurrWordIndex)
        except:
            pass
    
    # handles key pressed events in the textBox
    def keyPressedInTextBox(self, event):
        self.prevKey = event.keysym
        if event.keysym != "Left" and event.keysym != "Right" and \
           event.keysym != "Up" and event.keysym != "Down" and \
           self.textBox.get("1.0", "end-1c") != "":
            if self.prevKey != "??" and event.keysym != "z" and \
               event.keysym != "y" and event.keysym != "a":
                self.textBox.tag_remove("highlight", "1.0", END)
                self.currentWordLabel.config(text="Selected Word: None")
                self.currentWordObj = None
                self.previousWordObj = None
                self.currentWordList = []
                self.previousWordList = []
                self.currentDefList = [None]
                self.currentDef = None
                self.currentDefIndex = 0
                self.currentSynDict = None
                self.currentAntDict = None
                self.termListBox.delete(0, "end")
                if not self.antonymsMode:
                    self.termListBox.insert(END, "No Synonyms!")
                else:
                    self.termListBox.insert(END, "No Antonyms!")
                self.updateDefMenu(self.currentDefList)
    
    # adds placeholder text to TextBox
    def addPlaceHolderText(self, event):
        textBoxText = self.textBox.get("1.0", "end-1c")
        if textBoxText == "":
            self.textBox.tag_remove("highlight", "1.0", END)
            self.makePlaceHolderText()
    
    # makes the instructions/placeholder text
    def makePlaceHolderText(self):
        self.textBox.insert(END, self.instructions)
        self.textBox.tag_remove("highlight", "1.0", END)
        self.textBox.tag_add("highlight", "3." + str(len("Insert text and ")), 
                             "3." + str(len("Insert text and ") + \
                             len("Highlight")))
        self.currentWordObj = None
    
    # checks if placeholder text is present
    def placeholderTextPresent(self):
        textBoxText = self.textBox.get("1.0", "end-1c")
        placeHolderText = self.instructions
        return textBoxText == placeHolderText
    
    # if the placeholdertext is in the TextBox, delete text
    def deletePlaceHolderText(self, *args):
        if self.placeholderTextPresent():
            self.deleteText()
    
    # adds instructions to TermBox
    def addTermBoxInstr(self, *args):
        if self.currentSynDict == None and self.currentAntDict == None and \
            self.currentDefList == [self.defInstructions]:
            self.termListBox.delete(0, "end")
            self.termListBox.insert(END, "After picking a definition, " + \
                                         "Click HERE to Browse Terms")
            self.termListBox.insert(END,
                                "Double click with the Mouse or Hit the " + \
                                "\"ENTER\" key to change the word")
            
            synOrAnt = "Synonyms"
            if self.antonymsMode:
                synOrAnt = "Anyonyms"
                
            self.termListBox.insert(END, "Click the \"" + synOrAnt + "\" " + \
                                    "button above to swap between " + \
                                    "Synonyms and Antonyms")
            try:
                curSelectionTuple = self.termListBox.curselection()
                self.currentListBoxIndex = curSelectionTuple[0]
                self.termListBox.activate(self.currentListBoxIndex)
            except:
                pass
            self.termListBox.select_set(self.currentListBoxIndex)
            self.termListBox.activate(self.currentListBoxIndex)

    # switches between synonym and antonym mode
    def switchModes(self):
        self.antonymsMode = not self.antonymsMode
        if not self.antonymsMode:
            self.toggleSynOrAntButton.config(text="Synonyms")
        else:
            self.toggleSynOrAntButton.config(text="Antonyms")
        self.generateTermList()
    
    # undoes a word replacement
    def undo(self, event):
        if self.currentWordList != []:
            lastWordObj = None
            if len(self.currentWordList) > 1:
                poppedWord = self.currentWordList.pop()
                lastWordObj = self.currentWordList[-1]
                if lastWordObj != None:
                    self.previousWordList += [poppedWord]
                    self.replaceWordInTextBox(lastWordObj.word)
                    self.currentWordObj = lastWordObj
    
    # undoes an undo
    def redo(self, event):
        if self.previousWordList != []:
            lastWordObj = None
            if len(self.previousWordList) > 0:
                lastWordObj = self.previousWordList.pop()
                self.replaceWordInTextBox(lastWordObj.word)
                self.addToWordList(lastWordObj)
                self.currentWordObj = lastWordObj
    
    # updates the current synonym/antonym whenever mouse is in the ListBox
    def updateCurrentSynOrAnt(self, event):
        try:
            curSelectionTuple = self.termListBox.curselection()
            self.currentListBoxIndex = curSelectionTuple[0]
            self.termListBox.activate(self.currentListBoxIndex)
            if not self.antonymsMode:
                currDefDict = self.currentSynDict[self.currentDef]
                self.currentSyn = currDefDict[self.currentListBoxIndex]["term"]
            else:
                currDefDict = self.currentAntDict[self.currentDef]
                self.currentAnt = currDefDict[self.currentListBoxIndex]["term"]
        except:
            pass
    
    # replaces word in text box with the chosen synonym
    def replaceWordWithSynOrAnt(self, event):
        try:
            if not self.placeholderTextPresent():
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
    
    # replaces the current word with another word in the textBox
    def replaceWordInTextBox(self, newWord):
        textBoxLine = getDigitsBeforeDecPt(self.currentWordIndex)
        textBoxCol = getDigitsAfterDecPt(self.currentWordIndex)
        endOfCurrWordCol = textBoxCol + len(self.currentWordObj.word)
        endOfCurrWordIndex = str(textBoxLine) + "." + str(endOfCurrWordCol)
        self.textBox.replace(self.currentWordIndex, endOfCurrWordIndex, newWord)
    
    # gets the user's highlighted word, creates a Word object of that word, 
    # updates the current word label, and sets all variables to the 
    # corresponding instance variable of the Word object 
    def updateCurrentWord(self):
        try:
            self.previousWordObj = self.currentWordObj
            self.previousWordIndex = self.currentWordIndex
            highlightedWord = self.textBox.get(SEL_FIRST, SEL_LAST)
            self.currentWordObj = Word(highlightedWord)
            # if user picked a new word, reset all indices and unhiglight the 
            # previous word
            if self.currentWordObj != self.previousWordObj:
                self.currentDefIndex = 0
                self.currentListBoxIndex = 0
            self.currentWordList = [self.currentWordObj]
            if self.currentWordObj.hasSynOrAnt():
                wordObjStr = self.currentWordObj.word
                if "\n" in self.currentWordObj.word[-1]:
                    wordObjStr = self.currentWordObj.word[:-1]
                self.currentWordLabel.config(text="Selected Word: \"" + \
                                             wordObjStr + "\"")
                self.currentWordIndex = self.textBox.index("sel.first")
                self.currentSynDict = self.currentWordObj.synonymDict
                self.currentAntDict = self.currentWordObj.antonymDict
                self.currentDefList = self.currentWordObj.definitionList
            else:
                self.currentWordLabel.config(text="Selected Word has no " + \
                                                  "Synonyms or Antonyms!")
                self.highlight(False, self.previousWordIndex, 
                                      self.previousWordObj)
                self.currentWordObj = None
                self.previousWordObj = None
                self.currentWordList = []
                self.previousWordList = []
                self.currentDefList = [None]
                self.currentDef = None
                self.currentDefIndex = 0
                self.currentSynDict = None
                self.currentAntDict = None
                self.termListBox.delete(0, "end")
                if not self.antonymsMode:
                    self.termListBox.insert(END, "No Synonyms!")
                else:
                    self.termListBox.insert(END, "No Antonyms!")
            self.updateDefMenu(self.currentDefList)
        except:
            # if there is no text in the TextBox and nothing is highlighted, 
            # reset everything and show instructions
            if self.textBox.get("1.0", "end-1c") == "":
                self.highlight(False, self.previousWordIndex, 
                                      self.previousWordObj)
                self.currentWordLabel.config(text="Selected Word: None")
                self.currentWordObj = None
                self.previousWordObj = None
                self.currentWordList = []
                self.previousWordList = []
                self.currentDefList = [self.defInstructions]
                self.currentDef = None
                self.currentDefIndex = 0
                self.currentSynDict = None
                self.currentAntDict = None
                self.definitionMenu["menu"].delete(0, "end")
                self.definitons.set(self.defInstructions)
                self.addTermBoxInstr()
    
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
            # loads definition menu with the first definition in defList
            self.definitons.set(defList[self.currentDefIndex])
    
    # CITATION: Some code from: https://stackoverflow.com/questions/37704176/how-to-update-the-command-of-an-optionmenu
    # Changes the definition label according to the user's choice
    def updateCurrentDef(self, *args):
        if self.currentDefList != [None]:
            prevDef = self.currentDef
            self.currentDef = str(self.definitons.get())
            # if user picked a new def, reset the ListBox Index
            if self.currentDef != prevDef:
                self.currentListBoxIndex = 0
            self.currentDefIndex = self.currentDefList.index(self.currentDef)
            self.generateTermList()
    
    # draws and creates a list made out of non-changeable entry boxes that
    # contain synonyms or antonyms, depending on the mode
    def generateTermList(self):
        self.termListBox.delete(0, "end")
        if not self.antonymsMode and self.currentSynDict != None and \
           self.currentDef in self.currentSynDict:
            if self.currentSynDict[self.currentDef] == []: # no synonyms
                self.termListBox.insert(END, "No Synonyms!")
            else:
                for synDict in self.currentSynDict[self.currentDef]:
                    self.termListBox.insert(END, synDict["term"])
        elif self.antonymsMode and self.currentAntDict != None and \
           self.currentDef in self.currentAntDict:
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
            self.textBox.tag_remove(SEL, "1.0", END)
            # checks if user asks for synonyms and antonyms
            if "synonyms for" in audioText or "antonyms for" in audioText or \
               "synonyms of" in audioText or "antonyms of" in audioText or \
               "synonym for" in audioText or "antonym for" in audioText or \
               "synonym of" in audioText or "antonym of" in audioText:
                # gets the word that the user wants
                word = ""
                if "synonyms for" in audioText:
                    if self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("synonyms for") + \
                                            len("synonyms for")
                    word = audioText[indexOfWord:]
                elif "antonyms for " in audioText:
                    if not self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("antonyms for") + \
                                            len("antonyms for")
                    word = audioText[indexOfWord:]
                elif "synonyms of " in audioText:
                    if self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("synonyms of") + \
                                            len("synonyms of")
                    word = audioText[indexOfWord:]
                elif "antonyms of " in audioText:
                    if not self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("antonyms of") + \
                                            len("antonyms of")
                    word = audioText[indexOfWord:]
                elif "synonym for " in audioText:
                    if self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("synonym for") + \
                                            len("synonym for")
                    word = audioText[indexOfWord:]
                elif "antonym for " in audioText:
                    if not self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("antonym for") + \
                                            len("antonym for")
                    word = audioText[indexOfWord:]
                elif "synonym of " in audioText:
                    if self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("synonym of") + \
                                            len("synonym of")
                    word = audioText[indexOfWord:]
                elif "antonym of " in audioText:
                    if not self.antonymsMode:
                        self.switchModes()
                    indexOfWord = audioText.find("antonym of") + \
                                            len("antonym of")
                    word = audioText[indexOfWord:]

                # update the current word
                self.previousWordObj = self.currentWordObj
                self.previousWordIndex = self.currentWordIndex

                if word != "":
                    self.currentWordObj = Word(word[1:])
                else:
                    self.currentWordObj = None

                if self.currentWordObj != self.previousWordObj:
                    self.currentDefIndex = 0
                    self.currentListBoxIndex = 0
                self.currentWordList = [self.currentWordObj]

                # checks if current word is valid
                if self.currentWordObj != None and \
                   self.currentWordObj.hasSynOrAnt():
                    self.deletePlaceHolderText()
                    audioWord = self.currentWordObj.word
                    self.currentWordLabel.config(text="Selected Word: \"" + \
                                             audioWord + "\"")
                    if self.placeholderTextPresent():
                        self.currentWordIndex = "1.0"
                        self.textBox.insert(END, audioWord)
                    elif audioWord in self.textBox.get("1.0", "end-1c"):
                        self.currentWordIndex = self.textBox.search(audioWord, 
                                                                    "1.0", END)
                    else:
                        self.currentWordIndex = self.textBox.index("end-1c")
                        self.textBox.insert(END, audioWord)
                    # updates the synDict, antDict, and defList
                    self.currentSynDict = self.currentWordObj.synonymDict
                    self.currentAntDict = self.currentWordObj.antonymDict
                    self.currentDefList = self.currentWordObj.definitionList
                    self.updateDefMenu(self.currentDefList)
                    self.audioLabel.config(text="Hit Button Below to " + \
                                                "Record Audio")
                else:
                    revealedChars = 44
                    partOfWord = word[1:revealedChars]
                    if revealedChars <= len(word[1:]):
                        partOfWord += "..."
                    messagebox.showerror("ERROR!", "\"" + partOfWord + \
                                                   "\" has no " + \
                                                   "Synonyms or Antonyms. " + \
                                                   "Please Try Again.")

            # if user did not ask for synonyms or antonyms, then just insert the
            # audio at the end of the text
            else:
                self.deletePlaceHolderText()
                self.textBox.insert(END, audioText)
        else:
            messagebox.showerror("ERROR!", "Unable to Get Audio! Please Try "+\
                                           "Again.")
    
    # Code From: https://stackoverflow.com/questions/13801557/select-all-text-in-a-text-widget-using-python-3-with-tkinter
    # selects all text in a TextBox
    def selectAll(self, event):
        self.textBox.tag_add(SEL, "1.0", END)
        self.textBox.mark_set(INSERT, "1.0")
        self.textBox.see(INSERT)
    
    # clears text from TextBox
    def deleteText(self, *args):
        self.textBox.delete("1.0", END)

# returns the digits before the decimal point in a string representation of a 
# float
def getDigitsBeforeDecPt(strNum):
    indexOfDecPt = strNum.find(".")
    beforeDecimal = int(strNum[:indexOfDecPt])
    return beforeDecimal

# returns the digits after the decimal point in a string representation of a 
# float
def getDigitsAfterDecPt(strNum):
    indexOfDecPt = strNum.find(".")
    afterDecimal = int(strNum[indexOfDecPt + 1:])
    return afterDecimal