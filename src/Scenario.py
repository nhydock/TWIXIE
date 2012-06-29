from xml.dom.minidom import parse, parseString
import os

class Scenario:
	def __init__(self, path):
		self.objects = []
		self.commands = []
		self.message = ""
		
		#now we do the parsing of the xml file
		source = open(os.path.join("..", "data", "rooms", path + ".xml"))
		dom = parse(source)
		#root of the xml
		top = dom.getElementsByTagName("Room")[0]
		
		#name of the room	
		self.name = top.getElementsByTagName("Name")[0].firstChild.data	
		
		#get the description of the room that can be displayed when Look is called
		self.message = top.getElementsByTagName("Description")[0].firstChild.data
		
		#get all the names of commands specific to the room
		self.commands = [n.firstChild.data for n in top.getElementsByTagName("CommandName")]	
		
		#get all the names of items found in the room
		self.objects = [n.firstChild.data for n in top.getElementsByTagName("ItemName")]	
		
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
		return self.message	
