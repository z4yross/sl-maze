import numpy as np
from math import pi, sin, cos

import matplotlib.pyplot as plt

class Agent:
	r = 5

	dirs_rev = np.array([pi / 2 + pi / 4, 0, -pi / 2 + -pi / 4])
	dirs = np.array([pi / 2, 0, -pi / 2])

	kill = False

	def __init__(self, x, y, dr, parent, objt, lvl = 0):
		self.x = x
		self.y = y
		self.dir = dr
		self.parent = parent
		self.objt = objt
		self.lvl = lvl

	def sensCard(self, maze):
		tetta = self.dir + self.dirs_rev

		res = []

		for i, t in enumerate(tetta):
			fY = int(self.y - 27 * sin(t))
			fX = int(self.x + 27 * cos(t))
			
			if fY < len(maze) and fX < len(maze[0]):
				# print(f'p: ({fX}, {fY}) = {maze[fY][fX]}')
				if maze[fY][fX] > 0:
					# print(f'v: ({fX}, {fY}) = {maze[fY][fX]}')
					res.append(self.dirs[i] + self.dir)
				
		return res


	def children(self, posb, maze):
		child = []

		if not self.kill:
			for p in posb:
				notIn = True
				i = 0
				while notIn:
					x = int(self.x + (self.r - i) * cos(p))
					y = int(self.y - (self.r - i) * sin(p))
					i += 1
					if y < len(maze) and x < len(maze[0]):
						if maze[y][x] > 0:
							# print(f'a: ({x}, {y}) = {maze[y][x]}')
							a = Agent(x, y, p, self, self.objt, lvl = self.lvl + 1)
							child.append(a)
							notIn = False
							break

			if self.checkFinish(maze):
				return True
				# self.move()		
		
		return child


	def checkFinish(self, maze):
		for x in range(self.x - 18, self.x + 19):
			for y in range(self.y - 18, self.y + 19):
				if maze[y][x] == self.objt:
					return True
				else:
					fY = int(y + 18 * 1.5 * sin(self.dir))
					fX = int(x - 18 * 1.5 * cos(self.dir))
					if fY < len(maze) and fX < len(maze[0]):
						maze[fY][fX] = 0

	def checkWall(self, maze):
		for x in range(self.x - 3, self.x + 5):
			for y in range(self.y - 3, self.y + 5):
				if maze[y][x] < 1:
					self.kill = True


	def move(self):
		self.x += int(self.r * cos(self.dir))
		self.y += int(self.r * sin(self.dir))

	def update(self, maze):
		self.checkWall(maze)
		maze[self.y][self.x] = 2
		return self.children(self.sensCard(maze), maze)