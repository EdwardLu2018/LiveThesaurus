## Runs LiveThesaurus application

from tkinter import *
import src.LiveThesaurus as LT

# creates a LiveThesaurus application and runs it
root = Tk()
application = LT.LiveThesaurus(root)
application.run()