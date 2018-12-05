## Runs LiveThesaurus application

from tkinter import *
import LiveThesaurus as application

# creates a LiveThesaurus application and runs it
root = Tk()
application = application.LiveThesaurus(root)
application.run()