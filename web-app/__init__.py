from __future__ import print_function
from flask import Flask, request, render_template, jsonify, url_for
from word import Word

app = Flask(__name__)

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
		defList = wordObj.definitionList
		synList = wordObj.synonymDict
		return jsonify({ "currWord":word, "defList":defList, "synList":synList})

if __name__ == "__main__":
	app.run(debug=True)
