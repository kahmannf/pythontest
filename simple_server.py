from flask import Flask

app = new Flask(__name__)

@app.route("/")
def test():
    print("test")
    return 0

@app.route("/hello")
def hello():
    return "Hello World"
