from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.clock import Clock
from objects.background import Background
from objects.floor import Floor
from objects.bird import Bird
from objects.column_manager import ColumnManager
from objects.score import Score
from config import FPS
from kivy.utils import platform

class Game(Screen):
	def __init__(self, app, **kwargs):
		super(Game, self).__init__(**kwargs)
		self.app = app
		self.clock_event = None
		self.game_running = False

		# オブジェクト生成
		self.background = None
		self.floor = None
		self.bird = None
		self.column_manager = None
		self.score = None

		# リサイズイベントのバインド
		Window.bind(on_resize=self.on_resize)

	def on_pre_enter(self, *args):
		#画面が表示される直前に呼ばれる
		print("Setting up game before entering...")
		Window.bind(on_key_down=self.on_key_down)
		self.restart_game()  # ここでゲームのセットアップ
		return super().on_pre_enter(*args)

	def on_pre_leave(self, *args):
		# 画面が離れる直前に呼ばれる
		print("Clearing game widgets before leaving...")
		Window.unbind(on_key_down=self.on_key_down)
		self.clear_widgets()
		if self.clock_event:
			Clock.unschedule(self.clock_event)
			self.clock_event = None
		self.game_running = False
		return super().on_pre_leave(*args)

	def on_resize(self, window, width, height):
		# ウィンドウがリサイズされたときの処理
		if not hasattr(self, 'game_running') or not self.game_running:
			return

		# 各オブジェクトのリサイズメソッドを呼び出す
		if hasattr(self, 'background') and self.background:
			self.background.resize()
		if hasattr(self, 'floor') and self.floor:
			self.floor.resize()
		if hasattr(self, 'bird') and self.bird:
			self.bird.resize()
		if hasattr(self, 'column_manager') and self.column_manager:
			self.column_manager.resize()
		if hasattr(self, 'score') and self.score:
			self.score.resize()

# 	def add_pause_button(self):
# 		# ポーズボタンを追加（特にモバイル向け）
# 		if platform in ("android", "ios"):
# 			from kivy.uix.button import Button
# 
# 			# 透明度の高いボタンを右上に配置
# 			self.pause_button = Button(
# 				text="II",
# 				size_hint=(None, None),
# 				size=(50, 50),
# 				pos=(Window.width - 60, Window.height - 60),
# 				background_color=(0.5, 0.5, 0.5, 0.7),
# 				color=(1, 1, 1, 1)
# 			)
# 			self.pause_button.bind(on_press=self.toggle_pause)
# 			self.add_widget(self.pause_button)
# 
# 	def toggle_pause(self, *args):
# 		# ゲームの一時停止/再開を切り替え
# 		self.paused = not self.paused
# 
# 		if self.paused:
# 			if self.clock_event:
# 				Clock.unschedule(self.clock_event)
# 				self.clock_event = None
# 		else:
# 			if not self.clock_event:
# 				self.clock_event = Clock.schedule_interval(self.update, 1.0 / FPS)

	def restart_game(self):
		self.clear_widgets()
		self.paused = False

		# オブジェクト生成
		self.background = Background(self.app.images["background"])
		self.floor = Floor(self.app.images["floor"])
		self.bird = Bird(self.app.images["bird"])
		self.column_manager = ColumnManager(self.app.images["pipe"])
		self.score = Score(self.app.number_images, self.app.sounds["point"])

		# 画面に追加
		self.add_widget(self.background)
		self.add_widget(self.floor)
		self.add_widget(self.bird)
		self.add_widget(self.column_manager)
		self.add_widget(self.score)

# 		# モバイル向けにポーズボタンを追加
# 		self.add_pause_button()

		# ゲーム状態を初期化
		self.game_running = True

		# 既に `Clock.schedule_interval()` が動いていた場合は解除
		if self.clock_event:
			Clock.unschedule(self.clock_event)
			self.clock_event = None

		# `Clock.schedule_interval()` で `update()` を定期実行
		self.clock_event = Clock.schedule_interval(self.update, 1.0 / FPS)

	def on_key_down(self, window, key, scancode, codepoint, modifiers):
		# スペースキー（キーコード32）が押された場合
		if key == 32:
			self.bird.flap()
			self.app.sounds["wing"].play()
# 		if key == 32:
# 			if self.paused:
# 				self.toggle_pause()
# 			else:
# 				self.bird.flap()
# 				self.app.sounds["wing"].play()
# 		# ESCキー（キーコード27）が押された場合
# 		elif key == 27:
# 			self.toggle_pause()

	def on_touch_down(self, touch):
# 		# ポーズボタンの処理はスーパークラスに任せる（Buttonウィジェットが処理）
# 		if self.pause_button and self.pause_button.collide_point(*touch.pos):
# 			return super().on_touch_down(touch)

		# 鳥を羽ばたかせる（一時停止中は除く）
		if not self.paused:
			self.bird.flap()
			self.app.sounds["wing"].play()
		return super().on_touch_down(touch)

	def update(self, dt):
		if not self.game_running:
			return

		# オブジェクトの状態を更新
		self.background.update(dt)
		self.floor.update(dt)
		self.column_manager.update(dt)
		# 鳥の更新（False ならゲームオーバー）
		if not self.bird.update(dt, self.column_manager.columns):
			self.game_over()
			return

		self.score.check_score_count(self.bird, self.column_manager.columns)

	def game_over(self):
		print("Game over! Switching back to menu...")
		self.app.sounds["hit"].play()
		self.game_running = False
		# スコアを保存するなどの処理をここに追加
		self.app.switch_screen("menu")
