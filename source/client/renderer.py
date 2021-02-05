import pygame, os
import time
import json
import math as m

pygame.init()


with open('configs.json') as f:
	cfgs = json.load(f)
print("Configurazioni caricate.")

# init pygame and window
WIDTH, HEIGHT = cfgs["width"], cfgs["height"]
OFFW, OFFH = WIDTH//2, HEIGHT//2

WHITE, BLACK = (255,255,255), (0,0,0)

RECT_WIDTH = 0

def togglefullscreen():
	pygame.display.toggle_fullscreen()

def init():
	global schermo

	os.environ['SDL_VIDEO_CENTERED'] = '1'

	if cfgs["fullscreen"]:
		schermo = pygame.display.set_mode((WIDTH, HEIGHT),pygame.FULLSCREEN)
	else:
		schermo = pygame.display.set_mode((WIDTH, HEIGHT))

	pygame.display.set_caption('Snake')

	schermo.fill(WHITE)


def update(background = BLACK):
	pygame.display.update()
	schermo.fill(background)


def render_scene(scene):
	if scene.foods != []:
		render_food(scene.foods, scene.tilesize, scene.scale)
	for snk in scene.snakes:
		render_snake(snk, scene.tilesize, scene.scale)

	render_world(scene.world, scene.tilesize, scene.scale)

def render_snake(snake, tilesize, scale):
	for tile in snake.body:
		pygame.draw.rect(schermo, snake.color, (tile.x * tilesize * scale + OFFW, -tile.y * tilesize * scale + OFFH, tilesize * scale, tilesize * scale), RECT_WIDTH)
		#pygame.draw.circle(schermo, snake.color, (int(tile.x * tilesize) + OFFW, -int(tile.y * tilesize) + OFFH), tilesize//2)

def render_food(foods, tilesize, scale):
	#pygame.draw.circle(schermo, (0,255,0), (int(food.x * tilesize) + OFFW, -int(food.y * tilesize) + OFFH), tilesize//2)
	for food in foods:
		pygame.draw.rect(schermo, (0,255,0), (food.x * tilesize * scale + OFFW, -food.y * tilesize * scale + OFFH, tilesize * scale, tilesize * scale), RECT_WIDTH)

def render_world(world, tilesize, scale):
	for coords in world:
		pygame.draw.rect(schermo, (255,255,255), (coords[0] * tilesize * scale + OFFW, -coords[1] * tilesize * scale + OFFH, tilesize * scale, tilesize * scale), RECT_WIDTH)
