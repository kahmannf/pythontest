from flask import Flask, request, render_template, url_for
from server_config import get_config
from data import Data



app = Flask(__name__)

server_config = get_config()

@app.route('/', methods=['GET'])
def show_recipes():
    data = Data(server_config=server_config)
    
    return render_template('show_recipes.html', data=data)


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