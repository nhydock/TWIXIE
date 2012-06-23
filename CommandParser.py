

global_commands = [Look(), LookAt()]

#universal parser for the game
#handles executing user input commands
class CommandParser:
	def __init__(self, engine):
		#engine is required to detect and effect globally stored things
		#like the player and the current scene
		self.engine = engine
		
	#Parses a sentence entered by the user and executes
	# any related commands
	def execute(self, string):
		command = none
		#check against globally known commands
		for c in global_commands:
			if string.contains(c): #look for the name of the command in the string
				command = global_commands[c]
				#only execute the command if it's usable in the current situation
				if command.isUsable():
					command.execute()
				return
				
		#check against room/scenario specific commands
		for c in self.engine.getCurrentScenario().getCommands():
			if string is c:
				c.execute()
				#only execute the command if it's usable in the current situation
				if c.isUsable():
					command.execute()
				
#Base structure for a command
#Commands can be loaded in from a file
#While there are global commands, most commands are defined per room/scenario
class Command:
	def __init__(self, engine, name, file = None, node = None):
		self.engine = engine
		
		#if a file is provided to load data from, use it
		if file is not None:
			loadFromFile(file, node)
		else
			self.location = None
			self.name = name
		
	#loads a command and definitions from a file
	def loadFromFile(self, file, node):
		pass
		
	def execute(self, s):
		pass
			
	def usable(self):
		#ignore execution if the location where the command can be executed is not equal
		# to the name of the current scenario
		if self.location is not None and self.engine.getCurrentScenario() is not self.location:
			return False
		return True
		
		
	#sets the location of where commands can be used
	#if None or "Any" is passed through, the command will be usable globally
	def setLocation(self, location):
		if location is "Any":
			location = None
		self.location = location

#command displays the information about the current scenario
class Look(Command):
	def __init__(self, engine):
		super(self).__init__(engine)
		self.name = "look"		#command name
		self.location = None	#can be used anywhere
		
	#reshows the current rooms message and commands
	def execute(self, s):
		self.engine.show(self.engine.getCurrentScenario().getMessage())
			
#Command to look at a specific thing in the room or in your inventory
class LookAt(Command):
	def __init__(self, engine):
		super(self).__init__(engine)
		self.name = "look at"
		self.location = None
	
	#looks at an item
	def execute(self, s):
		#now we look for an item in the list of known items
		#the we look at the items in the scene
		for i in self.engine.getCurrentScenario().getObjects():
			if s.contains(i):
				self.engine.show(i.getMessage())
				return
			
		#then we look it the items in the inventory since that list has potential to be longer
		for i in self.engine.getInventory():
			if s.contains(i):
				self.engine.show(i.getMessage())
				return
					
		#if nothing was found display an error
		self.engine.show("No such thing exists")
	
		
