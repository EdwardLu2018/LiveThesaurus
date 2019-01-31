from __future__ import print_function
from flask import Flask, request, redirect, url_for, render_template, Response, jsonify
import sys
from src.Word import *

app = Flask(__name__)

# sudo lsof -i:5000
# kill PID

word = "none"

# initial load
@app.route("/", methods=["POST", "GET"])
def sendData():
    return render_template("LiveThesaurus.html", word=word)

# when POST method is called from website
@app.route("/getData", methods=["POST", "GET"])
def getData():
	data = request.get_json()
	word = str(data["currWord"])
	wordObj = Word(word)
	if not wordObj.hasSynOrAnt():
		return jsonify({ "currWord": 0 })
	else:
		print(wordObj.word, file=sys.stderr)
		defList = wordObj.definitionList
		synList = wordObj.synonymDict
		return jsonify({ "currWord":word, "defList":defList, "synList":synList})

if __name__ == '__main__':
	app.run(debug=True)