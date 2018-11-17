import requests
from bs4 import BeautifulSoup

class Word(object):
    def __init__(self, word):
        self.word = word
        self.thesaurusSourceText = self.getThesaurusWebText()
        self.parser = BeautifulSoup(self.thesaurusSourceText, 'html.parser')
        self.synonymDict = self.getSynonymDict()

    # checks if word is invalid
    def isValidWord(self):
        return not "no thesaurus results" in self.thesaurusSourceText
        
    # returns a dictionary mapping the definition of a given word to its synonyms
    def getSynonymDict(self):
        definitionList = []
        synonymDict = {}
        
        if not self.isValidWord():
            return None
        
        # parses the javascript code with the dictionary of synonyms for word
        indexOfSynonyms = 15
        lenOfIgnore = len("window.INITIAL_STATE = ")
        script = self.parser.find_all("script")[indexOfSynonyms]
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
            
        # updates synonymDict mapping definitions to their synonyms
        for defn in definitionList:
            index1 = copyScript.find("\"synonyms\":") + len("\"synonyms\":")
            index2 = index1 + copyScript[index1:].find("]")
            synonyms = copyScript[index1:index2] + "]"
            synonymsList = eval(synonyms)
            synonymDict[defn] = synonymsList
            copyScript = copyScript[index2:]
        
        # removes unecessary keys
        for defn in synonymDict:
            listOfAllSyns = synonymDict[defn]
            for synDict in reversed(listOfAllSyns):
                if "isInformal" in synDict.keys() and \
                "targetTerm" in synDict.keys() and \
                "targetSlug" in synDict.keys():
                    del synDict["isInformal"]
                    del synDict["targetTerm"]
                    del synDict["targetSlug"]
                if "isVulgar" in synDict.keys():
                    if synDict["isVulgar"] != None:
                        listOfAllSyns.remove(synDict)
                    else:
                        del synDict["isVulgar"]
        
        return synonymDict
    
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
    
    def __repr__(self):
        return "Word: " + self.word
