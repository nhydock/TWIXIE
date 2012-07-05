from lxml import etree
from Command import Command, getCommand
import os

class Scenario:
	def __init__(self, path):
		self.objects = []
		self.commands = []
		self.message = ""
		
		#now we do the parsing of the xml file
		source = open(os.path.join("..", "data", "rooms", path + ".xml"))
		tree = etree.parse(source)
		#root of the xml
		root = tree.getroot()
		
		#name of the room	
		self.name = root.attrib["name"]
		
		#get the description of the room that can be displayed when Look is called
		self.message = root.attrib["description"]
		
		#get all the names of commands specific to the room
		self.commands = []
		for n in root.findall("Command"):
			if len(n) > 0: 
				self.commands.append(Command(node = n))
			else: 
				self.commands.append(getCommand(n.attrib["name"]))
				
		print self.commands
		
		#get all the names of items found in the room
		self.objects = []
		"""
		for n in root.findall("Item"):
			if len(n) > 0: 
				self.commands.append(Item(node = n))
			else: 
				self.commands.append(getCommand(n.attrib["name"]))
		"""
		
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
