import requests
from bs4 import BeautifulSoup

class Word(object):
    def __init__(self, word):
        self.word = word
        self.thesaurusSourceText = self.getThesaurusWebText()
        self.parser = BeautifulSoup(self.thesaurusSourceText, 'html.parser')
        self.script = self.getScript()
        if self.hasSynOrAnt():
            self.definitionList = self.getDefList()
            self.synonymDict = self.get("synonyms")
            self.antonymDict = self.get("antonyms")
        else:
            self.definitionList = None
            self.synonymDict = None
            self.antonymDict = None
    
    # gets the html text of thesaurus.com at a given word
    def getThesaurusWebText(self):
        HTMLTextWord = self.word.lower()
        if HTMLTextWord == "" or HTMLTextWord.isdigit() or HTMLTextWord.isspace():
            return None
        elif " " in HTMLTextWord:
            HTMLTextWord = HTMLTextWord.replace(" ", "%20")
        url = "https://www.thesaurus.com/browse/"
        thesaurusWebsite = requests.get(url + HTMLTextWord + "?s=t")
        return thesaurusWebsite.text 
    
    # checks if word is invalid
    def hasSynOrAnt(self):
        return not ("no thesaurus results" in self.thesaurusSourceText or \
                    "\n" in self.word or "\t" in self.word)
    
    # gets a javascript dictionary containing defintions, parts of speech, 
    # synonyms and antonyms
    def getScript(self):
        # parses javascript code
        indexOfImportantDict = 15
        lenOfIgnore = len("window.INITIAL_STATE = ")
        script = self.parser.find_all("script")[indexOfImportantDict]
        script = script.text[lenOfIgnore:-1] # subtract 1 to remove closing "}" 
                                             # of javascript dictionary
        script = script.replace("null", "None")
        self.script = script.replace("%20", " ")
        return self.script
    
    # gets a list of defintions of the word
    def getDefList(self):
        script = self.script
        definitionList = []
        
        # updates definitionList with all definitions of word
        while "\"0\",\"definition\":" in script and "\"pos\":":
            defn = ""
            pos = ""
            
            # finds definitions
            startIndexOfDef = script.find("\"definition\":") + len("\"definition\":") + 1
            endIndexOfDef = startIndexOfDef + script[startIndexOfDef:].find(",\"") - 1
            defnition = script[startIndexOfDef:endIndexOfDef]
            script = script[endIndexOfDef:]
            
            # finds part of speech
            startIndexOfPos = script.find("\"pos\":") + len("\"pos\":") + 1
            endIndexOfPos = startIndexOfPos + script[startIndexOfPos:].find(",\"") - 1
            partOfSpeech = script[startIndexOfPos:endIndexOfPos]
            script = script[endIndexOfPos:]
            
            definitionList += [defnition + " (" + partOfSpeech + ")"]
        
        return definitionList
        
    # returns a dictionary mapping the definition of a given word to its 
    # synonyms or antonyms, depending on the type
    def get(self, type):
        script = self.script
        result = {}
        
        # updates result, mapping definitions to their synonyms
        for defn in self.definitionList:
            index1 = script.find("\"" + type + "\":") + len("\"" + type + "\":")
            index2 = index1 + script[index1:].find("]")
            synOrAntListStr = script[index1:index2] + "]"
            synOrAntList = eval(synOrAntListStr)
            result[defn] = synOrAntList
            script = script[index2:]
        
        # removes unecessary keys
        for defn in result:
            listOfAllTerms = result[defn]
            for dict in reversed(listOfAllTerms):
                if "isInformal" in dict.keys() and \
                "targetTerm" in dict.keys() and \
                "targetSlug" in dict.keys():
                    del dict["isInformal"]
                    del dict["targetTerm"]
                    del dict["targetSlug"]
                if "isVulgar" in dict.keys():
                    if dict["isVulgar"] != None:
                        listOfAllTerms.remove(dict)
                    else:
                        del dict["isVulgar"]
        
        return result
    
    # string representation
    def __repr__(self):
        return "Word: " + self.word
    
    # hash function
    def __hash__(self):
        return hash(self.word)
    
    # equivalence check
    def __eq__(self, other):
        return isinstance(other, Word) and self.word == other.word