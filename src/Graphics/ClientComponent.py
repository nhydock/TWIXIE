import pygame
from pygame.locals import *
from Core import Engine
import os

from Graphics.GfxObj import *

#The client component is actually considered a scene object
from Core.View import Scene 

#import the internal resolution to work with for positioning things
from Core.View import INTERNAL_RESOLUTION as IRES	


CLEAR_COLOR = (0,0,0,255)	#clears the screen to black
TEXT_COLOR = (200/255.0, 115/255.0, 11/255.0, 255/255.0)
FONT_SIZE = 24

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
        
        self.messageWindow = DialogBox(Texture("window.png"), self.font, (64, 64))
        
    #gets the global font for use
    def getFont(self):
        return self.font

    #handles key input
    def keyPressed(self, key, char):
        #print char
		
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
        self.mIndex += 1
        #clear the message when the index is outside of the message bounds
        if self.mIndex > len(self.messageWindow):
            self.messageWindow.clear()
            self.engine.show(None)
            self.mIndex = 0
        
    #renders all the graphics
    def render(self, visibility):
        currentScene = self.engine.getScenario()

        #renders the currentScene's picture to the screen
        background = currentScene.getImage()
        #place the background in the center of the screen
        background.setPosition(IRES[0]/2, IRES[1]/2)
        #scale the background to the size of the window
        background.setScale(min(background.pixelSize[0], IRES[0]-64), min(background.pixelSize[1], IRES[1]), True)	
        #give the image a hue
        background.setColor(TEXT_COLOR)
        #now the image should fill the background of the window
        background.draw()
		
		#renders the text command to the screen
        if not self.engine.isShowingMessage():
            self.font.setPosition(3, self.font.get_height())
            self.font.render(self.text % self.engine.getTyped())
        else:
			#format the message into lines of text
            if len(self.messageWindow) == 0:
                #we need to set the desired size first before we add the text into it
                self.messageWindow.setDimensions(IRES[0]/2, 0)
                self.messageWindow.setHeightByLines(LINES_TO_DISPLAY)
                #now we can add the message text
                self.messageWindow.addText(self.engine.getMessage())
                #and then we position it on screen
                self.messageWindow.setPosition(16, IRES[1]/2)
                
            #draws the dialog box
            self.messageWindow.draw(self.mIndex)
			
