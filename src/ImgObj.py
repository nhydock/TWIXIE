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

LEFT   = 0
CENTER = 1
RIGHT  = 2

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
        self.rect        = (0.0,0.0,self.frameSize[0],self.frameSize[1])
                                                    #left, top, right, bottom, crops the texture
        self.alignment  = CENTER                   #alignment of the vertices for placement
        self.pixelSize   = (self.texture.pixelSize[0]/frameX,
                            self.texture.pixelSize[1]/frameY)   
                                                    #the actual size of the image in pixels
                                                    
        self.width, self.height = self.pixelSize    #the width and height after transformations
                                                    # are taken into account

        self.createArrays()
                       
        #for animation purposes
        self.frames = [frameX, frameY]      #number of frames (x axis, y axis)
        self.currentFrame = [0, 0]          #current frame
                                            #will reverse the animation when looping
        self.reverseH = False               #   reverse along frameX
        self.reverseV = False               #   reverse along frameY
        
        self.transformed = False            #did the image's attributes change
    
        #OPENGL DISPLAY LIST
        self.listBase = None
        
    #sets up the vertex and texture array coordinates
    def createArrays(self):
        # numpy zeros is used because it can generate an array that can
        # be used for assigning coordinates to quite quickly
        self.vtxArray = [0.0]*8
        self.texArray = [0.0]*8

        self.createVerts()
        self.createTex()

    #set up vertex coordinates
    def createVerts(self):
        vtxArray = self.vtxArray

        #vertices
        #top left, top right, bottom right, bottom left
        vtxArray[0] = 0; vtxArray[1] = 0
        vtxArray[2] = self.pixelSize[0]; vtxArray[3] = 0
        vtxArray[4] = self.pixelSize[0]; vtxArray[5] = self.pixelSize[1]
        vtxArray[6] = 0; vtxArray[7] = self.pixelSize[1]

    #set up texture coordinates
    def createTex(self):
        rect = self.rect    #not really necessary, it just saves on some typing
                            #because I got sick of typing "self." all the time
       
        texArray = self.texArray

        #top left, top right, bottom right, bottom left

        #texture coordinates
        texArray[0] = rect[0]; texArray[1] = rect[1]
        texArray[2] = rect[2]; texArray[3] = rect[1]
        texArray[4] = rect[2]; texArray[5] = rect[3]
        texArray[6] = rect[0]; texArray[7] = rect[3]

    #sets up a display list to make rendering more optimized
    def createDisplayList(self):
        #create the base location of the list
        self.listBase = glGenLists(1)
		
        #start creating the new list
        glNewList(self.listBase+1, GL_COMPILE)
			
        glPushMatrix()
        
        #performs GL operations to render the plane
        glEnableClientState(GL_TEXTURE_COORD_ARRAY)
        glEnableClientState(GL_VERTEX_ARRAY)
        glVertexPointer(2, GL_FLOAT, 0, self.vtxArray)
        glTexCoordPointer(2, GL_FLOAT, 0, self.texArray)
        glDrawArrays(GL_QUADS, 0, 8)
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
        self.setRect((float(int(x)-1)*self.frameSize[0], float(int(y)-1)*self.frameSize[1], 
                      float(int(x))*self.frameSize[0], float(int(y))*self.frameSize[1]))

    #crops the texture
    def setRect(self, rect):
        self.rect = rect
        self.createTex()
        self.createDisplayList()
        
    #sets where the image is anchored (left, center, or right)
    def setAlignment(self, alignment):
        if type(alignment) is str:
            alignment = alignment.upper()
            self.alignment = eval(alignment)
        elif alignment.isNumeric():
            self.alignment = alignment
        
    #finally draws the image to the screen
    def draw(self):
    
        #create a display list if one hasn't been made yet
        if self.listBase == None:
            self.createDisplayList()

        glPushMatrix()

        x = self.position[0]
        if self.alignment == 0:
            x += float(self.pixelSize[0])/2.0
        elif self.alignment == 2:
            x -= float(self.pixelSize[0])/2.0
        glTranslatef(x, self.position[1], -.1)
            
        glScalef(self.scale[0], self.scale[1], 1.0)
        glRotatef(-self.angle, 0, 0, 1)
        glColor4f(*self.color)

        self.texture.bind()

        glCallList(self.listBase+1)
        
        glPopMatrix()
