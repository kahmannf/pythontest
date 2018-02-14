from flask import Flask, request, render_template, url_for
from server_config import get_config
from data import Data



app = Flask(__name__)

server_config = get_config()

@app.route('/', methods=['GET'])
def show_recipes():
    data = Data(server_config=server_config)

    data.view_name = 'Menu'

    return render_template('show_recipes.html', data=data)

@app.route('/filtered/', methods=['GET'])
def show_recipes_filtered():
    data = Data(server_config=server_config)

    data.view_name = 'Menu'

    data.filter_recipes()

    return render_template('show_recipes.html', data=data)


@app.route('/maintenance/', methods=['GET'])
def maintenance():
	if session['logged_in']:
		return render_template('maintenance.html')
	else:
		return render_template('maintenance_login.html')

@app.route('/login/', methods=['POST'])
def login():
	if request.form['pin'] != server_config['maintenance_pin']:
		return render_template('maintenance_login.html', error='Invalid pin!')
	else:
		session['logged_in'] = True
		return redirect(url_for('maintenance'))

def main():
    ##data = Data()

    ##data.recipes = load_recipes('dir')

    ##print (data.recipes)

    ##for recipe in data.recipes:
    ##    print(recipe)
    ##    print(recipe.get('name'))
    app.run(host=server_config['flask_host_name'],port=server_config['flask_port'])

if __name__ == '__main__':
    main()
