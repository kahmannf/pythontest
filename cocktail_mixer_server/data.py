class Data:

    application_name = ''

    recipes = []

    def __init__(self, server_config):
        self.application_name = server_config['app_name'] 
        self.recipes = load_recipes(server_config['recipes_dir'])


def load_recipes(dir):
        recipe_list = [{ 'name': 'Havana Cola' }, { 'name': 'Mai Tai' }]
        return recipe_list
