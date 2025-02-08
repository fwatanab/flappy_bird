import pygame
from assets import load_images, load_sounds, load_number_imaes
from config import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from screens.menu import Menu
from screens.game import Game
from objects.background import Background

class Game_manager:
	def __init__(self):
		# 初期化
		pygame.init()
		self.clock = pygame.time.Clock()  # Clockオブジェクトを作成
		self.running = True #ゲームの進行状況

		# 画面に描画
		self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
		pygame.display.set_caption("Flappy Bird")

		# 素材のロード
		self.images = load_images()
		self.sounds = load_sounds()
		self.number_images = load_number_imaes()

		# 初期画面をメニュー画面に設定
		self.current_screen = Menu(self)

	def switch_screen(self, new_screen):
		self.current_screen = new_screen

	def run(self):
		# ゲームのメインループ
		try:
			while self.running:
				self.dt = self.clock.tick(FPS)  # フレーム間隔を取得（ミリ秒単位）

				self.current_screen.handle_events()
				self.current_screen.update()
				self.current_screen.draw()
				pygame.display.update()

		# 例外処理(当たり判定処理)
		except Exception as e:
			print(e)  # デバッグ用メッセージ
			self.sounds["hit"].play()
			pygame.time.delay(1000)  # 1秒間待機させて音を反映
			self.running = False

		finally:
			# 終了処理
			pygame.quit()