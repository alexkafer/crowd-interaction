""" Pixel Manager with Data Storage, Websocket, and HTTP Get Interface """
from enum import Enum
from websocket_server import WebsocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json
import unicodedata
import ConfigParser

import threading

NET_LIGHT_WIDTH = 12 # Number of columns
NET_LIGHT_HEIGHT = 5 # Number of rows

class Color(Enum):
    """ Three options of the Net Lights. Off, Red, and Green """
    OFF = 0
    RED = 1
    GREEN = 2

class ColorEncoder(json.JSONEncoder):
    def default(self, obj):
         if isinstance(obj, Color):
             return obj.value
         # Let the base class default method raise the TypeError
         return json.JSONEncoder.default(self, obj)

def new_client(client, server):
    """ Called for every client connecting (after handshake) """
    print("New client connected and was given id %d" % client['id'])
    server.send_message_to_all("Hey all, a new client has joined us")

# Called for every client disconnecting
def client_left(client, server):
    """ Called for every client disconnecting """
    print("Client(%d) disconnected" % client['id'])
    
class PixelManager(HTTPServer):
    """ Pixel Manager with Data Storage, Websocket, and HTTP Get Interface """
    def __init__(self, websocket_port = 8080, webserver_port = 8000):
        """ Initializes the pixels to the correct size and pre-sets everything to OFF """
        self.pixels = [[Color.OFF for x in range(NET_LIGHT_WIDTH)] for y in range(NET_LIGHT_HEIGHT)] 
        self.dmx = None

        config = ConfigParser.RawConfigParser() 
        config.read('DMX.cfg')

        self.dmxmap = []

        for row in range(5):
            for col in range(12):
                 self.dmxmap.append([config.getint('RED', str(col) + ',' + str(row)), config.getint('GREEN', str(col) + ',' + str(row))])
                
        print "Config: ", self.dmxmap
        self.ws = WebsocketServer(websocket_port, "0.0.0.0")
        self.ws.set_fn_new_client(new_client)
        self.ws.set_fn_client_left(client_left)
        self.ws.set_fn_message_received(self.receive_update)

        server_address = ('', webserver_port)
        HTTPServer.__init__(self, server_address, PixelServer)

    def start_websocket(self):
        """ Starts the web socket """
        print 'Starting web socket...'
        self.websocket_thread = threading.Thread(target=self.ws.run_forever)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()

    def receive_update(self, client, server, message):
        """ Receives web socket update and updates the pixel manager """
        print("Client(%d) said: %s" % (client['id'], message))
        update = json.loads(message)
        row = int(update['row'])
        col = int(update['col'])
        color = Color(int(update['color']))
        self.set_color(row, col, color)

    def set_color(self, row, column, color):
        """ Sets an individual pixel to a given color """
        self.pixels[row][column] = color
        print("Setting color to " + str(color))
        if self.dmx is not None:
            self.dmx.sendDMX(self.convert_to_dmx_array())

        if self.ws:
            payload = {
                'row': row,
                'col': column,
                'color': color.value
            }

            self.ws.send_message_to_all(json.dumps(payload))

    def get_pixels(self):
        """ Sets an individual pixel to a given color """
        return self.pixels

    def convert_to_dmx_array(self):
        """ Converts the matrix to a single 1D array. """
        output = [0] * 512
        flattened = (self.pixels[4] + self.pixels[3] + self.pixels[2] + self.pixels[1] + self.pixels[0])
        index = 0
        for pixel in flattened:
            print index, pixel, self.dmxmap[index]
            if pixel == Color.RED:
                output[self.dmxmap[index][0]-1] = 255
            elif pixel == Color.GREEN:
                output[self.dmxmap[index][1]-1] = 255
            else:
                output[self.dmxmap[index][0]-1] = 0
                output[self.dmxmap[index][1]-1] = 0

            index += 1
            
        return output

    def link_dmx(self, dmx):
        """ Links the DMX instance to the Pixel Manager  """
        self.dmx = dmx

    def start_webserver(self):
        """ Starts the web server """
        print 'Starting httpd...'
        self.websocket_thread = threading.Thread(target=self.serve_forever)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()
        #Test the DMX connection

class PixelServer(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write(json.dumps(self.server.get_pixels(), cls=ColorEncoder))

    def do_HEAD(self):
        self._set_headers()