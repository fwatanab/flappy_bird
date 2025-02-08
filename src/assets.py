import pygame
import os

def load_images():
	images = {
		"menu": {
			"title": pygame.image.load("assets/images/title.png"),
			"start": pygame.image.load("assets/images/start_menu.png"),
			"icon": pygame.image.load("assets/images/menu_icon.png"),
		},
		"background": pygame.image.load("assets/images/background.png"),
		"floor": pygame.image.load("assets/images/floor.png"),
		"bird": [
			pygame.image.load("assets/images/redbird-downflap.png"),
			pygame.image.load("assets/images/redbird-midflap.png"),
			pygame.image.load("assets/images/redbird-upflap.png")
		],
		"pipe": pygame.image.load("assets/images/pipe-green.png"),
		"gameover": pygame.image.load("assets/images/gameover.png"),
	}
	return images

def load_sounds():
	sounds = {
		"hit": pygame.mixer.Sound("assets/sounds/hit.wav"),
		"point": pygame.mixer.Sound("assets/sounds/point.wav"),
		"wing": pygame.mixer.Sound("assets/sounds/wing.wav"),
	}
	return sounds

def load_number_imaes():
	number_images = [
		pygame.image.load("assets/images/0.png"),
		pygame.image.load("assets/images/1.png"),
		pygame.image.load("assets/images/2.png"),
		pygame.image.load("assets/images/3.png"),
		pygame.image.load("assets/images/4.png"),
		pygame.image.load("assets/images/5.png"),
		pygame.image.load("assets/images/6.png"),
		pygame.image.load("assets/images/7.png"),
		pygame.image.load("assets/images/8.png"),
		pygame.image.load("assets/images/9.png"),
	]
	return number_images