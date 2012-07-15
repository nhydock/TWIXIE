import threading
from Graphics.ClientComponent import *
from Core import Engine, Input
from pygame.locals import *

import os
import sys

from Graphics.View import Viewport, HARDWARE

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
            Input.update()          #first will check for key presses
            
            #we get the top most scene for updating logic
            scene = self.viewport.getTopMostScene()
                    
            if scene is not None:
                scene.run()         #any calculations of interactions are processed from the
                                    # previous loop before anything new is rendered

            self.viewport.update()  #we update the graphics of the current scene
            
            if scene is not None:
                #we use the topmost scene because it should be the only one effected
                # by user input in the simple case of this game
                self.detectInput(scene)
            
            #we reset the input so then previous events do not continue stacking in for checking
            Input.reset()

            #we check the game clock and figure current FPS
            self.clock.tick(FPS)
            self.currentFPS = int(self.clock.get_fps())

            #fps counter is in the title bar
            pygame.display.set_caption(caption % (self.currentFPS))
			
    #checks to see where the position of the mouse is over 
    #an object and if that object has been clicked
    #also handles all the key input and passes it to the current scene
    def detectInput(self, scene):
        for key, char in Input.getKeyPresses():
            scene.keyPressed(key, char)

        #in the case of this game, we are not using mouse input
        """
        for press in Input.clicks:
            clickedImages = [image.getCollision(press) for image in ImgObj.clickableObjs]
            try:
                x = clickedImages.index(True)
                scene.buttonClicked(ImgObj.clickableObjs[x])
            except ValueError:
                continue
        """
		

#main execution method
def main():
    thread = Runner()
    thread.start()

	
if __name__ == '__main__':
    main()
