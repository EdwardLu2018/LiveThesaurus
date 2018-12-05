# LiveThesaurus

## What is LiveThesaurus?

LiveThesaurus is an application that allows users to input any type of English text and 
manipulate specific words in their text according to synonyms and antonyms from thesaurus.com. 
LiveThesaurus uses web-scraping to parse a javascript dictionary from thesaurus.com containing 
definitions of words mapping to various synonyms. Users can highlight specific words and will 
be given a list of synonyms and antonyms taken from that dictionary. They can click on the synonym
or antonym they want, select a term, and the word turn into the selected term in the text. There 
is also an option to record voice audio, convert it into text, and manipulate the text. 


## How do I run LiveThesaurus?

Before running LiveThesaurus, you need to download a few modules:
1. requests: ```$ python3 -m pip install requests```
2. BeautifulSoup: ```$ python3 -m pip install beautifulsoup4```
3. inflect: ```$ pip3 install inflect```
4. nltk: ```$ sudo pip3 install -U nltk```
5. run the nltkInstall.py file
6. Google Speech API (tutorial from: https://pythonspot.com/speech-recognition-using-google-speech-api/):<br>
	- ```$ git clone http://people.csail.mit.edu/hubert/git/pyaudio.git```<br>
	- ```$ cd pyaudio```<br>
	- ```$ sudo python setup.py install```<br>
	- ```$ sudo pip3 install SpeechRecognition```

If modules are not installed, try pip[your python version], for example, pip3.6

After doing this, please run the __init__.py file to run LiveThesaurus


## Shortcuts and commands:

1. Pressing "ENTER", double clicking, and pressing the left arrow all switch words with the 
   selected synonym or antonym<br>
2. Pressing the audio button and saying "synonyms for [word]" will give you the synonyms for the word.
   You can also say "synonyms of [word]", "synonym for [word]", or "synonym of [word]". You can also
   say "antonyms" instead of "synonyms".
3. Command-a (or Control-a) selects all user entered text<br>
4. Command-q (or Control-q) quits the application<br>
