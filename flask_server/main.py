from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

counter = 0

@app.route('/test/')
def get_test():
    return render_template('test.html')

@app.route('/post_data/', methods=['POST'])
def post_data():
    counter = int(counter) + 1
    return redirect(url_for('test'))


app.run(host="0.0.0.0", port=5001)

