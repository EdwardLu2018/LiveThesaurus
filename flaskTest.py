from __future__ import print_function
from flask import Flask, request, redirect, url_for, render_template
import sys
from src.Word import *

app = Flask(__name__)

# sudo lsof -i:5000
# kill PID

@app.route("/", methods=['GET', 'POST'])
def init():
    return render_template("LiveThesaurus.html")

# @app.route('/', methods=['POST'])
# def my_form_post():
#     text = request.form['text']
#     processed_text = text.upper()
#     inputVar = processed_text
#     print(inputVar, file=sys.stderr)
#     return redirect("/")

if __name__ == '__main__':
	app.run(debug=True)