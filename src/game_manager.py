from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.core.window import Window
from kivy.utils import platform
from kivy.uix.image import Image
from kivy.uix.widget import Widget
from assets import load_images, load_sounds, load_number_images
from screens.menu import Menu
from screens.game import Game
from config import BASE_WIDTH, BASE_HEIGHT, ASPECT_RATIO, FULLSCREEN, DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT

class GameManager(App):
	def build(self):
		# 再入防止用フラグ & 直前サイズ
		self._resizing = False
		self._prev_w, self._prev_h = Window.size
		# メニュー時のみマウスリサイズ許可
		self._allow_mouse_resize = False
		# 画面（フルスクリーン）上限。system_size が無い環境は現在サイズを使う
		self._screen_w, self._screen_h = (getattr(Window, "system_size", None) or Window.size)
		self._screen_w, self._screen_h = int(self._screen_w), int(self._screen_h)

		# ウィンドウサイズの設定
		if platform in ("android", "ios"):
			# モバイルでは常にフルスクリーンに設定
			Window.fullscreen = True
		else:
			# デスクトップはウィンドウモード + スマホ相当の初期サイズ
			Window.fullscreen = False
			# 最小サイズは比率に合わせて両辺を設定（9:16）
			min_w = 240
			min_h = int(min_w / ASPECT_RATIO)  # 例: 240 / 0.5625 = 426
			Window.minimum_width = min_w
			Window.minimum_height = min_h
			# 初期サイズを 9:16（スマホ相当）に設定
			Window.size = (DEFAULT_WINDOW_WIDTH, DEFAULT_WINDOW_HEIGHT)

		# 縦横比を保持（PC のみ）: size イベントで処理
		if platform not in ("android", "ios"):
			Window.bind(size=self._guard_and_keep_ratio)

		# 設定値を使用
		self.base_width = BASE_WIDTH
		self.base_height = BASE_HEIGHT
		self.aspect_ratio = ASPECT_RATIO

		# リソースロード
		self.images = load_images()
		self.sounds = load_sounds()
		self.number_images = load_number_images()

		# 画面マネージャー作成
		self.screen_manager = ScreenManager()

		# 各画面を追加
		self.screen_manager.add_widget(Menu(app=self, name="menu"))
		self.screen_manager.add_widget(Game(app=self, name="game"))

		# 初期画面設定
		self.screen_manager.current = "menu"

		return self.screen_manager

	def _guard_and_keep_ratio(self, instance, size):
		"""マウスのリサイズ方向に合わせてもう片方だけを補正し、拡大暴走を防ぐ。"""
		if platform in ("android", "ios"):
			return
		if self._resizing:
			return

		# メニュー以外では、外部（マウス）リサイズを拒否して元に戻す
		if self.screen_manager.current != "menu" or not self._allow_mouse_resize:
			if tuple(size) != (self._prev_w, self._prev_h):
				self._resizing = True
				try:
					Window.size = (self._prev_w, self._prev_h)
				finally:
					self._resizing = False
			return

		w, h = map(int, size)
		if w <= 0 or h <= 0:
			return

		# スクリーン上限でクランプ
		max_w, max_h = self._screen_w, self._screen_h
		w = min(w, max_w)
		h = min(h, max_h)

		target = float(self.aspect_ratio)  # w/h
		cur = w / float(h)
		if abs(cur - target) < 0.001:
			# ほぼ目標比率なら何もしない
			self._prev_w, self._prev_h = w, h
			return

		# どちらをユーザーが主に動かしたかを推定
		dw = abs(w - self._prev_w)
		dh = abs(h - self._prev_h)

		new_w, new_h = w, h
		if dw >= dh:
			# 幅が動いた → 高さを幅に合わせて補正（高さを増減）
			new_h = max(Window.minimum_height, int(round(w / target)))
		else:
			# 高さが動いた → 幅を高さに合わせて補正（幅を増減）
			new_w = max(Window.minimum_width, int(round(h * target)))

		# もう一度上限でクランプ（比率調整で溢れた場合）
		new_w = min(new_w, max_w)
		new_h = min(new_h, max_h)

		# 再入防止しつつサイズ再設定
		if new_w != w or new_h != h:
			self._resizing = True
			try:
				Window.size = (new_w, new_h)
			finally:
				self._resizing = False
		# 直前サイズを更新
		self._prev_w, self._prev_h = Window.size

	def switch_screen(self, new_screen_name):
		self.screen_manager.current = new_screen_name

	# ===== メニュー用 API（ボタン等から呼ぶ）=====
	def begin_menu_resize(self):
		"""メニューでサイズ調整を始める前に呼ぶ（マウス操作許可）"""
		self._allow_mouse_resize = True

	def end_menu_resize(self):
		"""メニューでサイズ調整を終えたら呼ぶ（誤操作防止のため無効化）"""
		self._allow_mouse_resize = False

	def resize_to_preset(self, mode: str):
		"""'phone' / 'tablet' / 'desktop' / 'max' に合わせて一発リサイズ"""
		target = float(self.aspect_ratio)

		# 代表的な論理解像度。必要ならここを好みで調整
		presets = {
			"phone":   (360, 640),
			"tablet":  (540, 960),
			"desktop": (720, 1280),
		}

		if mode == "max":
			W, H = self._screen_w, self._screen_h
			best_w = int(H * target)
			best_h = H
			if best_w > W:
				best_w = W
				best_h = int(W / target)
			w, h = best_w, best_h
		else:
			w, h = presets.get(mode, presets["phone"])

		# 比率に丸め（安全策）
		h = int(round(w / target))
		# 上限・下限でクランプ
		w = max(Window.minimum_width, min(w, self._screen_w))
		h = max(Window.minimum_height, min(h, self._screen_h))
		self._resizing = True

		try:
			Window.size = (w, h)
		finally:
			self._resizing = False

		self._prev_w, self._prev_h = Window.size

