#!/usr/bin/python3
''' script that starts a Flask web application '''

from flask import Flask

app = Flask(__name__)
app.url_map.strict_slashes = False


@app.route("/")
def hello():
    ''' /: displays Hello HBNB! '''
    return "Hello HBNB!"


@app.route("/hbnb")
def hbnb():
    ''' /hbnb: displays HBNB '''
    return "HBNB"


@app.route("/c/<text>")
def C_text(text):
    ''' /c/<text>: display C followed by the value of the text variable '''
    text = text.replace("_", " ")
    return "C {}".format(text)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
