import pygame
from objects.column import Column
from config import PIPE_SPAWN_INTERVAL, SCREEN_WIDTH

class Column_manager:
	def __init__(self, image):
		self.image = image
		self.columns = []
		self.spawn_timer = 0 # 次のパイプ生成までのカウント

	def update(self, dt):
		# スポーンタイマーを更新
		self.spawn_timer += dt
		if self.spawn_timer >= PIPE_SPAWN_INTERVAL:
			# パイプを生成し、リストに追加
			new_column = Column(self.image, SCREEN_WIDTH + 20)
			self.columns.append(new_column)
			self.spawn_timer = 0 # タイマーをリセット

		# 各パイプの更新とスクロール
		for column in self.columns:
			column.update()

		# 画面外に出たパイプを削除
		self.columns = [col for col in self.columns if col.top_rect.right > 0]
	
	def draw(self, screen):
		for column in self.columns:
			column.draw(screen)
