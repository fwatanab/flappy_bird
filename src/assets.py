from kivy.core.image import Image as CoreImage
from kivy.core.audio import SoundLoader

def load_images():
	return {
		"menu": {
			"title": CoreImage("assets/images/title.png").texture,
			"start": CoreImage("assets/images/start_menu.png").texture,
			"icon": CoreImage("assets/images/menu_icon.png").texture,
		},
		"background": CoreImage("assets/images/background.png").texture,
		"floor": CoreImage("assets/images/floor.png").texture,
		"bird": [
			CoreImage("assets/images/redbird-downflap.png").texture,
			CoreImage("assets/images/redbird-midflap.png").texture,
			CoreImage("assets/images/redbird-upflap.png").texture,
		],
		"pipe": CoreImage("assets/images/pipe-green.png").texture,
		"gameover": CoreImage("assets/images/gameover.png").texture,
	}

def load_sounds():
	return {
		"hit": SoundLoader.load("assets/sounds/hit.wav"),
		"point": SoundLoader.load("assets/sounds/point.wav"),
		"wing": SoundLoader.load("assets/sounds/wing.wav"),
	}

def load_number_images():
	return [
		CoreImage("assets/images/0.png").texture,
		CoreImage("assets/images/1.png").texture,
		CoreImage("assets/images/2.png").texture,
		CoreImage("assets/images/3.png").texture,
		CoreImage("assets/images/4.png").texture,
		CoreImage("assets/images/5.png").texture,
		CoreImage("assets/images/6.png").texture,
		CoreImage("assets/images/7.png").texture,
		CoreImage("assets/images/8.png").texture,
		CoreImage("assets/images/9.png").texture,
	]
