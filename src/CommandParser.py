
from Command import global_commands
import string

#universal parser for the game
#handles executing user input commands
class CommandParser:
	def __init__(self, engine):
		
		#engine is required to detect and effect globally stored things
		#like the player and the current scene
		self.engine = engine
		self.typed = []
		
	def getCurrentTypedMessage(self):
		return string.join(self.typed, "")
		
	def addLetter(self, char):
		self.typed.append(char)
	
	#pop off the last letter
	def removeLetter(self):
		self.typed = self.typed[:-1]
		
	#Parses a sentence entered by the user and executes
	# any related commands
	def execute(self):
		s = self.getCurrentTypedMessage()
		command = none
		#check against globally known commands
		for c in global_commands:
			if s.contains(c): #look for the name of the command in the string
				command = global_commands[c]
				#only execute the command if it's usable in the current situation
				if command.isUsable():
					command.execute()
				return
				
		#check against room/scenario specific commands
		for c in self.engine.getCurrentScenario().getCommands():
			if s is c:
				c.execute()
				#only execute the command if it's usable in the current situation
				if c.isUsable():
					command.execute()

		
