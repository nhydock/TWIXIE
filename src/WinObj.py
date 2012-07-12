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

#a window created to be used as a background for images
class WinObj:
    def __init__(self, texture, (width,height)=(64, 64)):
        
        self.texture = texture
        self.texture.changeTexture(texture.textureSurface, False)
        
        #attributes
        #over rides the width and height of the rect
        self.width = width
        self.height = height
        #overrides the rect position
        self.left = 0
        self.top = 0
        
        self.color = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.pixelSize   = self.texture.pixelSize   #the actual size of the image in pixels

        self.__createArrays__()

    #sets up the vertex and texture array coordinates
    def __createArrays__(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = [[0.0]*3]*16
        self.texArray = [[0.0]*2]*16
        print self.vtxArray
        
        #  0  1  2  3
        #  4  5  6  7
        #  8  9 10 11
        # 12 13 14 15
        self.indexArray = [0,   1,  5,  4,
                           1,   2,  6,  5,
                           2,   3,  7,  6,
                           4,   5,  9,  8,
                           5,   6, 10,  9,
                           6,   7, 11, 10,
                           8,   9, 13, 12,
                           9,  10, 14, 13,
                           10, 11, 15, 14]

        self.__createVerts__()
        self.__createTex__()

    #set up vertex coordinates
    def __createVerts__(self):
        vtxArray = self.vtxArray

        #top left, top right, bottom right, bottom left

        #vertices
        border = 32
        
        xcoord = [0, border, self.width - border, self.width]
        ycoord = [0, border, self.height - border, self.height]
        index = 0
        for i in range(4):
            for n in range(4):
                vtxArray[index][0] = xcoord[n]
                vtxArray[index][1] = ycoord[i]
                index += 1

    #set up texture coordinates
    def __createTex__(self):
        texArray = self.texArray

        #top left, top right, bottom right, bottom left

        #texture coordinates
        thirdPS  = (float(self.pixelSize[0])/3.0, float(self.pixelSize[1])/3.0)
        coord = [0, 1.0/3.0, 2.0/3.0, 1.0]
        index = 0
        
        for i in range(4):
            for n in range(4):
                texArray[index][0] = coord[n]
                texArray[index][1] = coord[i]
                index += 1

    #changes the position of the image to x, y
    #over rides Rect's moving
    #position of the rect is based on top-left corner
    #instead of returning a new rect, it just replaces the information about this one
    def move(self, x, y):
		self.left = x
		self.top = y
        
    #changes the size of the image and scales the surface
    def setDimensions(self, width, height):
		#if the dimensions are the same then skip regenerating the verts
        if self.width == width and self.height == height:
            return
        
        self.width = width
        self.height = height

		#reupdates the verts
        self.__createVerts__()
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(color)):
            self.color[i] = color[i]

    #finally draws the image to the screen
    def draw(self):
        glPushMatrix()

        glTranslatef(self.left, self.top,-.1)
        glColor4f(*self.color)
        self.texture.bind()

        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointerf(self.vtxArray)
        glTexCoordPointerf(self.texArray)
        glDrawElements(GL_QUADS, len(self.indexArray), GL_UNSIGNED_BYTE, self.indexArray)
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()
