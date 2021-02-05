# client side application module

class tile:
	def __init__(self, x, y, t):
		self.x = x
		self.y = y
		self.t = t

class environment:
	def __init__(self, env):
		self.world = env.world
		self.snakes = env.snakes
		self.foods = env.foods
		self.tilesize = env.tilesize
		self.scale = env.scale

	def storenew(self, new):
		self.snakes = new[0]
		self.foods = new[1]


class food:
	def __init__(self, food):
		self.x = food.x
		self.y = food.y
		self.color = food.color

class snake:
	def __init__(self, snk):
		self.x = snk.x
		self.y = snk.y
		self.body = snk.body
		self.color = snk.color
