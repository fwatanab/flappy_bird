from kivy.uix.screenmanager import Screen
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.core.window import Window
from objects.background import Background
from objects.title import Title

class Menu(Screen):
	def __init__(self, app, **kwargs):
		super(Menu, self).__init__(**kwargs)
		print(f"Menu instance created: {self}")
		self.app = app
		self.images = app.images

		# 背景オブジェクトの生成
		self.background = Background(self.images["background"])
		self.title = Title(self.images["menu"]["title"])
		self.add_widget(self.background)
		self.add_widget(self.title)

	def on_pre_enter(self, *args):
		# Windowにバインド
		Window.bind(on_key_down=self.on_key_down)
		# メニュー中のみ、マウスリサイズを許可（ゲーム中は不可）
		self.app.begin_menu_resize()
		return super().on_pre_enter(*args)

	def on_pre_leave(self, *args):
		# アンバインド
		Window.unbind(on_key_down=self.on_key_down)
		return super().on_pre_leave(*args)

	def on_key_down(self, window, key, scancode, codepoint, modifiers):
		# スペースキー（キーコード32）が押された場合
		if key == 32:
			self.app.switch_screen("game")

	def on_touch_down(self, touch):
		# 画面がタッチされた場合
		self.app.switch_screen("game")
		return super().on_touch_down(touch)

	def update(self, dt):
		self.background.update(dt)
