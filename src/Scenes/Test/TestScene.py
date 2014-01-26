import sfml as sf
from Utils.Scene import Scene


class TestScene(Scene):
	def start(self):
		#load up and create a test sprite
		texture = sf.Texture.load_from_file('../data/window.png')
		self.sprite = sf.Sprite(texture)

		return True

	def update(self, delta):
		#handle key input
		if sf.Keyboard.is_key_pressed(sf.Keyboard.RIGHT):
			self.sprite.move(50.0*delta, 0)
		elif sf.Keyboard.is_key_pressed(sf.Keyboard.LEFT):
			self.sprite.move(-50.0*delta, 0)

	def render(self, context, delta):
		context.draw(self.sprite)