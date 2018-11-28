import requests
from bs4 import BeautifulSoup
# verb file from NodeBox Linguistics:
# https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation
from verb import verb_tense, verb_conjugate
import inflect
inflect = inflect.engine()
import nltk as nltk

class Word(object):
    def __init__(self, word):
        self.word = word
        self.thesaurusSourceText = self.getThesaurusWebText()
        self.parser = BeautifulSoup(self.thesaurusSourceText, 'html.parser')
        self.script = self.getScript()
        self.definitionList = self.getDefList()
        self.synonymDict = self.getDict("synonyms")
        self.antonymDict = self.getDict("antonyms")
    
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
    
    # checks if word has synonyms or antonyms
    def hasSynOrAnt(self):
        return not ("no thesaurus results" in self.thesaurusSourceText or \
                    "\n" in self.word or "\t" in self.word)
    
    # gets a javascript dictionary containing defintions, parts of speech, 
    # synonyms and antonyms
    def getScript(self):
        scriptList = self.parser.find_all("script")
        
        # finds the index of the javascript dictionary that contains the 
        # defintions, synonyms, etc
        indexOfImportantDict = -1
        for script in scriptList:
            if "window.INITIAL_STATE = " not in str(script):
                indexOfImportantDict += 1
        
        # parses javascript code
        lenOfIgnore = len("window.INITIAL_STATE = ")
        script = scriptList[indexOfImportantDict]
        script = script.text[lenOfIgnore:-1] # subtract 1 to remove closing "}" 
                                             # of javascript dictionary
        script = script.replace("null", "None")
        self.script = script.replace("%20", " ")
        self.script = script.replace("\\u002F", "/")
        
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
            definition = script[startIndexOfDef:endIndexOfDef]
            script = script[endIndexOfDef:]
            
            # finds part of speech
            startIndexOfPos = script.find("\"pos\":") + len("\"pos\":") + 1
            endIndexOfPos = startIndexOfPos + script[startIndexOfPos:].find(",\"") - 1
            partOfSpeech = script[startIndexOfPos:endIndexOfPos]
            script = script[endIndexOfPos:]
            
            if partOfSpeech == "noun":
                if self.checkSingOrPlur(self.word) == "plural":
                    definition = self.makePhrasePlural(definition)
            elif partOfSpeech == "verb":
                try:
                    wordTense = verb_tense(self.word)
                    definition = self.conjugatePhrase(definition, wordTense)
                except:
                    pass
            
            definitionList += [definition + " (" + partOfSpeech + ")"]
        
        return definitionList
        
    # returns a dictionary mapping the definition of a given word to its 
    # synonyms or antonyms, depending on the type
    def getDict(self, type):
        script = self.script
        result = {}
        
        # updates result, mapping definitions to their synonyms
        for defn in self.definitionList:
            startIndex = script.find("\"" + type + "\":") + len("\"" + type + "\":")
            endIndex = startIndex + script[startIndex:].find("]")
            termListStr = script[startIndex:endIndex] + "]"
            termList = eval(termListStr)
            
            posStartIndex = defn.find("(") + 1
            posEndIndex = defn.find(")")
            pos = defn[posStartIndex:posEndIndex]
            
            if pos == "noun":
                if self.checkSingOrPlur(self.word) == "plural":
                    for termSet in termList:
                        newTerm = self.makePhrasePlural(termSet["term"])
                        termSet["term"] = newTerm
            # conjugates every term if the part of speech is a verb
            elif pos == "verb":
                try:
                    wordTense = verb_tense(self.word)
                    for termSet in termList:
                        newTerm = self.conjugatePhrase(termSet["term"], wordTense)
                        termSet["term"] = newTerm
                except:
                    pass
            
            result[defn] = termList
            script = script[endIndex:]
        
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
    
    # conjugates a word into a given tense
    def conjugate(self, word, tense):
        try:
            word = verb_conjugate(word, tense)
        except:
            pass
            
        return word
    
    # conjugates a phrase into a certain tense
    def conjugatePhrase(self, phrase, tense):
        # splits a phrase into seperate words and conjugates accoringly
        
        # if there is a comma, then there are multiple verbs in the 
        # phrase and each verb must be conjugated
        if ", " in phrase:
            phraseWords = phrase.split(", ")
            for i in range(len(phraseWords)):
                word = phraseWords[i]
                word = self.conjugate(word, tense)
                phraseWords[i] = word
                # if there are multiple words, conjugate first word
                if " " in phraseWords[i]:
                    wordsInPhrase = phraseWords[i].split(" ")
                    firstWord = wordsInPhrase[0]
                    firstWord = self.conjugate(firstWord, tense)
                    wordsInPhrase[0] = firstWord
                    phraseWords[i] = " ".join(wordsInPhrase)
            phrase = ", ".join(phraseWords)
        # if there are no commas, but the phrase has multiple words, only 
        # conjugate the first verb
        elif " " in phrase:
            phraseWords = phrase.split(" ")
            for i in range(len(phraseWords)):
                word = phraseWords[i]
                word = self.conjugate(word, tense)
                phraseWords[i] = word
            phrase = " ".join(phraseWords)
        # if there is only one verb in the phrase, then just conjugate the 
        # phrase
        else:
            phrase = self.conjugate(phrase, tense)
            
        return phrase
        
    # checks if a noun is singular or plural
    def checkSingOrPlur(self, noun):
        if inflect.singular_noun(noun):
            return "plural"
        else:
            return "singular"
    
    # makes a noun plural if it's singular
    def makePlural(self, noun):
        try:
            if self.checkSingOrPlur(noun) == "singular":
                noun = inflect.plural(noun)
        except:
            pass
            
        return noun
        
    # turns a phrase into its plural form
    def makePhrasePlural(self, phrase):
        # pluralize with inflect if there is a comma in the phrase
        if "," in phrase:
            phrase = inflect.plural(phrase)
            
        # tokenizes the words and creates a list of tuples containing words
        # and their POS
        phraseList = nltk.word_tokenize(phrase)
        posTags = nltk.pos_tag(phraseList)
        
        # finds index of first noun and makes that noun plural
        indexOfFirstNoun = 0
        for i in range(len(posTags)):
            if posTags[i][1] == "NN":
                indexOfFirstNoun = i
                break
        phraseList[indexOfFirstNoun] = self.makePlural(phraseList[indexOfFirstNoun])
        
        phrase = " ".join(phraseList)
        phrase = phrase.replace(" ,", ",")
        
        return phrase
    
    # string representation
    def __repr__(self):
        return "Word: " + self.word
    
    # hash function
    def __hash__(self):
        return hash(self.word)
    
    # equivalence check
    def __eq__(self, other):
        return isinstance(other, Word) and self.word == other.word