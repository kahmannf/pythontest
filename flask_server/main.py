from flask import Flask, request, render_template, redirect, url_for

app = Flask(__name__)

@app.route('/test/')
def get_test():
    return render_template('test.html')

@app.route('/post_data/', methods=['POST'])
def post_data():
    return redirect(url_for('success.html'))


app.run(host="0.0.0.0", port=5001)

