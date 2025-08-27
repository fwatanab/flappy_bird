from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from config import LOGO_SIZE_RATIO, LOGO_POS_RATIO

class Logo(Widget):
	def __init__(self, texture, **kwargs):
		super(Logo, self).__init__(**kwargs)
		self.image = texture
		self.size = (int(Window.width * LOGO_SIZE_RATIO[0]), int(Window.height * LOGO_SIZE_RATIO[1]))
		self.pos = (int((Window.width - self.size[0]) * LOGO_POS_RATIO[0]),
					int((Window.height - self.size[1]) * LOGO_POS_RATIO[1]))
		with self.canvas:
			self.rect = Rectangle(texture=self.image, size=self.size, pos=self.pos)
		Window.bind(on_resize=self.on_resize)

	def on_resize(self, *args):
		self.size = (int(Window.width * LOGO_SIZE_RATIO[0]), int(Window.height * LOGO_SIZE_RATIO[1]))
		self.pos = (int((Window.width - self.size[0]) * LOGO_POS_RATIO[0]),
					int((Window.height - self.size[1]) * LOGO_POS_RATIO[1]))
		self.rect.size = self.size
		self.rect.pos = self.pos
