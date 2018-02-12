from flask import Flask, request, render_template, url_for

from data import Data

app = Flask(__name__)

data = Data()

@app.route('/', methods=['GET'])
def index():
    global data
    return render_template('index.html', data=data)



app.run(host="0.0.0.0",port=5001)