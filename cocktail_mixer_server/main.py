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

    data.view_name = 'Available recipes'

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


@app.route('/set_slot/', methods=['GET','POST'])
def set_slot():
    data = Data(server_config=server_config)

    if not session.get('logged_in', False):
        return redirect(url_for('maintenance'))

    if request.method == 'POST':
        slot =int(request.form.get('slot', -1))
        beverage_name = request.form.get('beverage', None)
        amount = int(request.form.get('amount', 0))

        error_messages = []

        if slot < 0:
            error_messages.append('Invalid slot number: %s' % slot)
        
        if amount < 0:
            error_messages.append('Invalid amount: %s' % amount)
        
        beverage = data.get_beverage(beverage_name)

        if not beverage:
            error_messages.append('Unknown beverage: %s' % beverage_name)

        if len(error_messages) > 0:
            for message in error_messages:
                flash(message)
        else:
            supply_item = {
                'slot': slot,
                'beverage': beverage['name'],
                'amount': amount
            }
            data.set_supply_item(supply_item)

        return redirect(url_for('maintenance'))

    data.view_name = 'Set slot data'

    slot = int(request.args.get('slot', -1))

    if  slot == -1:
        return redirect(url_for('show_recipes'))
    else:
        return render_template('set_slot.html', data=data, slot=str(slot))


@app.route('/maintenance/beverages/', methods=['GET'])
def ma_beverages():
    if not session.get('logged_in', False):
        return redirect(url_for('maintenance'))

    data = Data(server_config=server_config)
    return render_template('ma_beverages.html', data=data)

@app.route('/edit_beverage/', methods=['GET', 'POST'])
def edit_beverage():
    if not session.get('logged_in', False):
        return redirect(url_for('maintenance'))

    data = Data(server_config=server_config)

    if request.method == 'POST':
        name = request.form.get('name', '')
        viscosity = int(request.form.get('viscosity', -1))
        alcohol_vol = int(request.form.get('alcohol_vol', -1))

        error_messages = []

        if not name:
            error_messages.append('Name cannot be empty')
        
        if viscosity < 0:
            error_messages.append('Invalid value for viscosity')

        if alcohol_vol < 0:
            error_messages.append('Invalid value for Alcohol Vol. Percentage')

        if len(error_messages) > 0:
            for message in error_messages:
                flash(message)
        else:
            data.update_or_create_beverage({
                'name': name,
                'viscosity': viscosity,
                'alcohol_vol': alcohol_vol
            })


        return redirect(url_for('ma_beverages'))

        

    beverage_name = request.args.get('name', '')
    
    beverage = data.get_beverage(beverage_name)

    if not beverage_name or not beverage:
        flash('Unknown beverage: %s' % beverage_name)
        return redirect(url_for('ma_beverages'))
    else:
        return render_template('edit_beverage.html', data=data, beverage=beverage)

@app.route('/new_beverage/', methods=['GET', 'POST'])
def new_beverage():
    if not session.get('logged_in', False):
        return redirect(url_for('maintenance'))

    if request.method == 'POST':
        pass

    data = Data(server_config=server_config)

    return render_template('edit_beverage.html', data=data, beverage={})

def main():

    app.run(host=server_config['flask_host_name'],port=server_config['flask_port'])

if __name__ == '__main__':
    main()
