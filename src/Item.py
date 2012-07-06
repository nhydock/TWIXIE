from lxml import etree
from Command import loadCommand
from TwiObj import TwiObj
import os

class Item(TwiObj):
	
	cache = []	#stores all previously loaded items
	
	def __init__(self, node):
		super(Item, self).__init__(node.attrib["name"], node.find("Description").text)
		
		#get if the player can hold onto the item
		self.possess = bool(node.find("Possess").text in ["True", "true", "1"])
		
		self.command = loadCommand(node.find("Command"))
			
		#add self to loaded Item cache
		Item.cache.append(self)
		
	#gets the command that the item executes
	def getCommand(self):
		return self.command
		
	def execute(self):
		engine = Engine.getInstance()
		
		#execute the item's command
		try:
			self.command.execute("")
		#if the item is not usable or the item has no command then just say nothing happened
		except Exception:
			engine.show("Nothing happened")
			
#gets a preloaded item or loads a new item into cache using a provided node
def loadItem(node):
	#don't try loading anything if node is Nonetype
	if node is None:
		return None
	
	if len(node) > 0:
		return Item(node)
	else:
		name = node.attrib["name"].lower()
		for item in Item.cache:
			if name == str(item):
				return item
		return None		
		
