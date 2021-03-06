# LiveThesaurus

## What is LiveThesaurus? 
LiveThesaurus is an application that allows users to input any type of English text and manipulate specific words in their text according to synonyms and antonyms from thesaurus.com. LiveThesaurus uses web scraping to parse a javascript dictionary from [thesaurus.com](thesaurus.com) containing definitions of words mapping to various synonyms. Users can highlight specific words and will be given a list of synonyms and antonyms taken from that dictionary. Then, they can double-click on the synonym or antonym they want, select a term, and their highlighted word will swap with the selected term in the text. There is also an option to record voice audio, convert it into text, and manipulate the text.

LiveThesaurus is a Term Project for the course 15-112 "Fundamentals of Programming and Computer
Science" at Carnegie Mellon University.

## How do I run LiveThesaurus?
### Python:
Install dependencies:
```
$ pip3 install -r python-app/requirements.txt
```
Run application:
```
$ python3 python-app/
```

### Website (Work in progress):
Visit this [website](https://livethesaurus.herokuapp.com/)<br>
[![Website Link](https://github.com/EdwardLu2018/LiveThesaurus/blob/master/readme/web-app.gif)](https://livethesaurus.herokuapp.com/)

## Video:
[![Video Link](https://github.com/EdwardLu2018/LiveThesaurus/blob/master/readme/img.png)](https://youtu.be/QUXn-8Eoq7w)

## Shortcuts and commands (for Python version only):
- Pressing "ENTER", double clicking, and pressing the left arrow all switch words with the selected synonym or antonym<br>
- Pressing the audio button and saying "synonyms for [word]" will give you the synonyms for the word.
    - You can also say "synonyms of [word]", "synonym for [word]", or "synonym of [word]". You can also
    - say "antonyms" instead of "synonyms".
- Command-a (or Control-a) selects all user entered text<br>
- Command-q (or Control-q) quits the application<br>
