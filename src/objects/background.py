from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.graphics import Rectangle
from config import SCROLL_SPEED
try:
	from config import COLUMN_CROSS_SECONDS  # 例: 3.0 sec
except Exception:
	COLUMN_CROSS_SECONDS = 3.0  # フォールバック（好みで調整）

class Background(Widget):
	def __init__(self, texture, **kwargs):
		super(Background, self).__init__(**kwargs)
		self.image = texture

		# 画面サイズを取得して初期描画
		self.window_width, self.window_height = map(int, Window.size)
		self.x_pos = 0

		# キャンバスを描画
		with self.canvas:
			self.rect1 = Rectangle(
				texture = self.image,
				size = (self.window_width, self.window_height),
				pos = (self.x_pos, 0)
			)
			self.rect2 = Rectangle(
				texture = self.image,
				size = (self.window_width, self.window_height),
				pos = (self.x_pos + self.window_width, 0)
			)

		# サイズ変化に合わせる（任意）
		self.bind(size=self.on_size)
		Window.bind(on_resize=self.on_resize)

	def resize(self, *args):
		"""Game から明示的に呼べる窓口。"""
		self.window_width, self.window_height = Window.size
		self.update_rectangles()

	def on_resize(self, *args):
		self.window_width, self.window_height = Window.size
		self.update_rectangles()

	def on_size(self, *args):
		w, h = self.size
		self.window_width, self.window_height = int(w), int(h)
		self.update_rectangles()

	def update_rectangles(self):
		# 2枚ともサイズを変更
		self.rect1.size = (self.window_width, self.window_height)
		self.rect2.size = (self.window_width, self.window_height)

		# 位置を調整（背景がスクロール中の場合も正しく表示されるように
		self.rect1.pos = (self.x_pos, 0)
		self.rect2.pos = (self.x_pos + self.window_width, 0)


	def update(self, dt):
		# 画面幅 / 秒数 = px/s にすることで、どの幅でも体感速度一定
		speed_px_per_sec = self.window_width / float(COLUMN_CROSS_SECONDS)
		self.x_pos -= speed_px_per_sec * dt

		# 一定以上左に行ったらリセット
		if self.x_pos <= -self.window_width:
			self.x_pos = 0
		
		# 背景位置を更新
		self.rect1.pos = (self.x_pos, 0)
		self.rect2.pos = (self.x_pos + self.window_width, 0)
