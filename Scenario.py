

class Scenario:
	def __init__(self, name):
		self.objects = []
		self.commands = []
		self.message = ""
		
	#gets a list of objects within the room that
	#can be looked at
	def getObjects(self):
		return self.objects
		
	#gets a list of the different commands
	#that are unique to this scenario
	def getCommands(self):
		return self.commands
		
	#gets the room description for displaying on
	#the screen when describing things
	def getMessage(self):
		return message	
