import sfml as sf
from Core.CommandParser import CommandParser
from Utils.Scene import Scene


class TestScene(Scene):
	def start(self):
		#load up and create a test sprite
		texture = sf.Texture.load_from_file('../data/window.png')
		self.sprite = sf.Sprite(texture)

		#load up font
		font = sf.Font.load_from_file("../data/fonts/default.ttf")
		self.text = sf.Text();
		self.text.font = font
		self.text.color = sf.Color.BLACK
		self.text.character_size = 24
		self.text.position = (10, 450);

		self.cp = CommandParser(None)
		self.move = [False, False, False, False]

		return True

	def key_pressed(self, event):
		#type input
		if event.type == sf.Event.TEXT_ENTERED:
			if (event.unicode == '\b'):
				self.cp.removeLetter()
			else:
				self.cp.addLetter(event.unicode);

		#move the test sprite around
		elif event.code == sf.Keyboard.LEFT:
			self.move[0] = True
		elif event.code == sf.Keyboard.RIGHT:
			self.move[1] = True
		elif event.code == sf.Keyboard.UP:
			self.move[2] = True
		elif event.code == sf.Keyboard.DOWN:
			self.move[3] = True
		
	def key_released(self, event):
		if event.code == sf.Keyboard.LEFT:
			self.move[0] = False
		elif event.code == sf.Keyboard.RIGHT:
			self.move[1] = False
		elif event.code == sf.Keyboard.UP:
			self.move[2] = False
		elif event.code == sf.Keyboard.DOWN:
			self.move[3] = False
		

	def update(self, delta):
		#handle horizontal movement
		xrate = 0
		if self.move[0]:
			xrate -= 50
		elif self.move[1]:
			xrate += 50
		
		#handle vertical movement
		yrate = 0
		if self.move[2]:
			yrate -= 50
		elif self.move[3]:
			yrate += 50

		self.sprite.move(xrate * delta, yrate * delta);
		self.text.string = self.cp.getCurrentTypedMessage()

	def render(self, context, delta):
		context.draw(self.sprite)
		context.draw(self.text)