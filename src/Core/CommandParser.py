
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
		
	#gets the currently typed command as a string
	def getCurrentTypedMessage(self):
		return string.join(self.typed, "")
		
	#adds a letter to the currently typed command
	def addLetter(self, char):
		self.typed.append(char)
	
	#pop off the last letter
	def removeLetter(self):
		self.typed = self.typed[:-1]
		
	#Parses a sentence entered by the user and executes
	# any related commands
	def execute(self):
		if self.typed is []:
			return
		#get the currently typed command to parse
		#ensure it's lower case, all commands should be registered in lower case so then case doesn't matter
		s = self.getCurrentTypedMessage().lower() 
		self.typed = []	#clear the command when it goes to execute
		print s
		
		command = None
		#default show message that thinks the command is wrong
		self.engine.show("What are you even trying to do?")
		try:
			#check against globally known commands and against room/scenario specific commands
			for c in global_commands+self.engine.getScenario().getCommands():
				if str(c) in s: #look for the name of the command in the string
					c.execute(s)
					return
		except Exception as e:
			print e
		
