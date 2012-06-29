import pygame
import Engine

SOFTWARE = 0	#Basic software rendering mode for pygame
HARDWARE = pygame.OPENGL | pygame.DOUBLEBUF | pygame.HWSURFACE	#Hardware rendering mode for pygame
CLEAR_COLOR = (0,0,0,255)	#clears the screen to black
TEXT_COLOR = (200, 115, 11, 255)

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
		
		self.internal_buffer = pygame.Surface(internal_res)
		self.display_buffer = pygame.display.set_mode(output_res, mode)
		
		self.font = pygame.font.Font("../data/fonts/default.ttf", 12)
		self.textEntryArea = pygame.Surface(internal_res, self.font.get_height()+4)
		
	#gets the global font for use
	def getFont(self):
		return self.font
		
	#renders all the graphics
	def render(self):
		print self.engine.getTyped()
		currentScene = self.engine.getScenario()

		#clean the buffers
		self.internal_buffer.fill(CLEAR_COLOR)
		self.display_buffer.fill(CLEAR_COLOR)
		
		#renders the currentScene's data to the buffer
		#currentScene.render(self.internal_buffer)
		
		#renders the text command to the screen
		self.textEntryArea.fill(CLEAR_COLOR)	#clear the text entry area
		self.textEntryArea.blit(self.font.render("> %s" % self.engine.getTyped(), True, TEXT_COLOR), (3, 2)) #draws the text slightly offset in the box
		self.internal_buffer.blit(self.textEntryArea, (0, self.internal_buffer.get_height()-self.textEntryArea.get_height()))
		
		#renders to the display
		self.display_buffer.blit(pygame.transform.scale(self.internal_buffer, self.display_buffer.get_size()), (0,0))
		
		pygame.display.flip()
