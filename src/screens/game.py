import pygame
from objects.background import Background
from objects.floor import Floor
from objects.bird import Bird
from objects.column_manager import Column_manager
from objects.score import Score

class Game:
	def __init__(self, manager):
		self.manager = manager

		# オブジェクト生成
		self.background = Background(self.manager.images["background"])
		self.floor = Floor(self.manager.images["floor"])
		self.bird = Bird(self.manager.images["bird"])
		self.column_manager = Column_manager(self.manager.images["pipe"])
		self.score = Score(self.manager.number_images, self.manager.sounds["point"])

	def handle_events(self):
		# イベント処理
		for event in pygame.event.get():
			if event.type == pygame.QUIT: # 閉じるボタンが押された場合
				self.running = False
			if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
				self.bird.flap()
				self.manager.sounds["wing"].play()
	
	def update(self):
		# オブジェクト更新
		self.background.update()
		self.column_manager.update(self.manager.dt)
		self.floor.update()
		self.bird.update(self.column_manager.columns)
		self.score.check_score_count(self.bird, self.column_manager.columns)

	def draw(self):
		# 描画
		self.background.draw(self.manager.screen)
		self.column_manager.draw(self.manager.screen)
		self.floor.draw(self.manager.screen)
		self.bird.draw(self.manager.screen)
		self.score.draw(self.manager.screen)
