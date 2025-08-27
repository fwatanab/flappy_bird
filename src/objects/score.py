from kivy.uix.widget import Widget
from kivy.core.window import Window
from kivy.graphics import Rectangle
from kivy.utils import platform
from config import BASE_WIDTH

class Score(Widget):
	def __init__(self, number_textures, sound, **kwargs):
		super(Score, self).__init__(**kwargs)
		self.number_textures = number_textures
		self.point_sound = sound
		self.score = 0
		self.digits = []
		self.rectangles = []

		# モバイルかどうかでスケールを調整
		self.scale_factor = Window.width / float(BASE_WIDTH)  # 設定値を基準にスケール
		if platform in ("android", "ios"):
			self.scale_factor *= 1.5  # モバイルデバイスでは拡大

		# 数字のサイズ（元の画像サイズに基づく）
		self.digit_width = int(24 * self.scale_factor)
		self.digit_height = int(36 * self.scale_factor)

		# スコアの位置（画面上部中央）
		self.update_score_display()

		Window.bind(on_resize=self.resize)

	def resize(self, *args):
		"""ウィンドウサイズ変更時の処理"""
		# モバイルではスケールを大きくする
		self.scale_factor = Window.width / float(BASE_WIDTH)
		if platform in ("android", "ios"):
			self.scale_factor *= 1.5

		self.digit_width = int(24 * self.scale_factor)
		self.digit_height = int(36 * self.scale_factor)
		self.update_score_display()

	def update_score_display(self):
		"""スコア表示を更新"""
		self.canvas.clear()
		self.rectangles = []

		# スコアを文字列に変換
		score_str = str(self.score)

		# 全体の幅を計算
		total_width = len(score_str) * self.digit_width

		# 開始位置（画面上部中央）
		start_x = (Window.width - total_width) / 2
		start_y = int(Window.height * 0.9) - self.digit_height

		with self.canvas:
			for i, digit in enumerate(score_str):
				digit_texture = self.number_textures[int(digit)]
				digit_rect = Rectangle(
					texture=digit_texture,
					pos=(start_x + i * self.digit_width, start_y),
					size=(self.digit_width, self.digit_height)
				)
				self.rectangles.append(digit_rect)

	def check_score_count(self, bird, columns):
		"""鳥がパイプを通過したかチェック"""
		for column in columns:
			if not column.passed:
				# 鳥がパイプを通過したかどうか
				if bird.pos_x > column.pos_x + column.top_pipe_rect.size[0]:
					column.passed = True
					self.score += 1
					self.point_sound.play()
					self.update_score_display()
					return True
		return False
