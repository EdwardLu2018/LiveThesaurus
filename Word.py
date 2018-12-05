## Word class. Creates a class that has the synonyms/antonyms, definitions, and
## tense of a word, given that the word has those properties on thesaurus.com

import requests
from bs4 import BeautifulSoup
# verb file from NodeBox Linguistics:
# https://www.nodebox.net/code/index.php/Linguistics#verb_conjugation
from verb import *
import inflect
inflect = inflect.engine()
import nltk as nltk

class Word(object):
    def __init__(self, word):
        self.word = word.lower()
        self.thesaurusSourceText = self.getThesaurusWebText()
        if self.thesaurusSourceText != None:
            self.parser = BeautifulSoup(self.thesaurusSourceText, "html.parser")
            self.script = self.getScript()
            self.wordTense = getVerbTense(self.word)
            self.synonymDict = self.getDict("synonyms", self.wordTense)
            self.antonymDict = self.getDict("antonyms", self.wordTense)
            # definitions are the keys of the synonymDict on thesaurus.com
            self.definitionList = list(self.synonymDict.keys())
    
    # gets the html text of thesaurus.com at a given word
    def getThesaurusWebText(self):
        HTMLTextWord = self.word
        if HTMLTextWord == "" or HTMLTextWord.isdigit() or HTMLTextWord.isspace():
            return None
        elif " " in HTMLTextWord:
            HTMLTextWord = HTMLTextWord.replace(" ", "%20")
        url = "https://www.thesaurus.com/browse/"
        thesaurusWebsite = requests.get(url + HTMLTextWord + "?s=t")
        return thesaurusWebsite.text 
    
    # checks if word has synonyms or antonyms
    def hasSynOrAnt(self):
        if self.thesaurusSourceText == None:
            return False
        return not ("no thesaurus results" in self.thesaurusSourceText or \
                    "\t" in self.word)
    
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
    
    # gets a list of defintions of the word in it curretn tense
    def getInitialDefList(self, tense):
        script = self.script
        definitionList = []
        
        # updates definitionList with all definitions of word
        while "\"0\",\"definition\":" in script and "\"pos\":":
            defn = ""
            pos = ""
            
            # finds definitions
            startIndexOfDef = script.find("\"definition\":") + \
                              len("\"definition\":") + 1
            endIndexOfDef = startIndexOfDef + \
                            script[startIndexOfDef:].find(",\"") - 1
            definition = script[startIndexOfDef:endIndexOfDef]
            script = script[endIndexOfDef:]
            
            # finds part of speech
            startIndexOfPos = script.find("\"pos\":") + len("\"pos\":") + 1
            endIndexOfPos = startIndexOfPos + \
                            script[startIndexOfPos:].find(",\"") - 1
            partOfSpeech = script[startIndexOfPos:endIndexOfPos]
            script = script[endIndexOfPos:]
            
            # if the word is plural, make all its definitions plural
            if partOfSpeech == "noun":
                if getPOS(self.word) == "plural":
                    definition = makePhrasePlural(definition)
            # match definitions to the word tense if word is a verb
            elif partOfSpeech == "verb":
                wordTense = tense
                definition = conjugatePhrase(definition, wordTense)
            
            definitionList += [definition + " (" + partOfSpeech + ")"]
        
        return definitionList
        
    # returns a dictionary mapping the definition of a given word to its 
    # synonyms or antonyms, depending on the type
    def getDict(self, type, tense):
        script = self.script
        result = {}
        
        # updates result, mapping definitions to their synonyms
        for defn in self.getInitialDefList(tense):
            startIndex = script.find("\"" + type + "\":") + \
                         len("\"" + type + "\":")
            endIndex = startIndex + script[startIndex:].find("]")
            termListStr = script[startIndex:endIndex] + "]"
            termList = eval(termListStr)
            
            posStartIndex = defn.find("(") + 1
            posEndIndex = defn.find(")")
            pos = defn[posStartIndex:posEndIndex]
            
            # if the word is plural, make all its syns and ants plural
            if pos == "noun":
                if getPOS(self.word) == "plural":
                    for termSet in termList:
                        newTerm = makePhrasePlural(termSet["term"])
                        termSet["term"] = newTerm
            # match syns and ants to the word tense if word is a verb
            elif pos == "verb" and tense != None:
                for termSet in termList:
                    newTerm = conjugatePhrase(termSet["term"], tense)
                    termSet["term"] = newTerm
            
            result[defn] = termList
            script = script[endIndex:]
        
        # removes unecessary keys
        for defn in result:
            listOfAllTerms = result[defn]
            for dict in reversed(listOfAllTerms):
                del dict["isInformal"]
                del dict["targetTerm"]
                del dict["targetSlug"]
                if dict["isVulgar"] != None or dict["term"] == "":
                    listOfAllTerms.remove(dict)
        
        infinitiveVerbDict = getInfinitiveVerbDict(self.word, self.wordTense, 
                                                   type)
        if infinitiveVerbDict != None:
            result.update(infinitiveVerbDict)
        
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

## Natural Language Processing Helper Methods:
# gets the tense of a word if the word is a verb
def getVerbTense(word):
    wordTense = None # word is not a verb or has no tense
    try:
        wordTense = verb_tense(word)
        # some words can't be conjugated in first/second-person singular, 
        # so make the tense past if the original word is in 1st/2nd-person
        # singular past, and present if word is in 1st/2nd-person
        # singular present
        if "1st singular past" == wordTense or \
           "2nd singular past" == wordTense:
            wordTense = "past"
        elif "1st singular present" == wordTense or \
             "2nd singular present" == wordTense:
            wordTense = "present"
    except:
        pass
        
    return wordTense

# returns a synonym or antonym dict of the infinitive form of a verb
def getInfinitiveVerbDict(word, tense, type):
    infinitiveDict = None
    try:
        # if the tense is infinitive, don't get the infinitive verb dictionary
        if tense != "infinitive":
            infinitive = verb_infinitive(word)
            infinitiveWordObj = Word(infinitive)
            
            if type == "synonyms":
                infinitiveDict = infinitiveWordObj.getDict("synonyms", tense)
            elif type == "antonyms":
                infinitiveDict = infinitiveWordObj.getDict("antonyms", tense)
            
            # infinitive verb dictionary should not have terms that are not verbs
            for defn in reversed(list(infinitiveDict.keys())):
                posStartIndex = defn.find("(") + 1
                posEndIndex = defn.find(")")
                pos = defn[posStartIndex:posEndIndex]
                if pos != "verb":
                    del infinitiveDict[defn]
            
        return infinitiveDict
    except:
        return infinitiveDict

# conjugates a word into a given tense
def conjugate(word, tense):
    try:
        word = verb_conjugate(word, tense)
        return word
    except:
        return word

# conjugates a phrase into a certain tense
def conjugatePhrase(phrase, tense):
    # splits a phrase into seperate words and conjugates accoringly
    phraseWords = None
    
    # if there is a comma or semicolon, then there are multiple phrases in  
    # the phrase and each phrase within the larger phrase must be conjugated
    if ", " in phrase or "; " in phrase:   
        if "; " in phrase:
            phrases = phrase.split("; ")
        elif ", " in phrase:
            phrases = phrase.split(", ")
        
        for i in range(len(phrases)):
            phrases[i] = conjugatePhrase(phrases[i], tense)
        
        if "; " in phrase:
            phrase = "; ".join(phrases)
        elif ", " in phrase:
            phrase = ", ".join(phrases)
    
    # if there are no commas, but the phrase has multiple words, only 
    # conjugate the first verb
    elif " " in phrase:
        phraseWords = phrase.split(" ")
        for i in range(len(phraseWords)):
            word = phraseWords[0]
            word = conjugate(word, tense)
            phraseWords[0] = word
        phrase = " ".join(phraseWords)
    
    # if there is only one verb in the phrase, then just conjugate the 
    # phrase
    else:
        phrase = conjugate(phrase, tense)
    
    return phrase
    
# checks if a noun is singular or plural
def getPOS(noun):
    if inflect.singular_noun(noun):
        return "plural"
    else:
        return "singular"

# makes a noun plural if it's singular
def makePlural(noun):
    # these words do not have plural forms
    if noun == "somebody" or noun == "something" or noun == "someone":
        return noun
    try:
        if getPOS(noun) == "singular":
            noun = inflect.plural(noun)
        return noun
    except:
        return noun
    
# pluralizes a phrase
def makePhrasePlural(phrase):
    # split the phrase if there is a comma/semicolon in the phrase
    if ", " in phrase or "; " in phrase:
        if "; " in phrase:
            phrases = phrase.split("; ")
        elif ", " in phrase:
            phrases = phrase.split(", ")

        for i in range(len(phrases)):
            phrases[i] = makePhrasePlural(phrases[i])

        if "; " in phrase:
            phrase = "; ".join(phrases)
        elif ", " in phrase:
            phrase = ", ".join(phrases)
    
    # tokenizes the words and creates a list of tuples containing words
    # and their POS
    phraseList = nltk.word_tokenize(phrase)
    posTags = nltk.pos_tag(phraseList)
    
    # finds index of first noun and makes that noun plural
    # finds index of first verb and turns that verb into infinitive tense
    indexOfFirstNoun = 0
    indexOfFirstVerb = 0
    if "one" != posTags[0][0]:
        for i in range(len(posTags)):
            if "NN" in posTags[i][1]:
                indexOfFirstNoun = i
                break

    for i in range(len(posTags)):
        if "VB" in posTags[i][1]:
            indexOfFirstVerb = i
            break

    indexOfLastNounUntilVerb = indexOfFirstNoun
    # if the first noun is "one", make "one" plural
    if "one" == posTags[0][0]:
        phraseList[indexOfFirstNoun] = "ones"
    else:
        # finds the index of the last noun before the first verb
        while indexOfLastNounUntilVerb + 1 < len(posTags) and \
              "NN" in posTags[indexOfLastNounUntilVerb + 1][1]:
            indexOfLastNounUntilVerb += 1
        # ignore cases where the last noun before a verb is "who"
        if phraseList[indexOfLastNounUntilVerb] == "who":
            indexOfLastNounUntilVerb -= 1
        
        phraseList[indexOfLastNounUntilVerb] = makePlural(phraseList[indexOfLastNounUntilVerb])

    if indexOfLastNounUntilVerb != indexOfFirstVerb:
        if posTags[indexOfFirstVerb][1] != "VBN": # for verbs that end in "en", singular and 
                                                  # plural subjects do not matter
            phraseList[indexOfFirstVerb] = conjugate(phraseList[indexOfFirstVerb], 
                                                     "infinitive")

    phrase = " ".join(phraseList)
    phrase = phrase.replace(" ,", ",")
    phrase = phrase.replace(" ;", ";")
    
    return phrase