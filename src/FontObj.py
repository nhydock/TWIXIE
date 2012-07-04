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

import numpy as np
from numpy import array, float32

from Texture import Texture #create Textures specifically instead of loadTexture because surfaces can't be cached

import string

#global alignment variables
LEFT   = 0
CENTER = 1
RIGHT  = 2

#set up the generic texture array
TEX_ARRAY = np.zeros((4,2), dtype=float32)

#top left, top right, bottom right, bottom left
#texture coordinates
TEX_ARRAY[0,0] = 0; TEX_ARRAY[0,1] = 0
TEX_ARRAY[1,0] = 1; TEX_ARRAY[1,1] = 0
TEX_ARRAY[2,0] = 1; TEX_ARRAY[2,1] = 1
TEX_ARRAY[3,0] = 0; TEX_ARRAY[3,1] = 1

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
		
		self.generateGlyphs()

		#attributes
		self.scale     = (1.0, 1.0)             #image bounds (width, height)
		self.position  = (0,0)                  #where in the window it should render
		self.angle     = 0                      #angle which the image is drawn
		self.color     = (255,255,255,255)      #colour of the image
		self.alignment = 1                      #alignment of the text (left, center , right)
		self.shadow = True                      #does the font project a shadow

	def stringWidth(self, string):
		s = 0
		for i in list(string):
			s += self.glyphTex[ord(i)].pixelSize[0]
		return s
		
	#generates a dictionary of glyphs for use
	def generateGlyphs(self):
		self.listBase = glGenLists(128)
		self.glyphTex = [None] * 128
		for i in xrange(128):
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
			vtxArray = np.zeros((4,3), dtype=float32)
			pixelSize = self.glyphTex[i].pixelSize
			halfPS = (float(pixelSize[0])/2.0, float(pixelSize[1])/2.0)

			vtxArray[0,0] = 0;            vtxArray[0,1] =  halfPS[1]
			vtxArray[1,0] = pixelSize[0]; vtxArray[1,1] =  halfPS[1]
			vtxArray[2,0] = pixelSize[0]; vtxArray[2,1] = -halfPS[1]
			vtxArray[3,0] = 0;            vtxArray[3,1] = -halfPS[1]
			
			#bind and render the glyph
			self.glyphTex[i].bind()

			glEnableClientState(GL_TEXTURE_COORD_ARRAY)
			glEnableClientState(GL_VERTEX_ARRAY)
			glVertexPointerf(vtxArray)
			glTexCoordPointerf(TEX_ARRAY)
			glDrawArrays(GL_QUADS, 0, vtxArray.shape[0])
			glDisableClientState(GL_VERTEX_ARRAY)
			glDisableClientState(GL_TEXTURE_COORD_ARRAY)

			glPopMatrix()
						
			#shift the character over a little so it won't overlap with other letters
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
	def setScale(self, width, height):
		if self.scale[0] != width and self.scale[1] != height:
			if (width >= 0 and width <= 1) and (height >= 0 and height <= 1):
				self.scale = (width,height)
			else:
				self.scale = (float(width)/float(self.pixelSize[0]), float(height)/float(self.pixelSize[1]))
		
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
	def render(self, text, antialias = True, color = None, background = None):
		#submethod for rendering the text in its proper settings
		#this is used so then shadows and other text effects that require rendering multiple times can
		# just be easily called
		def draw(position = self.position, scale = self.scale, angle = self.angle, color = self.color):

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
			glScalef(scale[0], scale[1], 1.0)	#then we scale it up
			glRotatef(angle, 0, 0, 1)			#then we rotate it
			glColor4f(*color)					#and finally we apply the colour

			#reset x, it's going to be moving now
			y = 1
			height = self.get_linesize()	#amount of space to reserve for each line

			glListBase(self.listBase)
			#first we split the text into lines
			for line in text.split("\n"):
				glTranslate(0, y, 0)	#shift the line down
				
				glPushMatrix()
			
				#then we take the line and treat it one char at a time
				glCallLists(str(line))

				glPopMatrix()	
				
				y += height	#move y down a line
			#pop the font matrix
			glPopMatrix()
			glPopAttrib()
			
		if self.shadow:
		#shadow gets offset slightly to the bottom right and is slightly less opaque than the original color
			draw(position = (self.position[0] + 1, self.position[1] - 2), color = (0,0,0,self.color[3]*.8))
		draw()    
