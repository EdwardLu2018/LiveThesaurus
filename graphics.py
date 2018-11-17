from tkinter import *
from Word import *

class LiveThesaurus(object):
    def __init__(self, master):
        self.master = master
        master.title('LiveThesaurus')
        master.option_add('*font', ('Times New Roman', 14))
        
        self.currentWord = None
        self.currentSynDict = None
        self.defList = [None]
        
        # https://stackoverflow.com/questions/15981000/tkinter-python-maximize-window
        screenWidth, screenHeight = master.winfo_screenwidth(), master.winfo_screenheight()
        master.geometry("%dx%d+0+0" % (screenWidth, screenHeight))        
        
        self.textScrollFrame = Frame(self.master)
        self.scroll = Scrollbar(self.textScrollFrame)
        self.textBox = Text(self.textScrollFrame, width=20, height=40, borderwidth=2, relief="sunken")
        self.button = Button(self.textScrollFrame, width=20, height=1, text="print highlighted text", 
                            command=self.getHighlightedWord)
        self.scroll.config(command=self.textBox.yview)
        self.textBox.config(yscrollcommand=self.scroll.set)
        
        self.scroll.pack(side=RIGHT, fill=Y)
        self.textBox.pack(side=TOP, fill=BOTH)
        self.button.pack(side=TOP, fill=BOTH)
        self.textScrollFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=5, pady=5)
        
        self.rightFrame = Frame(self.master, borderwidth=2, relief="solid")
        self.innerFrame = Frame(self.rightFrame)
        
        self.options = StringVar()
        self.menu = OptionMenu(self.innerFrame, self.options, *self.defList)
        self.menu.pack(side=TOP, fill=X)
        self.options.set(self.defList[0])
        
        self.selectedWord = Label(self.innerFrame, text="Selected Word: " + str(self.currentWord), borderwidth=2, relief="solid", anchor=N)
        self.defn = Label(self.innerFrame, text="Definiton: " + str(self.defList[0]), borderwidth=2, 
                    relief="solid", anchor=N)
        self.input2 = Label(self.innerFrame, text="Synonyms\nand more!", borderwidth=2, 
                    relief="solid", anchor=N)
        self.selectedWord.pack(side=TOP, fill=X)
        self.defn.pack(side=TOP, fill=X)
        self.input2.pack(side=TOP, fill=X)
        self.rightFrame.pack(side=LEFT, fill=BOTH, expand=YES, padx=3, pady=3)
        self.innerFrame.pack(side=TOP, fill=BOTH, expand=YES, padx=3, pady=3)
    
    def getHighlightedWord(self):
        try:
            highlightedWord = self.textBox.selection_get()
            self.currentWord = Word(highlightedWord)
            if self.currentWord.isValidWord():
                self.currentWord = Word(highlightedWord)
                print(self.currentWord)
                self.selectedWord.config(text = "Selected Word: " + self.currentWord.word)
                self.currentSynDict = self.currentWord.synonymDict
                self.defList = list(self.currentSynDict.keys())
                self.updateDefMenu()
                self.defn.config(text = "Definition: " + self.defList[0])
            else:
                currentWord = None
        except:
            print("No Word Selected")

    # https://stackoverflow.com/questions/37704176/how-to-update-the-command-of-an-optionmenu
    def changeDefLabel(self, *args):
        self.defn.config(text=self.options.get())
    
    def updateDefMenu(self):
        m = self.menu["menu"]
        m.delete(0, "end")
        for d in self.defList:
            m.add_command(label=d, 
                    command=lambda value=d: self.options.set(value))
        self.options.trace("w", self.changeDefLabel)
        self.options.set(self.defList[0])
        
root = Tk()
my_gui = LiveThesaurus(root)
mainloop()