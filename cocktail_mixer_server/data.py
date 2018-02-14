import json, os, inspect

class Data:

    application_name = ''

    view_name = 'Cocktail Mixer!'

    recipes = []
    beverages = []
    supply = []

    server_config = None

    def __init__(self, server_config):
        self.server_config = server_config
        self.application_name = server_config['app_name'] 
        self.beverages = sorted(load_from_file(server_config['beverages_dir']), key= lambda bev : bev.get('name'))
        self.supply = sorted(load_from_file(server_config['supply_dir']), key= lambda sup : sup.get('slot'))
        self.recipes = sorted(load_from_file(server_config['recipes_dir']), key= lambda rec : rec.get('name'))
        
    def get_supply_item(self, name):
        for supply_item in self.supply:
            if supply_item['beverage'] == name:
                return supply_item
        return None

    def can_mix(self, recipe):
        totalML = int(self.server_config['glass_size'])
        
        total_parts = 0
        for ingredient in recipe['ingredients']:
            total_parts += int(ingredient['amount'])
        
        for ingredient in recipe['ingredients']:
            supply_item = self.get_supply_item(name=ingredient['beverage'])
            if supply_item:
                required_amount = float(totalML) * float(ingredient['amount']) / float(total_parts) 
                if required_amount > int(supply_item['amount']):
                    return False
            else:
                return False
        return True


    def filter_recipes(self):
        available_recipes = []
        for recipe in self.recipes:
            if self.can_mix(recipe=recipe):
                available_recipes.append(recipe)
        self.recipes = available_recipes

def get_file_names(directory):
    return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]

def load_from_file(dir):
    result_list = []
    
    server_dir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
    source_dir = os.path.join(server_dir, dir)
    
    if not os.path.isdir(source_dir):
        return result_list
    
    files = get_file_names(source_dir)

    for filename in files:
        full_filename = os.path.join(source_dir, filename)

        file_stream = open(full_filename, 'rU')

        dictionary = json.load(file_stream)

        result_list.append(dictionary)
    
    return result_list

def load_beverages(beverages_dir):
    beverage_list = []
    beverage_list.append({
        'name' : 'Gin'
    })
    beverage_list.append({
        'name' : 'Cola'
    })
    beverage_list.append({
        'name' : 'Tonic Water'
    })
    beverage_list.append({
        'name' : 'Havana'
    })

    return beverage_list

def load_supply(supply_dir):
    supply_list = []
    supply_list.append({
        'slot' : 2,
        'beverage' : 'Gin',
        'amount' : 1000
    })
    supply_list.append({
        'slot' : 3,
        'beverage' : 'Tonic Water',
        'amount' : 1000
    })
    supply_list.append({
        'slot' : 4,
        'beverage' : 'Cola',
        'amount' : 1000
    })
    return supply_list

