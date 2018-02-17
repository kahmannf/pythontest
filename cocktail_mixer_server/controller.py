import smbus
import time
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
        ##test comment
        pass

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
            

    



