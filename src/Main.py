import threading
from ClientComponent import *
import Engine
import Input
from pygame.locals import *

import os
import sys

_internal_resolution = [320, 240]	#size that the engine should render in
_output_resolution = [800, 600]		#size that the engine will output for viewing and interacting

FPS = 30

caption = 'TWIXIE [FPS: %i]'

class Runner(threading.Thread):
	#Runner method for the update thread
	#this controls update calls to the system and graphic components of the program
	def run(self):
		#start up all the pygame things
		pygame.mixer.pre_init(44100)

		pygame.init()

		os.environ['SDL_VIDEO_WINDOW_POS'] = 'center'   #centers the window in the middle of your screen

		self.clock = pygame.time.Clock()
		self.currentFPS = 60    #the currentFPS the engine is rendering at

		#start/initializes the Thread and its engine components
		i = 0
		engine = Engine.getInstance()
		graphics = ClientComponent(_internal_resolution, _output_resolution, SOFTWARE)
	
		while not Input.finished:
			graphics.render()	#update graphics
			Input.update()
			#handle key input
			for key, char in Input.getKeyPresses():
				print engine.parser.getCurrentTypedMessage()
				#if the engine is showing a message, skip through the message when any button is pressed
				if engine.isShowingMessage():
					continue
				
				#execute commands on pressing return
				if key == K_RETURN:
					engine.parser.execute()
				#add the letter to the player's command
				elif key == K_BACKSPACE:
					engine.parser.removeLetter()
				else:
					engine.parser.addLetter(char)

			self.clock.tick(FPS)
			self.currentFPS = int(self.clock.get_fps())
			
			#fps counter is in the title bar
			pygame.display.set_caption(caption % (self.currentFPS))
			
			

#main execution method
def main():
	thread = Runner()
	thread.start()

	
if __name__ == '__main__':
	main()
