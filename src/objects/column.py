import pygame
import random
from config import SCROLL_SPEED, PIPE_GAP, PIPE_MIN, PIPE_SPAWN_INTERVAL, FLOOR_Y, SCREEN_HEIGHT

class Column:
	def __init__(self, image, x_pos):
		# パイプの配置範囲を定義
		top_limit = PIPE_MIN # 上パイプの最小高さ
		bottom_limit = FLOOR_Y - PIPE_GAP - PIPE_MIN # 下パイプが隙間を考慮した範囲

		# 上パイプのY座標をランダムに設定
		top_pipe_y = random.randint(top_limit, bottom_limit)
		# 上パイプの下端を基準に下パイプを配置
		bottom_pipe_y = top_pipe_y + PIPE_GAP

		self.image = image
		self.image_rotated = pygame.transform.rotate(self.image, 180)  # 180度回転

		self.top_rect = self.image.get_rect(midbottom=(x_pos, top_pipe_y))
		self.bottom_rect = self.image.get_rect(midtop=(x_pos, bottom_pipe_y))

		self.passed = False # パイプの通過判定

	def update(self):
		self.top_rect.x -= SCROLL_SPEED
		self.bottom_rect.x -= SCROLL_SPEED

	def draw(self, screen):
		screen.blit(self.image_rotated, self.top_rect)
		screen.blit(self.image, self.bottom_rect)
