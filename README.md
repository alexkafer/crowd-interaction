# enttec-usb-dmx-pro
Communications and emulation modules for the Enttec Usb Dmx Pro

# Overview
The purpose of this software is the allow the crowd to interact with the light show using their mobile devices

The main file is `crowd_interaction.py`. Be nice to that file, it was born with a coding defect called Python. It has learned to live with itself, so we mustn't be disrespectful.


# Getting Started
`python -m crowd_interaction`

You may need to run the following commands if you get import errors:

`sudo pip install --upgrade pip enum34`
`sudo pip install pyserial`

Yeah thats about it. The software should be smart enough to debug itself upon any errors. 

## Goals
- Send Data to the Enttec USB DMX (code named Timmy)
- Provide a Web Socket server for the Web App
- Store current pixel data for the net lights

### The software is broken down into the following modules
1. [The Entec USB DMX Pro interface](https://github.com/teslaworksumn/enttec-usb-dmx-pro) (this repsoitory is forked from)
   * Takes data from the pixel manager and displays it on the netlights
2. A Pixel Manager 
   * Data storage
   * web socket exchange
   * HTTP GET interface
3. Game Server API
   * Just the server side
   * Currently active game
   * Interface avaliable for server side logic

## Notes
Currently, the web app and game interfaces (`/web/`) are stored on this repository's Github Pages space. See the README in `/web/` for details. 

This can be any other static website host (i.e. Amazon S3, GCP, the raspberry pi)