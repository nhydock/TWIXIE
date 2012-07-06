import threading
from ClientComponent import *
import Engine
import Input
from pygame.locals import *

import os
import sys

from View import Viewport, HARDWARE

_output_resolution = [800, 480]		#size that the engine will output for viewing and interacting

FPS = 60

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
		self.screen = pygame.display.set_mode(_output_resolution, HARDWARE)
        
		engine = Engine.getInstance()
		self.viewport = Viewport(_output_resolution)

		self.viewport.pushScene(ClientComponent())

		# main event loop
		while not Input.finished:
			Input.update()

			self.viewport.run()
			Input.reset()

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
