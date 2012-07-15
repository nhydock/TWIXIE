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

from Texture import loadTexture

import pygame

LEFT   = TOP = 0
CENTER = 1
RIGHT  = BOTTOM = 2


#an Image Object for rendering and collision detection (mouse)
class ImgObj(object):
    
    def __init__(self, texture, frameX = 1, frameY = 1):
        #ability to set/load a texture if the passed in value is not a Texture object
        if isinstance(texture, str):
            self.texture = loadTexture(path = texture)
        elif isinstance(texture, pygame.Surface):
            self.texture = loadTexture(surface = texture)
        else:
            self.texture = texture
       
        #attributes
        self.scale       = (1.0, 1.0)               #image bounds (width, height)
        self.position    = (0,0)                    #where in the window it should render
        self.angle       = 0                        #angle which the image is drawn
        self.color       = [1.0,1.0,1.0,1.0]        #colour of the image RGBA (0 - 1.0)
        
        self.frameSize   = (1.0/float(frameX),1.0/float(frameY))
                                                    #the size of each cell when divided into frames
        self.alignment   = LEFT                     #alignment of the vertices horizontally for placement
        self.valignment  = TOP                      #alignment of the vertices vertically for placement
        self.pixelSize   = (self.texture.pixelSize[0]/frameX,
                            self.texture.pixelSize[1]/frameY)   
                                                    #the actual size of the image in pixels
                                                    
        self.width, self.height = self.pixelSize    #the width and height after transformations
                                                    # are taken into account
                
        #for animation purposes
        self.frames = [frameX, frameY]      #number of frames (x axis, y axis)
        self.currentFrame = [1, 1]          #current frame
                                            #will reverse the animation when looping
        self.reverseH = False               #   reverse along frameX
        self.reverseV = False               #   reverse along frameY
        
        self.transformed = False            #did the image's attributes change
    
        #OPENGL DISPLAY LIST
        self.listBase = None
        
    #sets up the vertex and texture array coordinates
    def __createArrays__(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = [0.0]*8
        self.texArray = [0.0]*8

        #verts are same for all
        self.__createVerts__()
           
        #create the base location of the list
        self.listBase = glGenLists(self.frames[0]*self.frames[1])
		
        #texture coordinates vary on frame, and as a result so do the display lists
        for y in xrange(self.frames[1]):
            for x in xrange(self.frames[0]):
                self.__createTex__(x, y)
                self.__createDisplayList__(x+(y*self.frames[0]))

    #set up vertex coordinates
    def __createVerts__(self):
        vtxArray = self.vtxArray

        #vertices
        #top left
        vtxArray[0] = 0
        vtxArray[1] = 0
        #top right
        vtxArray[2] = self.pixelSize[0]
        vtxArray[3] = vtxArray[1]
        #bottom right
        vtxArray[4] = vtxArray[2]
        vtxArray[5] = -self.pixelSize[1]
        #bottom left
        vtxArray[6] = vtxArray[0]
        vtxArray[7] = vtxArray[5]

    #set up texture coordinates
    def __createTex__(self, x, y):
        texArray = self.texArray
        
        #texture coordinates

        #top left
        texArray[0] = self.frameSize[0]*x
        texArray[1] = self.frameSize[1]*y
        #top right
        texArray[2] = texArray[0]+self.frameSize[0]
        texArray[3] = texArray[1]
        #bottom right
        texArray[4] = texArray[2]
        texArray[5] = texArray[1]+self.frameSize[1]
        #bottom left
        texArray[6] = texArray[0]
        texArray[7] = texArray[5]

    #sets up a display list to make rendering more optimized
    def __createDisplayList__(self, i):
        
        #start creating the new list
        glNewList(self.listBase+i, GL_COMPILE)
			
        glPushMatrix()
        
        #performs GL operations to render the plane
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.vtxArray)
        glTexCoordPointer(2, GL_FLOAT, 0, self.texArray)
        glDrawArrays(GL_QUADS, 0, len(self.vtxArray))
        glDisableClientState(GL_VERTEX_ARRAY)
        glDisableClientState(GL_TEXTURE_COORD_ARRAY)

        glPopMatrix()

        #end generating the list
        glEndList()
        
    #changes the position of the image to x, y
    def setPosition(self, x, y):
        if not self.position == (x, y):
            self.position = (x, y)
            self.transformed = True
            
    def getX(self):
        return self.position[0]
        
    def getY(self):
        return self.position[1]
        
    def getPosition(self):
        return self.position
                    
    #changes the size of the image and scales the surface
    def setScale(self, width = 1.0, height = 1.0, inPixels = False):
        if not inPixels:
            if not self.scale == (width, height):
                self.scale = (width,height)
                self.transformed = True
                self.width = self.scale[0] * self.pixelSize[0]
                self.height = self.scale[1] * self.pixelSize[1]
        else:
            if not self.scale == (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1])):
                self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))
                self.transformed = True
                self.width = width
                self.height = height

    #scales the image size by only the width
    # if keep_aspect_ratio is true it will scale the height
    # as well in order to maintain the aspect ratio
    def scaleWidth(self, width, keep_aspect_ratio = True):
        height = self.scale[1]
        if keep_aspect_ratio:
            height = self.scale[1] * (width/self.pixelSize[0])
        if not self.scale == (width/self.pixelSize[0], height):
            self.scale = (width/self.pixelSize[0], height)
            self.transformed = True
            self.width = width*self.pixelSize[0]
            
    #same as scaleWidth except that the value passed
    #is the height of the image instead of the width
    def scaleHeight(self, height, keep_aspect_ratio = True):
        width = self.scale[0]
        if keep_aspect_ratio:
            width = self.scale[0] * (height/self.pixelSize[1])
        if not self.scale == (width, height/self.pixelSize[1]):
            self.scale = (width, height/self.pixelSize[1])
            self.transformed = True
            self.height = height
            
    #rotates the image to the angle
    def setAngle(self, angle):
        if not self.angle == angle:
            self.angle = angle
            self.transformed = True

    #rotates the image
    def rotate(self, angle):
        if not self.angle == (self.angle + angle):
            self.angle += angle
            self.transformed = True
        
    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        for i in range(len(self.color)):
            self.color[i] = float(color[i])

    #changes the frame number of the image
    def setFrame(self, x = 1, y = 1):
        self.currentFrame = [x, y]

    #sets where the image is anchored (left, center, or right)
    def setAlignment(self, alignment):
        if type(alignment) is str:
            alignment = alignment.upper()
            self.alignment = eval(alignment)
        elif alignment.isNumeric():
            self.alignment = alignment
        
    #sets where the image is anchored along its y axis
    def setVAlignment(self, alignment):
        if type(alignment) is str:
            alignment = alignment.upper()
            self.valignment = eval(alignment)
        elif alignment.isNumeric():
            self.valignment = alignment
            
    #finally draws the image to the screen
    def draw(self):
    
        #create a display list if one hasn't been made yet
        if self.listBase == None:
            self.__createArrays__()
            
        glPushMatrix()

        #fix the x position based on alignment
        x = self.position[0]
        if self.alignment == 0:
            x += float(self.pixelSize[0])/2.0
        elif self.alignment == 2:
            x -= float(self.pixelSize[0])/2.0
            
        #fix the y position based on vertical alignment
        y = self.position[1]
        if self.valignment == 0:
            y += float(self.pixelSize[1])/2.0
        elif self.alignment == 2:
            y -= float(self.pixelSize[1])/2.0
            
        glTranslatef(x, y, -.1)
            
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(-self.angle, 0, 0, 1)
        glColor4f(*self.color)

        self.texture.bind()

        glCallList(self.listBase+int((self.currentFrame[0]-1)+((self.currentFrame[1]-1)*self.frames[0])))
        
        glPopMatrix()
