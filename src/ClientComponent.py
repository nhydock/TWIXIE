import pygame
import Engine
import os
import string
from sysobj import *
from View import Scene #this is actually considered a scene object
from View import INTERNAL_RESOLUTION as IRES	#import the internal resolution to work with for positioning things

CLEAR_COLOR = (0,0,0,255)	#clears the screen to black
TEXT_COLOR = (200, 115, 11, 255)
FONT_SIZE = 32

LINES_TO_DISPLAY = 6	#how many lines of description text are allowed to be shown at a time

#Client Component handles all the graphics drawing of the game
#It uses pyGame to display everything
class ClientComponent(Scene):
	
	"""
	Initializes the game window
	"""
	def __init__(self):
		self.engine = Engine.getInstance()	#get engine instance for rendering the scene
		
		#font for the display
		self.font = FontObj("default.ttf", FONT_SIZE)
		self.font.setColor(TEXT_COLOR)
		
		#area to display the currently typed command
		self.text = "> %s"
		
		self.message = None	#stores the wrapped message so the processing does not happen every frame
		self.mIndex = 0		#current line index for the message display
		
	#gets the global font for use
	def getFont(self):
		return self.font
		
	#wrap words to screen size
	def wrapWords(self, s):
		lines = []					#lines generated
		line = []					#words in current line
		words = s.split()			#split up the string into individual words
		word = ""					#current word to analyze
		size = 0					#size in pixels of the current word
		iterator = 0				#index in word list
		xStart = 10					#x position to start calculations from
		x = 0						#x position on screen for wrapping
		width = IRES[0]				#width of the screen to wrap within
		
		#operation to take the string and divide it into lines
		for word in words:
			size = self.font.size(word + " ")[0] 
			
			#if word added to current x exceeds boundaries, then wrap it
			if x + size > width or word is "\n":
				lines.append(string.join(line, " "))
				line = [word]	#make new line with the word in it
				x = xStart + size
			#else just add to thel ine
			else:
				line.append(word)
				x += size
			
		#add the last line
		lines.append(string.join(line, " "))
		return lines
	
	#handles key input
	def keyPressed(self, key, char):
		print char
		
		#if the engine is showing a message, skip through the message when any button is pressed
		if self.engine.isShowingMessage():
			self.nextLines()	#advances the message on key press
			return
		
		#execute commands on pressing return
		if key == K_RETURN:
			self.engine.parser.execute()
		#remove a letter from the player's command
		elif key == K_BACKSPACE:
			self.engine.parser.removeLetter()
		#add the letter to the player's command
		else:
			self.engine.parser.addLetter(char)
		
	#advances the line index
	def nextLines(self):
		self.mIndex += LINES_TO_DISPLAY
		#clear the message when the index is outside of the message bounds
		if self.mIndex > len(self.message)-1:
			self.message = None
			self.engine.show(None)
			self.mIndex = 0
		
	#renders all the graphics
	def render(self, visibility):
		currentScene = self.engine.getScenario()

		#renders the currentScene's data to the buffer
		#currentScene.render(self.internal_buffer)
		
		#renders the text command to the screen
		
		if not self.engine.isShowingMessage():
			self.message = None
			self.font.setPosition(3, self.font.get_height())
			self.font.render(self.text % self.engine.getTyped())
		else:
			#format the message into lines of text
			if self.message is None:
				self.message = self.wrapWords(self.engine.getMessage())
			#draw the lines of text that are currently showing
			for i in range(self.mIndex, min(len(self.message), self.mIndex+LINES_TO_DISPLAY)):
				self.font.setPosition(3, 2 + self.font.get_height()*(i % LINES_TO_DISPLAY))
				self.font.render(self.message[i])
			#self.internal_buffer.blit(self.messageDisplayArea, (0, self.internal_buffer.get_height()-self.messageDisplayArea.get_height()))
