###################
   LiveThesaurus   
###################
https://github.com/EdwardLu2018/LiveThesaurus

Q. What is LiveThesaurus?
A. LiveThesaurus is an application that allows users to input any type of English text and 
manipulate specific words in their text according to synonyms and antonyms from thesaurus.com. 
LiveThesaurus uses web-scraping to parse a javascript dictionary from thesaurus.com containing 
definitions of words mapping to various synonyms. Users can highlight specific words and will 
be given a list of synonyms and antonyms taken from that dictionary. They can click on the synonym
or antonym they want, select a term, and the word turn into the selected term in the text. There 
is also an option to record voice audio, convert it into text, and manipulate the text. 

Q. How do I run LiveThesaurus?
A. Before running LiveThesaurus, you need to download a few modules:
	1. Run the modulesInstaller.py file in the "modules" folder
	2. Download Google Speech API (tutorial from: https://pythonspot.com/speech-recognition-using-google-speech-api/):
		- Install homebrew (https://brew.sh/) if you are using a Mac.
			- for Windows do $ python -m pip3 install pyaudio
		- $ brew install portaudio
		- $ pip3 install pyaudio
		- $ git clone http://people.csail.mit.edu/hubert/git/pyaudio.git
		- $ cd pyaudio
		- $ sudo python setup.py install
		- $ sudo pip3 install SpeechRecognition
	After doing this, please run the init.py file to run LiveThesaurus.

Shortcuts and commands:
	1. Pressing "ENTER", double clicking and pressing the left arrow all switch words with the 
	   selected synonym or antonym
	2. Pressing the audio button and saying "synonyms for [word]" will give you the synonyms for the word.
	   You can also say "synonyms of [word]", "synonym for [word]", or "synonym of [word]". You can also
	   say "antonyms" instead of "synonyms".
	3. Command-a (or Control-a) selects all user entered text
	4. Command-q (or Control-q) quits the application
