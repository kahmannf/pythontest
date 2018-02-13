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
        self.beverages = load_beverages(server_config['beverages_dir'])
        self.supply = load_supply(server_config['supply_dir'])
        self.recipes = load_recipes(server_config['recipes_dir'])
        
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
            supply_item = self.get_supply_item(ingredient['name'])
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

def load_recipes(dir):
        recipe_list = []
        recipe_list.append({
            'name' : 'Havana Cola',
            'ingredients' : [{
                    'name' : 'Havana',
                    'amount' : 1
                }, {
                    'name' : 'Cola',
                    'amount' : 4
                }

            ]
        })
        recipe_list.append({
            'name' : 'Gin Tonic',
            'ingredients' : [{
                    'name' : 'Gin',
                    'amount' : 1
                }, {
                    'name' : 'Tonic Water',
                    'amount' : 4
                }
            ]
        })

        return recipe_list

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
