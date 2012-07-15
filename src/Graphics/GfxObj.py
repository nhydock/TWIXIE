
#this is a global importer for the graphics components of the game
#by importing using from GfxObj import * at the top of a .py file
# you'll have access to all these rendering objects

import os
import sys

from Graphics.Camera import Camera
from Graphics.ImgObj import ImgObj
from Graphics.WinObj import WinObj
from Graphics.Texture import loadTexture as Texture
from Graphics.FontObj import FontObj
from Graphics.DialogBox import DialogBox
