from tkinter import *
from Word import *

class LiveThesaurus(object):
    def __init__(self, master):
        self.master = master
        master.title('LiveThesaurus')
        master.option_add('*font', ('Times New Roman', 14))
        
        self.currentWord = None
        self.currentSynDict = None
        self.currentDef = None
        self.currentDefList = [None]
        
        # Code from: https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        screenWidth = master.winfo_screenwidth()
        screenHeight = master.winfo_screenheight()
        master.geometry("%dx%d+0+0" % (screenWidth, screenHeight))        
        
        self.leftFrame = Frame(self.master, borderwidth=2, relief="solid")
        # creates a text box and scroll bar, along with a button that will
        # print synonyms on the right side of the window
        self.textScrollBar = Scrollbar(self.leftFrame)
        self.textBox = Text(self.leftFrame, width=20, height=40, 
                            borderwidth=1, relief="sunken")
        self.getSynButton = Button(self.leftFrame, width=20, height=1, 
                             text="Get Synonyms!", 
                             command=self.updateCurrentWord)
        self.textScrollBar.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.textScrollBar.set)
        
        # packs the textbox, scroll bar, and button all on the left side of the 
        # screen
        self.leftFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.textScrollBar.pack(side=RIGHT, fill=Y)
        self.textBox.pack(side=TOP, fill=BOTH, padx=3, pady=3)
        self.getSynButton.pack(side=TOP, fill=BOTH)
        
        
        # creates the right frame of the window
        self.rightFrame = Frame(self.master, borderwidth=2, relief="solid")
        self.wordInfoFrame = Frame(self.rightFrame, borderwidth=2, 
                                  relief="solid")
        self.synFrame = Frame(self.rightFrame, borderwidth=2, relief="solid")
        self.synList = Listbox(self.synFrame, borderwidth=1, relief="solid")
        
        # creates and packs an option menu for definitions
        self.options = StringVar()
        self.definitionMenu = OptionMenu(self.wordInfoFrame, self.options, 
                              *self.currentDefList)
        self.definitionMenu.pack(side=TOP, fill=X)
        self.options.set(self.currentDefList[0])
        
        # labels for the selected word, current definition, and synonyms
        self.currentWordLabel = Label(self.wordInfoFrame, 
                                 text="Selected Word: " + str(self.currentWord),
                                 borderwidth=1, relief="solid", anchor=N)
        self.definitionLabel = Label(self.wordInfoFrame, 
                          text="Definiton: " + str(self.currentDefList[0]),
                          borderwidth=1, relief="solid", anchor=N)
        self.synonymLabelTitle = Label(self.synFrame, text="List of Synonyms:",
                                  borderwidth=1,
                                  relief="solid", anchor=N)
        
        self.synScrollBar = Scrollbar(self.synList)
        self.synScrollBar.config(command=self.synList.yview)
        self.synList.config(yscrollcommand=self.synScrollBar.set)
        
        self.rightFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        self.wordInfoFrame.pack(side=TOP, fill=X, padx=3, pady=3)
        self.currentWordLabel.pack(side=TOP, fill=X, padx=2, pady=2)
        self.definitionLabel.pack(side=TOP, fill=X, padx=2, pady=2)
        
        self.synFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=3)
        self.synonymLabelTitle.pack(side=TOP, fill=X, padx=2, pady=2)
        self.synList.pack(side=TOP, fill=BOTH, expand=YES, padx=2)
        self.synScrollBar.pack(side=RIGHT, fill=Y)
        self.generateSynonymList()
    
    # gets the prints the highlighted word when button is pressed and sets 
    # the above labels corresponding to the word
    def updateCurrentWord(self):
        try:
            highlightedWord = self.textBox.selection_get()
            self.currentWord = Word(highlightedWord)
            if self.currentWord.isValidWord():
                self.currentWord = Word(highlightedWord)
                self.currentWordLabel.config(text = "Selected Word: " + self.currentWord.word)
                self.currentSynDict = self.currentWord.synonymDict
                self.currentDefList = list(self.currentSynDict.keys())
                self.updateDefMenu()
            else:
                currentWord = None
        except:
            print("No Word Selected")

    # Code from: https://stackoverflow.com/questions/37704176/how-to-update-the-command-of-an-optionmenu
    # Changes the definition label according to the user's choice
    def changeDefLabel(self, *args):
        self.currentDef = str(self.options.get())
        self.definitionLabel.config(text="Definiton: " + self.currentDef)
        self.generateSynonymList()
    
    # updates the definition menu according to the user's choice
    def updateDefMenu(self):
        menu = self.definitionMenu["menu"]
        menu.delete(0, "end")
        for d in self.currentDefList:
            menu.add_command(label=d, 
                    command=lambda value=d: self.options.set(value))
        # gives all options a command associated with changeDefLabel
        self.options.trace("w", self.changeDefLabel)
        self.options.set(self.currentDefList[0])
    
    # draws and creates a synonym list made out of non-changeable entry boxes
    def generateSynonymList(self):
        self.synList.delete(0,'end')
        if self.currentSynDict != None:
            for syn in self.currentSynDict[self.currentDef]:
                self.synList.insert(END, syn["term"])
    
root = Tk()
my_gui = LiveThesaurus(root)
mainloop()