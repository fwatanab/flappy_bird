import pygame
from config import SCROLL_SPEED, SCREEN_WIDTH, FLOOR_Y

class Floor:
	def __init__(self, image):
		self.image = image
		self.x_pos = 0

	def update(self):
		self.x_pos -= SCROLL_SPEED
		if self.x_pos <= -SCREEN_WIDTH:
			self.x_pos = 0

	def draw(self, screen):
		screen.blit(self.image, (self.x_pos, FLOOR_Y))
		screen.blit(self.image, (self.x_pos + SCREEN_WIDTH, FLOOR_Y))
