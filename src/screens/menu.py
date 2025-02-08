import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FLOOR_Y
from screens.game import Game

class Menu:
	def __init__(self, manager):
		self.manager = manager

	def handle_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				self.manager.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.manager.switch_screen(Game(self.manager))

	def update(self):
		pass

	def draw(self):
		# 背景を描画
		self.manager.screen.blit(self.manager.images["background"], (0, 0))

		# タイトル画像を描画
		title_image = self.manager.images["menu"]["title"]
		# 画面の上から1/4に描画位置を指定 （画像の幅・高さの半分を引く）
		title_x = SCREEN_WIDTH // 2 - title_image.get_width() // 2
		title_y = SCREEN_HEIGHT // 4 - title_image.get_height() // 2
		self.manager.screen.blit(title_image, (title_x, title_y))

		# アイコン画像を描画
		icon_image = pygame.transform.rotate(self.manager.images["menu"]["icon"], 30)
		icon_x = SCREEN_WIDTH // 2 - icon_image.get_width() // 2
		icon_y = SCREEN_HEIGHT // 2 - icon_image.get_height() // 2
		self.manager.screen.blit(icon_image, (icon_x, icon_y))

		# 地面を描画
		self.manager.screen.blit(self.manager.images["floor"], (0, FLOOR_Y))
		