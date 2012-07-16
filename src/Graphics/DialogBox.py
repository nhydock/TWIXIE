'''

2012 Nicholas Hydock
TWIXIE
Typed-Word Invokable Xenomorphic Incident Engine

Licensed under the GNU General Public License V3
http://www.gnu.org/licenses/gpl.html

'''

from OpenGL.GL import *
from OpenGL.GLU import *

import string

from WinObj import WinObj

#a window created to be used that can show text within it
class DialogBox(WinObj):
    #method that takes a string and wraps it into multiple lines
    #dependent on a window's dimensions
    @staticmethod
    def wrapText(s, window):
        dialog = []                 #the final dialog lines that get displayed
        lines = []					#lines generated
        line = []					#words in current line
        words = s.split()			#split up the string into individual words
        word = ""					#current word to analyze
        size = 0					#size in pixels of the current word
        iterator = 0				#index in word list
        x = 0						#x position on screen for wrapping
        width = window.getWidth()   #the width to wrap to
        
        #now we take into consideration window borders when wrapping
        #remember that window's extend ImgObj, so pixelSize is 1/3 the
        #size of the window's texture width wise.  Since we're taking
        #into account both borders, we subtract twice the border size
        width -= window.pixelSize[0]*2
        
        #we determine how many lines the dialog box will be able to show at
        #one time by taking the window's font and the height of the window
        LINE_LIMIT = (window.getHeight()-(window.pixelSize[1]*2))/window.font.get_linesize()
        print LINE_LIMIT
        
        #operation to take the string and divide it into lines
        for word in words:
            #get the width of the word in pixels dependent on the window's font
            size = window.font.stringWidth(word + " ")
            
            #if word added to current x exceeds boundaries, then wrap it to the next line
            if x + size > width:
                #we join all the previously stored words into a new line
                lines.append(string.join(line, " "))
                
                #if the amount of lines is at the limit, we start a new block
                if len(lines) >= LINE_LIMIT:
                    dialog.append(string.join(lines, "\n"))
                    lines = []
                    
                line = [word]	#make new line with the word in it
                x = size        #reposition x to beginning of the line
            #else just add to the ine
            else:
                line.append(word)
                x += size
            
        #add the last line
        lines.append(string.join(line, " "))
        dialog.append(string.join(lines, "\n"))
        print dialog
        return dialog
        
    #initializes a dialog box object
    def __init__(self, texture, font, width = 64, height = 64):
        super(DialogBox, self).__init__(texture, width, height)
        self.font = font
        self.text = []
        
    #adds a new string into the dialog box to display
    def addText(self, text):
        #dialog is in line-listed chunks, so first, we need to wrap the text
        # to fit the window
        text = DialogBox.wrapText(text, self)
        
        for s in text:
            self.text.append(s)
            
        print self.text
        
    #empties the text from the dialog box
    def clear(self):
        self.text = []

    #allow setting the height by the number of lines you want the dialogbox
    #to be able to show at any single time
    def setHeightByLines(self, i):
        self.height = (self.font.get_linesize()*i) + (self.pixelSize[1]*2)  #can't forget border allocation
        
    #gets the count of how many text blocks there are in the dialog box
    #when len is used on it
    def __len__(self):
        return len(self.text)
        
    #draws the window and text to screen
    # @param block_index
    #   text is wrapped and divided into blocks that the window can display
    #   blocks as in chunks of lines that fit into the window
    #   the set of lines 
    def draw(self, block_index = 0):
        
        #don't draw anything if the block index specified is out of range
        if block_index >= len(self):
            return
            
        #draw the window
        super(DialogBox, self).draw()
        
        #displays the lines of text within the window
        #print self.text[block_index]
        glPushMatrix()
        glTranslatef(self.pixelSize[0], 0, 0)
        self.font.setPosition(self.position[0], self.position[1])
        self.font.render(self.text[block_index])
        glPopMatrix()
            
        
