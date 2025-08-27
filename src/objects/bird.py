from kivy.uix.widget import Widget
from kivy.uix.image import Image
from kivy.core.window import Window
from kivy.graphics import Rectangle
from config import GRAVITY, FLAP_POWER, BIRD_START_RATIO, BIRD_SIZE_RATIO, FLOOR_HEIGHT_RATIO

class Bird(Widget):
	def __init__(self, textures, **kwargs):
		super(Bird, self).__init__(**kwargs)
		self.images = textures

		self.image_index = 0
		self.current_image = self.images[self.image_index]
		self.animation_timer = 0
		self.animation_speed = 0.1  # 秒単位でのアニメーション速度

		# 初期位置設定
		self.pos_x = int(Window.width * BIRD_START_RATIO[0])
		self.pos_y = int(Window.height * BIRD_START_RATIO[1])
		self.size_x = int(Window.width * BIRD_SIZE_RATIO[0])
		self.size_y = int(Window.height * BIRD_SIZE_RATIO[1])
		self._prev_w = float(Window.width)
		self._prev_h = float(Window.height)
		self.velocity = 0
		self.rotation = 0  # 回転角度

		# キャンバスの設定
		with self.canvas:
			self.rect = Rectangle(
				texture = self.current_image,
				size = (self.size_x, self.size_y),
				pos = (self.pos_x, self.pos_y)
			)

		# 画面サイズ変更時に再描画
		self.bind(size=self.on_size)
		Window.bind(on_resize=self.on_resize)

	def on_resize(self, *args):
		# 前ウィンドウ比を使って位置を維持
		new_w, new_h = float(Window.width), float(Window.height)
		x_ratio = self.pos_x / max(1.0, self._prev_w)
		y_ratio = self.pos_y / max(1.0, self._prev_h)

		# サイズ更新
		self.size_x = int(new_w * BIRD_SIZE_RATIO[0])
		self.size_y = int(new_h * BIRD_SIZE_RATIO[1])

		# 位置維持（比率ベース）
		self.pos_x = int(new_w * x_ratio)
		self.pos_y = int(new_h * y_ratio)
		self._prev_w, self._prev_h = new_w, new_h

		# 描画を更新
		self.rect.size = (self.size_x, self.size_y)
		self.rect.pos = (self.pos_x, self.pos_y)

	def on_size(self, *args):
		# ウィジェットのサイズが変わった場合の処理
		# resize()と同じことを行うが、インターフェースの統一のために維持
		new_width = int(Window.width * BIRD_SIZE_RATIO[0])
		new_height = int(Window.height * BIRD_SIZE_RATIO[1])

		# 変更がある場合のみ描画を更新
		if (new_width, new_height) != (self.size_x, self.size_y):
			self.size_x = new_width
			self.size_y = new_height
			self.rect.size = (self.size_x, self.size_y)

	def update(self, dt, columns):
		# アニメーション更新
		self.animation_timer += dt

		if self.animation_timer >= self.animation_speed:
			self.animation_timer = 0
			self.image_index = (self.image_index + 1) % len(self.images)
			self.current_image = self.images[self.image_index]
			self.rect.texture = self.current_image


		# 物理演算
		self.velocity += GRAVITY
		self.pos_y += self.velocity

		# 回転の処理（落下時は下向き、上昇時は上向きに）
		target_rotation = -30 if self.velocity > 0 else 30
		self.rotation = (self.rotation * 0.9) + (target_rotation * 0.1)  # 滑らかに回転

		# 衝突判定処理
		if self.check_sky_collision() or self.check_ground_collision() or self.check_pipe_collision(columns):
			return False

		# 描画の更新
		self.rect.pos = (self.pos_x, self.pos_y)
		return True

	def check_sky_collision(self):
		if self.pos_y + self.size_y >= Window.height:
			self.pos_y = Window.height - self.size_y
			self.velocity = 0
			print("Bird hit the sky!")
			return True
		return False

	def check_ground_collision(self):
		ground_y = Window.height * FLOOR_HEIGHT_RATIO
		if self.pos_y <= ground_y:
			self.pos_y = ground_y
			self.velocity = 0  # 地面に着いたら速度をリセット
			print("Bird hit the ground!")
			return True
		return False

	def check_pipe_collision(self, columns):
		# 鳥の座標情報
		bird_x, bird_y = self.pos_x, self.pos_y
		bird_width, bird_height = self.size_x, self.size_y

		for column in columns:

			# 上パイプの当たり判定
			top_x, top_y = column.top_pipe_rect.pos
			top_width, top_height = column.top_pipe_rect.size

			# 下パイプの当たり判定
			bottom_x, bottom_y = column.bottom_pipe_rect.pos
			bottom_width, bottom_height = column.bottom_pipe_rect.size

			# 衝突判定処理
			if (bird_x < top_x + top_width and bird_x + bird_width > top_x and
				bird_y < top_y + top_height and bird_y + bird_height > top_y):
				print("Bird hit the top pipe!")
				return True

			if (bird_x < bottom_x + bottom_width and bird_x + bird_width > bottom_x and
				bird_y < bottom_y + bottom_height and bird_y + bird_height > bottom_y):
				print("Bird hit the bottom pipe!")
				return True

		return False


	def flap(self):
		self.velocity = FLAP_POWER
		self.rotation = 20  # 少し上向きに
