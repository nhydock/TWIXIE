
#this is a global importer for the game
#by importing using from sysobj import * at the top of a .py file
# you'll have access to all these rendering objects

import os
import sys

w, h = 0, 0                     #width and height of the window

from Camera import Camera
from ImgObj import ImgObj
from WinObj import WinObj
from Texture import loadTexture as Texture
from FontObj import FontObj
from Audio import *
