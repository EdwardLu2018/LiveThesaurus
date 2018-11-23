import requests
from bs4 import BeautifulSoup

class Word(object):
    def __init__(self, word):
        self.word = word
        self.thesaurusSourceText = self.getThesaurusWebText()
        self.parser = BeautifulSoup(self.thesaurusSourceText, 'html.parser')
        self.synonymDict = self.get("synonyms")
        self.antonymDict = self.get("antonyms")
    
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
    def isValidWord(self):
        return not ("no thesaurus results" in self.thesaurusSourceText or \
               "\n" in self.word or "\t" in self.word)
        
    # returns a dictionary mapping the definition of a given word to its 
    # synonyms or antonyms, depending on the type
    def get(self, type):
        definitionList = []
        result = {}
        
        if not self.isValidWord():
            return None
        
        # parses javascript code
        indexOfImportantDict = 15
        lenOfIgnore = len("window.INITIAL_STATE = ")
        script = self.parser.find_all("script")[indexOfImportantDict]
        script = script.text[lenOfIgnore:-1]
        script = script.replace("null", "None")
        script = script.replace("%20", " ")
        copyScript = script
        
        # updates definitionList with all definitions of word
        while "\"0\",\"definition\":" in script:
            index1 = script.find("\"definition\":") + len("\"definition\":") + 1
            index2 = index1 + script[index1:].find(",\"") - 1
            defn = script[index1:index2]
            definitionList += [defn]
            script = script[index2:]
            
        # updates result, mapping definitions to their synonyms
        for defn in definitionList:
            index1 = copyScript.find("\"" + type + "\":") + len("\"" + type + "\":")
            index2 = index1 + copyScript[index1:].find("]")
            synOrAntListStr = copyScript[index1:index2] + "]"
            synOrAntList = eval(synOrAntListStr)
            result[defn] = synOrAntList
            copyScript = copyScript[index2:]
        
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
    
    def __repr__(self):
        return "Word: " + self.word
    
    def __hash__(self):
        return hash(self.word)
    
    def __eq__(self, other):
        return isinstance(other, Word) and self.word == other.word
