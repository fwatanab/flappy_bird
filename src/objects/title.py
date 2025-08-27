from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from config import TITLE_SIZE_RATIO, TITLE_POS_RATIO

class Title(Widget):
	def __init__(self, texture, **kwargs):
		super(Title, self).__init__(**kwargs)
		self.image =  texture

		self.size = (
			Window.width * TITLE_SIZE_RATIO[0],
			Window.height * TITLE_SIZE_RATIO[1]
		)
		self.pos = (
			(Window.width - self.size[0]) * TITLE_POS_RATIO[0],
			(Window.height - self.size[1]) * TITLE_POS_RATIO[1]
		)

		# タイトル描画設定
		with self.canvas:
			self.rect = Rectangle(
				texture = self.image,
				size = self.size,
				pos = self.pos
			)
		Window.bind(on_resize=self.on_resize)

	def on_resize(self, *args):
		self.size = (
			int(Window.width * TITLE_SIZE_RATIO[0]),
			int(Window.height * TITLE_SIZE_RATIO[1])
		)
		self.pos = (
			int((Window.width - self.size[0]) * TITLE_POS_RATIO[0]),
			int((Window.height - self.size[1]) * TITLE_POS_RATIO[1])
		)
		self.rect.size = self.size
		self.rect.pos = self.pos

