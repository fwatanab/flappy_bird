import pygame
from config import SCREEN_WIDTH
from objects.bird import Bird
from objects.column_manager import Column_manager

class Score:
	def __init__(self, images, sound):
		self.images = images # 0～9の画像を格納した辞書
		self.count = 0
		self.sound = sound

	def check_score_count(self, bird, columns):
		for column in columns:
			if not column.passed and bird.rect.x > column.top_rect.x:
				column.passed = True # パイプを通過済みに設定
				self.count += 1
				self.sound.play()
			
	def draw(self, screen):
		# スコアの描画（各桁ごとに画像を描画）
		score_str = str(self.count)
		total_width = len(score_str) * self.images[0].get_width() + (len(score_str) - 1) * 5

		# 画面中央に描画開始位置を設定
		x_offset = (SCREEN_WIDTH - total_width) / 2
		for char in score_str:
			digit = int(char)  # 文字列を整数に変換
			screen.blit(self.images[digit], (x_offset, 5))  # Y座標は 50px 上に設定
			x_offset += self.images[digit].get_width() + 5  # 次の桁に移動
