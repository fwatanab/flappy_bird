import random
from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle
from config import PIPE_GAP_RATIO, PIPE_START_WIDTH, PIPE_SIZE_RATIO, PIPE_MIN, FLOOR_HEIGHT_RATIO
try:
	from config import COLUMN_CROSS_SECONDS
except Exception:
	COLUMN_CROSS_SECONDS = 3.0

class Column(Widget):
	def __init__(self, texture, **kwargs):
		super(Column, self).__init__(**kwargs)
		self.image = texture

		# 上パイプ用に180度回転したテクスチャを生成
		self.top_pipe_texture = self.create_rotated_texture(self.image)

		# パイプの初期位置
		self.pos_x = Window.width * PIPE_START_WIDTH

		# パイプの位置をランダム生成
		self.create_pipes()
		# リサイズ時のために比率を記録
		self._bottom_ratio = self.bottom_pipe_height / float(max(1, Window.height))
		self._top_ratio = self.top_pipe_height / float(max(1, Window.height))

		# パイプの通過判定
		self.passed = False

		self.draw_pipe()

	def draw_pipe(self):
		self.canvas.clear()

		with self.canvas:
			self.top_pipe_rect = Rectangle(
				texture = self.top_pipe_texture,
				size = (Window.width * PIPE_SIZE_RATIO, self.top_pipe_height),
				pos = (self.pos_x, Window.height - self.top_pipe_height)
			)
			self.bottom_pipe_rect = Rectangle(
				texture = self.image,
				size = (Window.width * PIPE_SIZE_RATIO, self.bottom_pipe_height),
				pos = (self.pos_x, Window.height * FLOOR_HEIGHT_RATIO)
			)

	def resize(self, *args):
		# 画面高さに合わせてギャップを再計算（難易度一定）
		h = float(max(1, Window.height))
		floor_height = Window.height * FLOOR_HEIGHT_RATIO
		pipe_gap = Window.height * PIPE_GAP_RATIO
		# 下は前回比率で復元
		self.bottom_pipe_height = max(1, int(h * self._bottom_ratio))
		# 上は総和一定（床〜天井から gap と bottom を引く）
		self.top_pipe_height = max(1, int(Window.height - floor_height - (self.bottom_pipe_height + pipe_gap)))
		self.draw_pipe()

	def create_rotated_texture(self, texture):
		flipped_texture = texture.get_region(0, 0, texture.width, texture.height)
		flipped_texture.flip_vertical()
		flipped_texture.flip_horizontal()
		return flipped_texture

	def create_pipes(self):
		floor_height = Window.height * FLOOR_HEIGHT_RATIO
		pipe_min = Window.height * PIPE_MIN
		pipe_gap = Window.height * PIPE_GAP_RATIO

		# 床の上からランダムな高さに下パイプを配置
		bottom_pipe_max = Window.height - floor_height - pipe_gap - pipe_min
		bottom_pipe_min = pipe_min

		# ランダムに上パイプの位置を決定
		self.bottom_pipe_height = random.uniform(pipe_min, max(pipe_min, bottom_pipe_max))
		self.top_pipe_height = Window.height - floor_height - (self.bottom_pipe_height + pipe_gap)

		# さらにランダム性を追加
		if random.choice([True, False]):
			self.bottom_pipe_height *= random.uniform(0.8, 1.2)
			self.top_pipe_height = Window.height - floor_height - (self.bottom_pipe_height + pipe_gap)

		# 比率を保存（以降のリサイズで使用）
		h = float(max(1, Window.height))
		self._bottom_ratio = self.bottom_pipe_height / h
		self._top_ratio = self.top_pipe_height / h

	def update(self, dt):
		# 幅 / 秒数 = px/s で一定の体感スピード
		speed_px_per_sec = Window.width / float(COLUMN_CROSS_SECONDS)
		self.pos_x -= speed_px_per_sec * dt

		self.top_pipe_rect.pos = (self.pos_x, Window.height - self.top_pipe_height)
		self.bottom_pipe_rect.pos = (self.pos_x, Window.height * FLOOR_HEIGHT_RATIO)

	def is_out_of_screen(self):
		return self.pos_x + self.top_pipe_rect.size[0] < 0
