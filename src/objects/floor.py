from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle
from config import FLOOR_HEIGHT_RATIO
try:
	from config import COLUMN_CROSS_SECONDS
except Exception:
	COLUMN_CROSS_SECONDS = 3.0

class Floor(Widget):
	def __init__(self, texture, **kwargs):
		super(Floor, self).__init__(**kwargs)
		self.image = texture
		self.window_width, self.window_height = Window.size
		self.x_pos = 0

		floor_height = int(self.window_height * FLOOR_HEIGHT_RATIO)

		with self.canvas:
			self.rect1 = Rectangle(
				texture = self.image,
				size = (self.window_width, floor_height),
				pos = (self.x_pos, 0)
			)
			self.rect2 = Rectangle(
				texture = self.image,
				size = (self.window_width, floor_height),
				pos = (self.x_pos + self.window_width, 0)
			)

		self.bind(size=self.on_size)
		Window.bind(on_resize=self.on_resize)

	def on_resize(self, *args):
		self.window_width, self.window_height = map(int, Window.size)
		self.update_rectangles()

	def on_size(self, *args):
		self.window_width, self.window_height = map(int, self.size)
		self.update_rectangles()

	def update_rectangles(self):
		floor_height = int(self.window_height * FLOOR_HEIGHT_RATIO)

		self.rect1.size = (self.window_width, floor_height)
		self.rect2.size = (self.window_width, floor_height)
		self.rect1.pos = (self.x_pos, 0)
		self.rect2.pos = (self.x_pos + self.window_width, 0)

	def update(self, dt):
		# 背景と同じロジック：幅 / 秒数 = px/s
		speed_px_per_sec = self.window_width / float(COLUMN_CROSS_SECONDS)
		self.x_pos -= speed_px_per_sec * dt
		if self.x_pos <= -self.window_width:
			self.x_pos = 0

		self.rect1.pos = (self.x_pos, 0)
		self.rect2.pos = (self.x_pos + self.window_width, 0)


