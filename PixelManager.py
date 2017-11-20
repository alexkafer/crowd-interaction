""" Pixel Manager with Data Storage, Websocket, and HTTP Get Interface """
from enum import Enum
from websocket_server import WebsocketServer
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import json

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

def receive_socket_update(client, server, message):
    """ Receives web socket update and updates the pixel manager """
    if len(message) > 200:
            message = message[:200]+'..'
    print("Client(%d) said: %s" % (client['id'], message))

class PixelManager(HTTPServer):
    """ Pixel Manager with Data Storage, Websocket, and HTTP Get Interface """
    def __init__(self, websocket_port = 8080, webserver_port = 8000):
        """ Initializes the pixels to the correct size and pre-sets everything to OFF """
        self.pixels = [[Color.OFF for x in range(NET_LIGHT_WIDTH)] for y in range(NET_LIGHT_HEIGHT)] 
        self.dmx = None
        self.server = WebsocketServer(websocket_port)
        self.server.set_fn_new_client(new_client)
        self.server.set_fn_client_left(client_left)
        self.server.set_fn_message_received(receive_socket_update)

        server_address = ('', webserver_port)
        HTTPServer.__init__(self, server_address, PixelServer)

    def start_websocket(self):
        """ Starts the web socket """
        print 'Starting web socket...'
        self.websocket_thread = threading.Thread(target=self.server.run_forever)
        self.websocket_thread.daemon = True
        self.websocket_thread.start()


    def set_color(self, row, column, color):
        """ Sets an individual pixel to a given color """
        self.pixels[row][column] = color
        print("Setting color to " + str(color))
        if self.dmx is not None:
            self.dmx.sendDMX(self.convert_to_dmx_array())

    def get_pixels(self):
        """ Sets an individual pixel to a given color """
        return self.pixels

    def convert_to_dmx_array(self):
        """ Converts the matrix to a single 1D array. """
        return sum(self.pixels, [])

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