#Typed-word Invokable Objects
#generic object type for TWIXIE
#since all core objects that get loaded from XML have these
#properties and are designed to be referencable from the user input
#then it's best to just keep it as a generic object
class TwiObj(object):
	def __init__(self, name = "", description = ""):
		self.name = name				#name of the object
		self.description = description	#description of the object that is seen when Look or Look At is called
		
	#gets the name of the object
	def getName(self):
		return self.name
		
	#gets the description of the object
	def getDescription(self):
		return self.description
		
	#string representation of the object as how it's acceptable from a command input perspective
	def __str__(self):
		return self.name.lower()
		
	def __repr__(self):
		return self.__str__()	
	
