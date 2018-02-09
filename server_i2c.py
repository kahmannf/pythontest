import smbus
import time
from flask import Flask
from flask import request

app = Flask(__name__)

# for RPI version 1, use "bus = smbus.SMBus(0)"
bus = smbus.SMBus(1)

# This is the address we setup in the Arduino Program
address = 0x04

def writeNumber(value):
    bus.write_byte(address, value)
    # bus.write_byte_data(address, 0, value)
    return -1

#expects query-parameter 'port' and 'state'
@app.route('/set-state/')
def setState():

    port = int(request.args.get('port', ''))
    state = int(request.args.get('state', ''))

    if port < 2 or port > 13:
        return "Invalid Port: ", port

    if state != 0 and state != 1:
        return "Invalid state: ", state

    writeNumber(port)
    writeNumber(state)

    result = "Switched port ", port

    if state == 1:
        result = result, " on"
    else:
        result = result, " off"

    return result

app.run(host="0.0.0.0", port=5001)

