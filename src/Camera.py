'''

2012 Nicholas Hydock
TWIXIE
Typed-Word Invokable Xenomorphic Incident Engine

Licensed under the GNU General Public License V3
http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

DEFAULT_ZOOM = 100.0

#a "camera" object that allows you to pan around and focus in
# on view areas of a viewport that uses it
class Camera:
    def __init__(self, pos, zoom = 100):

        self.focusx = pos[0]	#x position to focus on
        self.focusy = pos[1]	#y position to focus on
        self.zoom = zoom		#zoom percentage
        
        #settings are stored for resetting values
        self._oldfocusx = self.focusx
        self._oldfocusy = self.focusy
        self._oldzoom = self.zoom
              
    #changes the focus settings of the camera to a new point with new zoom
    def focus(self, x, y, zoom):
		#store the current settings so they can be reset to later
        self._oldfocusx = self.focusx
        self._oldfocusy = self.focusy
        self._oldzoom = self.zoom
        
        #set the camera to new settings
        self.focusx = x
        self.focusy = y
        self.zoom = zoom

	#resets the focus to the last settings of the camera
    def resetFocus(self):
        self.focusx = self._oldfocusx
        self.focusy = self._oldfocusy
        self.zoom = self._oldzoom
