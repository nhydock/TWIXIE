'''

2012 Nicholas Hydock
TWIXIE
Typed-Word Invokable Xenomorphic Incident Engine

Licensed under the GNU General Public License V3
http://www.gnu.org/licenses/gpl.html

'''

import os
import sys

import pygame, pygame.image
from pygame.locals import *

from OpenGL.GL import *
from OpenGL.GLU import *

from Texture import Texture #create Textures specifically instead of loadTexture because surfaces can't be cached

import string

#global alignment variables
LEFT   = 0
CENTER = 1
RIGHT  = 2

#set up the generic texture array
TEX_ARRAY = [0.0]*8
print TEX_ARRAY

#top left, top right, bottom right, bottom left
#texture coordinates
TEX_ARRAY[0] = 0; TEX_ARRAY[1] = 0
TEX_ARRAY[2] = 1; TEX_ARRAY[3] = 0
TEX_ARRAY[4] = 1; TEX_ARRAY[5] = 1
TEX_ARRAY[6] = 0; TEX_ARRAY[7] = 1

#Set a desired amount of characters that should be cached
CHAR_CACHE_SIZE = 128

#FontObj are of the UlDunAd Rendering family with Texture, ImgObj, and WindowObj
# it extends directly from pygame for a familiar API but handles all rendering
# using basic OpenGL practices.  Important methods such as render have been
# overridden to perform OpenGL calls, and upon initialization a glyph dictionary
# is generated for use in rendering.  Surfaces and other objects are not generated
# from FontObj to use, instead rendering is direct and immediate to the OpenGL buffer
# using the glyphs stored.
class FontObj(pygame.font.Font):
    def __init__(self, path, size = 32):
        super(FontObj, self).__init__(os.path.join("..", "data", "fonts", path), size)
        
        #generates all the glyphs for use
        self.generateGlyphs()

        #attributes
        self.scale     = 1.0            	 #scaling percentage based on font height
        self.position  = (0,0)               #where in the window it should render
        self.angle     = 0                   #angle which the font is drawn
        self.color     = (255,255,255,255)   #colour of the font
        self.alignment = 1                   #alignment of the text (left, center , right)
        self.shadow = True                   #does the font project a shadow

    #gets the natural width of the string in pixels
    #this means that scale is not taken into factor when determining width
    def stringWidth(self, string):
        s = 0
        for i in list(string):
            s += self.glyphTex[ord(i)].pixelSize[0]
        return s
        
    #generates a dictionary of glyphs for use
    def generateGlyphs(self):
        #we set the list to be the size of how many glyphs will be cached
        self.listBase = glGenLists(CHAR_CACHE_SIZE)
        self.glyphTex = [None] * CHAR_CACHE_SIZE
        
        for i in xrange(CHAR_CACHE_SIZE):
            #each glyph consists of a texture and a vert array for its shape
            try:
                self.glyphTex[i] = Texture(surface = super(FontObj, self).render(""+chr(i), True, (255,255,255)))
            except Exception:
                self.glyphTex[i] = Texture(surface = super(FontObj, self).render(" ", True, (255,255,255)))

            #add the glyph to a display list
            glNewList(self.listBase+i, GL_COMPILE)
            
            #push a matrix for each char
            glPushMatrix()

            #generate the vertex array
            vtxArray = [0.0]*8
            pixelSize = self.glyphTex[i].pixelSize
            halfPS = (float(pixelSize[0])/2.0, float(pixelSize[1])/2.0)

            vtxArray[0] = 0;            vtxArray[1] =  halfPS[1]
            vtxArray[2] = pixelSize[0]; vtxArray[3] =  halfPS[1]
            vtxArray[4] = pixelSize[0]; vtxArray[5] = -halfPS[1]
            vtxArray[6] = 0;            vtxArray[7] = -halfPS[1]
            
            #bind and render the glyph
            self.glyphTex[i].bind()

            glEnableClientState(GL_TEXTURE_COORD_ARRAY)
            glEnableClientState(GL_VERTEX_ARRAY)
            glVertexPointer(2, GL_FLOAT, 0, vtxArray)
            glTexCoordPointer(2, GL_FLOAT, 0, TEX_ARRAY)
            glDrawArrays(GL_QUADS, 0, 8)
            glDisableClientState(GL_VERTEX_ARRAY)
            glDisableClientState(GL_TEXTURE_COORD_ARRAY)

            glPopMatrix()
                        
            #shift the character over a little extra so the next won't overlap with other letters
            glTranslatef(self.glyphTex[i].pixelSize[0] + 2, 0, 0)

            glEndList()

    #sets the alignment of how the text should be rendered
    def setAlignment(self, alignment):
        self.alignment = alignment

    #changes the position of the image to x, y
    def setPosition(self, x, y):
        self.position = (x, y)

    #moves the image from its current position by x and y
    def slide(self, x = 0, y = 0):
        self.position = (self.position[0] + x, self.position[1] + y)

    #changes the size of the image and scales the surface
    def setSize(self, size):
        self.scale = size/float(self.getsize())
        
    #rotates the image to the angle
    def setAngle(self, angle):
        self.angle = angle

    #rotates the image
    def rotate(self, angle):
        self.angle += angle

    #sets the colour of the image (RGBA 0.0 -> 1.0)
    def setColor(self, color):
        self.color = list(self.color)
        for i in range(len(color)):
            self.color[i] = color[i]

	#fades from the current color to the new color in the set amount of time
	# remember that the color must be in RGBA format
    def fade(self, color, milliseconds):
        color = [float(c) for c in color]   #makes sure the color is an array of floats
        if list(self.color) != color:
            self.color = [self.color[i] + (color[i] - self.color[i])/milliseconds for i in range(len(self.color))]
            return True
        return False

	#finally draws the image to the screen
    def render(self, text):
		#submethod for rendering the text in its proper settings
		#this is used so then shadows and other text effects that require rendering multiple times can
		# just be easily called
        def draw(text, position = self.position, scale = self.scale, angle = self.angle, color = self.color):

            #push a matrix for the whole set of words
            glPushAttrib(GL_LIST_BIT | GL_CURRENT_BIT  | GL_ENABLE_BIT | GL_TRANSFORM_BIT)
            glPushMatrix()
            
            #set the position based on alignment
            x = position[0]
            if self.alignment == 0:
                x += self.font.size(text)[0]/2.0
            elif self.alignment == 2:
                x -= self.font.size(text)[0]/2.0

            glTranslatef(x, position[1],-.1)	#first we move the font into the proper position
            glScalef(scale, scale, 1.0)			#then we scale it up/down
            glRotatef(angle, 0, 0, 1)			#then we rotate it
            glColor4f(*color)					#and finally we apply the colour

            height = self.get_linesize()	    #amount of space to reserve for each line

            #we identify the list base so opengl knows the data we're looking at for glyphs
            glListBase(self.listBase)
            
            #first we split the text into lines if it's not already
            if type(text) is str:
                text = text.split('\n')
                
            #print the lines of text
            for line in text:
                #because things are rendered in a proper cartesian coordinate
                # system, we subtract the height to have text going down the screen
                glTranslate(0, -height, 0)	#shift the line down
                
                #push a matrix for each line
                glPushMatrix()
            
                #then we take the line and treat it one char at a time
                glCallLists(str(line))

                glPopMatrix()	
                
            #pop the font matrix
            glPopMatrix()
            glPopAttrib()
            
        if self.shadow:
        #shadow gets offset slightly to the bottom right and is slightly less opaque than the original color
            draw(text, position = (self.position[0] + 1, self.position[1] - 2), color = (0,0,0,self.color[3]*.8))
        draw(text)    
