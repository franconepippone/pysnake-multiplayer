# server side application module

import random

class tile:
	def __init__(self, x, y, t):
		self.x = x
		self.y = y
		self.t = t

	def update(self):
		self.t -= 1
		if self.t <= 0:
			return True
		else:
			return False


class environment:
	def __init__(self, tiles_x, tiles_y, snakes = [], world = None, Foods = False, repeat = False, tilesize = 51):
		self.dim = (-tiles_x, -tiles_y),(tiles_x, tiles_y)
		self.tiles_x = tiles_x
		self.tiles_y = tiles_y
		self.tilesize = tilesize
		self.scale = 1
		if world == None:
			self.world = []
		else:
			self.world = world

		self.snakes = list(snakes)
		self.repeat = repeat

		if Foods == False:
			self.foods = [food(0,0, self.dim).scatter(self) for _ in range(5)]
		else:
			self.foods = Foods

	def update(self):
		for snk in self.snakes:
			if snk.update(self):
				self.snakes.remove(snk)

	def addsnake(self, snake):
		self.snakes.append(snake)

	def rmsnake(self, snake):
		self.snakes.remove(snake)


class food:
	def __init__(self, x, y, spawn_area = ((-10,-10),(10,10)), scatter = True):
		self.x = x
		self.y = y
		self.rect = spawn_area
		self.color = (0,0,255)

	def scatter(self, env):
		while True:
			x = random.randint(env.dim[0][0]+1, env.dim[1][0]-1)
			y = random.randint(env.dim[0][1]+1, env.dim[1][1]-1)

			if [x,y] in env.world:
				continue
			for snk in env.snakes:
				for tile in snk.body:
					if tile.x == self.x and tile.y == self.y:
						continue
			break
		self.x, self.y = x, y
		return self

def getrandomcolor():
	return random.randint(0,255), random.randint(0,255), random.randint(0,255)

class snake:
	def __init__(self, x, y, lenght, color = 'r'):
		self.x = x
		self.y = y
		self.len = lenght
		self.body = [tile(x+i, y, lenght-i) for i in range(lenght)]
		self.rqstdir = 1
		self.dir = 1
		if color == 'r':
			self.color = getrandomcolor()

	def collide(self, snake):
		for tile in snake.body:
			if tile.x == self.x and tile.y == self.y:
				return True
		return False

	def worldcollide(self, world):
		if [self.x, self.y] in world:
			return True
		return False

	def changedir(self, newdir):
		self.rqstdir = newdir

	def reset(self, x, y, lenght):
		self.x = x
		self.y = y
		self.len = lenght
		self.body = [tile(x+i, y, lenght-i) for i in range(lenght)]
		self.rqstdir = 1
		self.dir = 1

	def update(self, env):
		# update heading
		if self.rqstdir == 0 and self.dir != 1:
			self.dir = self.rqstdir
		elif self.rqstdir == 1 and self.dir != 0:
			self.dir = self.rqstdir
		elif self.rqstdir == -1 and self.dir != 2:
			self.dir = self.rqstdir
		elif self.rqstdir == 2 and self.dir != -1:
			self.dir = self.rqstdir

		# updating position
		if self.dir == 0:
			self.x += 1
		elif self.dir == 1:
			self.x -= 1
		elif self.dir == -1:
			self.y -= 1
		elif self.dir == 2:
			self.y += 1

		# checking for collisions
		if not point_in_rect(self.x, self.y, env.dim):
			if env.repeat == False:
				return True
			elif env.repeat == True:
				if self.x < -env.tiles_x:
					self.x = env.tiles_x
				elif self.x > env.tiles_x:
					self.x = -env.tiles_x
				elif self.y < -env.tiles_y:
					self.y = env.tiles_y
				elif self.y > env.tiles_y:
					self.y = -env.tiles_y

		if self.worldcollide(env.world):
			return True

		for snk in env.snakes:
			if self.collide(snk):
				return True

		# check for food collision and creation/destruction of tiles
		for food in env.foods:
			if food.x == self.x and food.y == self.y:
				food.scatter(env)
				self.len += 1
		else:
			for piece in self.body:
				piece.update()
			for piece in self.body:
				if piece.t <= 0:
					self.body.remove(piece)

		self.body.append(tile(self.x, self.y, self.len))
		return False

def point_in_rect(x,y,rect):
	if (rect[0][0] <= x <= rect[1][0]) and (rect[0][1] <= y <= rect[1][1]):
		return True
	return False
