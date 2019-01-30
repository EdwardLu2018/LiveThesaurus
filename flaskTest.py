from __future__ import print_function
from flask import Flask, request, redirect, url_for, render_template
import sys
from src.Word import *

app = Flask(__name__)

# sudo lsof -i:5000
# kill PID

@app.route("/")
def index():
    return render_template("LiveThesaurus.html")

# @app.route('/')
# @app.route('/<word>')
# def my_form_post(name=None):
#     return render_template('LiveThesaurus.html', name=word)

# @app.route("/#app", methods=["POST"])
# def my_form_post():
#     text = request.form['text']
#     print(text, file=sys.stderr)
#     return redirect("/")

@app.route('/handle_data', methods=['POST'])
def handle_data():
    projectpath = request.form['text']
    # your code
    # return a response
    print(projectpath, file=sys.stderr)
    return redirect("/#app")

if __name__ == '__main__':
	app.run(debug=True)