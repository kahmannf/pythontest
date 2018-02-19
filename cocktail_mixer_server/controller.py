import smbus
import time
from data import Data
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    
    return -1

def open_port(port):
    writeNumber(port + 2)
    writeNumber(1)

def close_port(port):
    writeNumber(port + 2)
    writeNumber(0)

class Controller:
    ## 0 = mixing
    ## 1 = available
    status = 1

    def start_mixing(self, data : Data, recipe, server_config):
        air_flow = data.get_supply_item('Air flow')
        waste_gate = data.get_supply_item('Waste gate')

        if not air_flow or not waste_gate:
            return False, 'not air flow or waste gte configured'
        
        if not data.can_mix(recipe):
            return False, 'insufficient supplies'
        
        self.mix(data, recipe, air_flow, waste_gate, server_config)
        return True, ''

    def mix(self, data : Data, recipe, air_flow, waste_gate, server_config):
        if not self.status == 1:
            return
        else:
            self.status = 0
        
        try:
            ingredients = recipe.ingredients[:]
            
            total_parts = 0

            for ingredient in ingredients:
                total_parts += ingredient['amount']
            
            for ingredient in ingredients:
                amount_in_ml = float( server_config['glass_size']) * float(ingredient['amount']) / float(total_parts)

                supply_item = data.get_supply_item(ingredient['beverage'])
                beverage = data.get_beverage(ingredient['beverage'])

                open_port(air_flow['slot'])

                air_ml = float(1000 - supply_item['amount'])

                open_port(supply_item['slot'])

                ##build up some preasure depending on how full the bottle is
                if air_ml > 0:
                    time.sleep(air_ml * 2 / 1000)

                ##this calculation was aquired bytesting. it is totally not accurate at all but the best i was able to come up with
                remaining_time = (beverage['viscosity'] (amount_in_ml - ((19/100) * air_ml) * 2)) / 10
                time.sleep(remaining_time)

                close_port(air_flow['slot'])
                open_port(waste_gate['slot'])

                air_reduce_time = 3 + ((air_ml + amount_in_ml) * 0.006)

                time.sleep(air_reduce_time)

                close_port(supply_item['slot'])
                close_port(air_flow['slot'])

                data.remove_amount(supply_item['beverage'], amount_in_ml)
            
        except Exception as error:
            self.status = 0
            return str(error)
            

    



