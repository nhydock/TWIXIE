import pygame
import Engine
import os
import string

SOFTWARE = 0	#Basic software rendering mode for pygame
HARDWARE = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE	#Hardware rendering mode for pygame
CLEAR_COLOR = (0,0,0,255)	#clears the screen to black
TEXT_COLOR = (200, 115, 11, 255)

LINES_TO_DISPLAY = 3	#how many lines of description text are allowed to be shown at a time

#Client Component handles all the graphics drawing of the game
#It uses pyGame to display everything
class ClientComponent:
	
	"""
	Initializes the game window
	@param internal_res	the Resolution at which the game should be rendered at a code level
	@param output_res	the resolution at which the user will see the game being rendered at
	@param mode	the display mode for rendering the game, either Software or Hardware modes
	"""
	def __init__(self, internal_res, output_res, mode = SOFTWARE):
		self.engine = Engine.getInstance()	#get engine instance for rendering the scene
		
		pygame.display.init();
		
		#display buffers
		self.internal_buffer = pygame.Surface(internal_res)
		self.display_buffer = pygame.display.set_mode(output_res, mode)
		
		#font for the display
		self.font = pygame.font.Font(os.path.join("..", "data", "fonts", "default.ttf"), 12)
		
		#area to display the currently typed command
		self.textEntryArea = pygame.Surface((internal_res[0], self.font.get_linesize()+4))
		self.text = "> %s"
		
		self.message = None	#stores the wrapped message so the processing does not happen every frame
		self.messageDisplayArea = pygame.Surface((internal_res[0], self.font.get_linesize()*LINES_TO_DISPLAY))
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
		width = self.internal_buffer.get_width()	#width of the screen to wrap within
		
		print words
		
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
		print lines
		return lines
	
	#advances the line index
	def nextLines(self):
		self.mIndex += LINES_TO_DISPLAY
		#clear the message when the index is outside of the message bounds
		if self.mIndex > len(self.message)-1:
			self.message = None
			self.engine.show(None)
		
	#renders all the graphics
	def render(self):
		currentScene = self.engine.getScenario()

		#clean the buffers
		self.internal_buffer.fill(CLEAR_COLOR)
		self.display_buffer.fill(CLEAR_COLOR)
		
		#renders the currentScene's data to the buffer
		#currentScene.render(self.internal_buffer)
		
		#renders the text command to the screen
		if not self.engine.isShowingMessage():
			self.message = None
			self.textEntryArea.fill(CLEAR_COLOR)	#clear the text entry area
			self.textEntryArea.blit(self.font.render(self.text % self.engine.getTyped(), False, TEXT_COLOR), (3, 2)) #draws the text slightly offset in the box
			self.internal_buffer.blit(self.textEntryArea, (0, self.internal_buffer.get_height()-self.textEntryArea.get_height()))
		else:
			#format the message into lines of text
			if self.message is None:
				self.message = self.wrapWords(self.engine.getMessage())
			#clear area to show the message
			self.messageDisplayArea.fill(CLEAR_COLOR)
			#draw the lines of text that are currently showing
			for i in range(self.mIndex, min(len(self.message), self.mIndex+LINES_TO_DISPLAY)):
				self.messageDisplayArea.blit(self.font.render(self.message[i], False, TEXT_COLOR), (3, 2 + self.font.get_linesize()*(i % LINES_TO_DISPLAY)))
			self.internal_buffer.blit(self.messageDisplayArea, (0, self.internal_buffer.get_height()-self.messageDisplayArea.get_height()))
			
		#renders to the display
		self.display_buffer.blit(pygame.transform.scale(self.internal_buffer, self.display_buffer.get_size()), (0,0))
		
		pygame.display.flip()
