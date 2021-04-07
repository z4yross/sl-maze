import numpy as np
from math import pi, sin, cos

import matplotlib.pyplot as plt

class Agent:
	dirs = np.array([pi / 2, -pi / 2])
	kill = False
	finish = False

	cln = 19

	def __init__(self, x, y, dr, parent, objt, im, fig, show, lvl = 0, cln = 19):
		self.x = int(x)
		self.y = int(y)
		self.dir = dr
		self.parent = parent
		self.objt = objt
		self.lvl = lvl

		self.im = im
		self.fig = fig
		self.show = show

		self.p = np.array([self.x, self.y] + (19 * np.array([-cos(self.dir), -sin(self.dir)])), dtype = int)
		self.origin = [x, y]


	def sensCard(self, maze):
		d = self.dir + self.dirs
		
		psb = []

		rep = False

		for t in d:
			x = int(np.rint(self.p[0] + 22 * cos(t)))
			y = int(np.rint(self.p[1] - 22 * sin(t)))
			
			if 0 < y < len(maze) and 0 < x < len(maze[0]):
				# print(f'n: ({x}, {y}) = {maze[y][x]}')
				if 5 > maze[y][x] > 0:
					psb.append(t)
					rep = True
		if rep:
			x = int(np.rint(self.x + 22 * cos(self.dir)))
			y = int(np.rint(self.y - 22 * sin(self.dir)))
			if 0 < y < len(maze) and 0 < x < len(maze[0]):
				# print(f'n: ({x}, {y}) = {maze[y][x]}')
				if 5 > maze[y][x] > 0:
					psb.append(self.dir)

		return psb


	def children(self, psb, maze):
		child = []

		for p in psb:
			child.append(Agent(self.x + 2 * cos(self.dir), self.y - 2 * sin(self.dir), p, self, self.objt, self.im, self.fig, self.show, lvl = self.lvl + 1))
		return child

	def checkFinish(self, maze):
		for x in range(self.x - 19, self.x + 19):
			for y in range(self.y - 19, self.y + 19):
				if maze[y][x] == self.objt:
					self.finish = True
				else:
					maze[y][x] = 6


	def move(self, maze):
		x = int(np.rint(self.x + 21 * cos(self.dir)))
		y = int(np.rint(self.y - 21 * sin(self.dir)))

		if 0 < y < len(maze) and 0 < x < len(maze[0]):
			# print(f'm: ({x}, {y}) = {maze[y][x]}')
			if maze[y][x] > 0:
				self.x += 2 * int(cos(self.dir))
				self.y -= 2 * int(sin(self.dir))
			else:
				self.kill = True

	def update(self, maze):

		if self.finish:
				return True

		while not self.kill:
			
			# print(f'p: ({self.p[0]}, {self.p[1]})\ncln: {self.cln <= 0}')
			if self.finish:
				return True


			self.move(maze)
			self.checkFinish(maze)

			psb = self.sensCard(maze)	

			if len(psb) and self.cln <= 0:
				# print(f"REP: {self.lvl}")
				return self.children(psb, maze)

			
			self.p = np.array([self.x, self.y] + (15 * np.array([-cos(self.dir), sin(self.dir)])), dtype = int)
			self.cln -= 2

			if self.show:
				self.im.set_data(maze)
				self.fig.canvas.draw()
				plt.pause(0.0001)

		return []
	


		
		
		