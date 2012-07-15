'''

2012 Nicholas Hydock
TWIXIE
Typed-Word Invokable Xenomorphic Incident Engine

Licensed under the GNU General Public License V3
http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

from math import *

from ImgObj import ImgObj

#a window created to be used as a background for images
class WinObj(ImgObj):
    def __init__(self, texture, width = 64, height = 64):
        super(WinObj, self).__init__(texture, 3, 3)
        self.height = height
        self.width = width
        
    def __createArrays__(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = [0.0]*8
        self.texArray = [0.0]*8

        #verts are same for all
        self.__createVerts__()
           
        #create the base location of the list
        #there's an additional slot added to hold the entire frame assembled
        self.listBase = glGenLists((self.frames[0]*self.frames[1]))
        
        #texture coordinates vary on frame, and as a result so do the display lists
        for y in xrange(self.frames[1]):
            for x in xrange(self.frames[0]):
                self.__createTex__(x, y)
                self.__createDisplayList__(x+(y*self.frames[0])+1)
            
        glNewList(self.listBase, GL_COMPILE)
        
        #draw corners
        glPushMatrix()
        #Top left corner
        glCallList(self.listBase+1)
        #Bottom left corner
        glTranslatef(0, self.pixelSize[1]-self.height, 0)
        glCallList(self.listBase+7)
        #Bottom right corner
        glTranslatef(self.width-self.pixelSize[0], 0, 0)
        glCallList(self.listBase+9)
        #Top right corner
        glTranslatef(0, self.height-self.pixelSize[1], 0)
        glCallList(self.listBase+3)
        glPopMatrix()
        
        #draw edges
        
        glPushMatrix()
        #Top
        glTranslatef(self.pixelSize[0], 0, 0)
        glScalef((self.width-(self.pixelSize[0]*2))/self.pixelSize[0], 1, 1)
        glCallList(self.listBase+2)
        #Bottom
        glTranslatef(0, -self.height+self.pixelSize[1], 0)
        glCallList(self.listBase+8)
        glPopMatrix()
        
        glPushMatrix()
        #Left Side
        glTranslatef(0, -self.pixelSize[1], 0)
        glScalef(1, (self.height - self.pixelSize[1]*2)/self.pixelSize[1], 1)
        glCallList(self.listBase+4)
        #Right Side
        glTranslatef(self.width-self.pixelSize[0], 0, 0)
        glCallList(self.listBase+6)
        glPopMatrix()
        
        #draw center
        glPushMatrix()
        glTranslate(self.pixelSize[0], -self.pixelSize[1], 0)
        glScale((self.width-(self.pixelSize[0]*2))/self.pixelSize[0], (self.height - self.pixelSize[1]*2)/self.pixelSize[1], 1)
        glCallList(self.listBase+5)
        glPopMatrix()
        
        glEndList()
            
    #changes the size of the image and scales the surface
    def setDimensions(self, width, height):
        #if the dimensions are the same then skip regenerating the verts
        if self.width == width and self.height == height:
            return
        
        self.width = width
        self.height = height
        
    def getWidth(self):
        return self.width
        
    def getHeight(self):
        return self.height
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(color)):
            self.color[i] = color[i]

