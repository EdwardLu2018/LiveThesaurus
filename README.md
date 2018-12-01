# LiveThesaurus

Q. What is LiveThesaurus?

A. LiveThesaurus is an application that allows users to input any type of English text and manipulate specific words in their text according to synonyms and antonyms from thesaurus.com. LiveThesaurus uses web-scraping to parse a javascript dictionary from thesaurus.com containing definitions of words mapping to various synonyms. Users can highlight specific words and will be given a list of synonyms and antonyms taken from that dictionary. They can click on the synonym or antonym they want, select a term, and the word turn into the selected term in the text. There will also be an option to record voice audio, convert it into text, and manipulate the text. 


Q. How do I run LiveThesaurus?

A. Before running LiveThesaurus you need to download a few modules.
1. requests: ```$ python3 -m pip install requests```
2. BeautifulSoup: ```$ python3 -m pip install beautifulsoup4```
3. inflect: ```$ pip3 install inflect```
4. nltk: ```$ sudo pip install -U nltk```
5. Run the nltkInstall.py file
After doing this, please run the __init__.py file to run LiveThesaurus


Shortcuts and commands:

1. Pressing "ENTER", double clicking and pressing the left arrow all switch words with the selected synonym or antonym<br>
2. Command-a (or Control-a) selects all user entered text<br>
3. Command-q quits the application<br>
