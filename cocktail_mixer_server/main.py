from flask import Flask, request, render_template, url_for, session, redirect, flash
from server_config import get_config
from data import Data

app = Flask(__name__)

server_config = get_config()

app.config.from_object(__name__) # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    SECRET_KEY= server_config.get('secret_key', 'dev_key')
))

app.config.from_envvar('FLASKR_SETTINGS', silent=True)


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


@app.route('/maintenance/', methods=['GET', 'POST'])
def maintenance():
    data = Data(server_config=server_config)
    data.view_name = 'Maintenance'

    if request.method == 'POST':
        if not session.get('logged_in', False):
            if server_config.get('maintenance_pin', '0') == '0':
            
                flash('Server-side issue: No pin configured')
                return render_template('maintenance_login.html', data=data)
            
            elif request.form['pin'] != server_config['maintenance_pin']:
            
                flash('Invalid pin!')
                return render_template('maintenance_login.html', data=data)
            
            else:
            
                session['logged_in'] = True
                return redirect(url_for('maintenance'))
        else: ##code for logout
            session['logged_in'] = False
            return redirect(url_for('show_recipes'))
    else:
        print(session.get('logged_in', False))
        if session.get('logged_in', False):
    	    return render_template('ma_supply.html', data=data)
        else:
    	    return render_template('maintenance_login.html', data=data)


@app.route('/set_slot/', methods=['GET'])
def set_slot():
    data = Data(server_config=server_config)

    slot = int(request.args.get('slot', -1))

    if  slot == -1:
        return redirect(url_for('show_recipes'))
    else:
        return render_template('set_slot.html', data=data, slot=str(slot))


def main():


    app.run(host=server_config['flask_host_name'],port=server_config['flask_port'])

if __name__ == '__main__':
    main()
