import smbus
import time
import asyncio
# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    
    return -1

class Controller:
    ## 0 = mixing
    ## 1 = available
    status = 1

    def start_mixing(self, data, recipe):
        loop = asyncio.get_event_loop()
        
        tasks = [asyncio.ensure_future(self.mix(data, recipe))]

        loop.run_until_complete(asyncio.wait(tasks))
        loop.close()

    @asyncio.coroutine
    def mix(self, data, recipe):
        if not self.status == 1:
            return
        else:
            self.status = 0
        
        try:
            time.sleep(5)
            
        except OSError as error:
            self.status = 0
            return str(error)
            

    



