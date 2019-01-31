from __future__ import print_function
from flask import Flask, request, redirect, url_for, render_template, Response, jsonify
import sys
# from src.Word import *

app = Flask(__name__)

# sudo lsof -i:5000
# kill PID

# @app.route("/")
# def index():
#     return render_template("LiveThesaurus.html")

word = "none"

@app.route('/', methods=['POST', "GET"])
def send():
    return render_template('LiveThesaurus.html', word=word)

@app.route('/getData', methods=['POST', 'GET'])
def getData():
	data = request.get_json()
	word = data["currWord"]
	print(word, file=sys.stderr)
	send()
	return jsonify(status="success", data=data)

if __name__ == '__main__':
	app.run(debug=True)