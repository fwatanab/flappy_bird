from kivy.core.window import Window
from kivy.uix.widget import Widget
from objects.column import Column
from config import PIPE_SPAWN_INTERVAL

class ColumnManager(Widget):
	def __init__(self, texture, **kwargs):
		super(ColumnManager, self).__init__(**kwargs)
		self.texture = texture
		self.columns = []
		self.spawn_timer = 0  # 次のパイプ生成までのカウント

	def resize(self, *args):
		for column in self.columns:
			column.resize()

	def update(self, dt):
		# スポーンタイマーを更新
		self.spawn_timer += dt
		if self.spawn_timer >= PIPE_SPAWN_INTERVAL:
			# 新しいパイプを生成してリストに追加
			new_column = Column(self.texture)
			self.add_widget(new_column)
			self.columns.append(new_column)
			self.spawn_timer = 0  # タイマーをリセット

		# 各パイプを更新
		for column in self.columns:
			column.update(dt)

		# 画面外に出たパイプを削除
		self.columns = [col for col in self.columns if not col.is_out_of_screen()]

		# 不要なウィジェットも削除
		for col in self.children[:]:
			if col not in self.columns:
				self.remove_widget(col)
