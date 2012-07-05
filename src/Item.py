from lxml import etree
from Command import Command, getCommand
import os

class Item(object):
	
	cache = {}	#stores all previously loaded items
	
	def __init__(self, node = None):
		
		self.name = ""
		self.message = ""
		self.command = None
		self.possess = True
		
		if node is not None:
			self.loadFromNode(node)
			
		#add self to loaded Item cache
		Item.cache[self.name] = self
	
	#loads a command and definitions from a file
	def loadFromNode(self, node):
		
		#name of the room	
		self.name = node.attrib["name"]	
		
		#get the description of the room that can be displayed when Look is called
		self.message = node.attrib["description"]
		
		#get if the player can hold onto the item
		self.possess = bool(node.find("Possess").text in ["True", "true", "1"])
		
		self.command = node.find("Command")
		if len(node) > 0:
			self.command = Command(self.command)
		else:
			self.command = getCommand(self.command.attrib["name"])
		
		print self.message
		print self.location
		print self.requirements
		print self.consumes
		print self.produces
			
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
		
	def execute(self):
		engine = Engine.getInstance()
		
		#execute the item's command
		try:
			self.command.execute("")
		#if the item is not usable or the item has no command then just say nothing happened
		except Exception:
			engine.show("Nothing happened")

	#string representation of the item as how it's acceptable from a command input perspective
	def __str__(self):
		return self.name.lower()
		
	def __repr__(self):
		return self.__str__()
