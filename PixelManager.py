""" Pixel Manager with Data Storage, Websocket, and HTTP Get Interface """
from enum import Enum

NET_LIGHT_WIDTH = 12 # Number of columns
NET_LIGHT_HEIGHT = 5 # Number of rows


class Color(Enum):
    """ Three options of the Net Lights. Off, Red, and Green """
    OFF = 0
    RED = 1
    GREEN = 2


class PixelManager(object):
    """ Pixel Manager with Data Storage, Websocket, and HTTP Get Interface """
    def __init__(self):
        """ Initializes the pixels to the correct size and pre-sets everything to OFF """
        self.pixels = [[Color.OFF for x in range(NET_LIGHT_WIDTH)] for y in range(NET_LIGHT_HEIGHT)] 
        self.DMX = None

    def set_color(self, row, column, color):
        """ Sets an individual pixel to a given color """
        self.pixels[row][column] = color
        if self.DMX is not None:
            self.DMX.sendDMX(self.convert_to_dmx_array())

    def get_pixels(self):
        """ Sets an individual pixel to a given color """
        return self.pixels

    def convert_to_dmx_array(self):
        """ Converts the matrix to a single 1D array. """
        return sum(self.pixels, [])

    def link_dmx(self, dmx):
        """ Links the DMX instance to the Pixel Manager  """
        self.DMX = dmx

        #Test the DMX connection