import pygame
from config import BIRD_START_POS, GRAVITY, FLAP_POWER, FLOOR_Y
from objects.column_manager import Column_manager

class Bird:
	def __init__(self, images):
		self.images = images
		self.image_index = 0
		self.rect = self.images[0].get_rect(center=BIRD_START_POS)
		self.velocity= 0
	
	def update(self, columns):
		self.velocity += GRAVITY
		self.rect.y += self.velocity
		self.image_index = (self.image_index + 1) % len(self.images)

		# 当たり判定処理
		self.check_sky_collision()
		self.check_ground_collision()
		self.check_pipe_collision(columns)

	def check_sky_collision(self):
		# 空との衝突判定
		if self.rect.top <= 0:
			self.rect.top = 0
			self.velocity = 0
			raise Exception("Bird hit the sky!")

	def check_ground_collision(self):
		# 地面との衝突判定
		if self.rect.bottom >= FLOOR_Y:
			self.rect.bottom = FLOOR_Y
			self.velocity = 0  # 地面に着いたら速度をリセット
			raise Exception("Bird hit the ground!")

	def check_pipe_collision(self, columns):
		# パイプとの衝突判定
		for column in columns:
			if self.rect.colliderect(column.top_rect) or self.rect.colliderect(column.bottom_rect):
				raise Exception("Bird collided with a pipe!")

	def flap(self):
		self.velocity = FLAP_POWER

	def draw(self, screen):
		screen.blit(self.images[self.image_index], self.rect)
