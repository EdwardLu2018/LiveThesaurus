## Runs LiveThesaurus application

from tkinter import *
import src.LiveThesaurus as LT

def main():
    # Creates a LiveThesaurus application and runs it
    root = Tk()
    application = LT.LiveThesaurus(root)
    application.run()

if __name__ == "__main__":
    main()
