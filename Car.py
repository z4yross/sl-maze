import numpy as np
from math import pi, sin, cos, acos, asin, sqrt, radians, degrees
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains

import time

class Car:

	p = np.array([])
	actionChains = None

	# dirs = {
	# 	0   : 'd',	
	# 	90  : 'w',
	# 	180 : 'a',
	# 	270 : 's'
	# }

	dirs = {
		0   : Keys.ARROW_RIGHT,	
		90  : Keys.ARROW_UP,
		180 : Keys.ARROW_LEFT,
		270 : Keys.ARROW_DOWN
	}

	# dirs = {
	# 	0   : 'rt',	
	# 	90  : 'up',
	# 	180 : 'lf',
	# 	270 : 'dn'
	# }

	def __init__(self, x, y, route, driver):
		self.route = route
		self.p = np.array([x, y], dtype = int)
		self.r_pos = self.p
		self.driver = driver
		self.canvas = driver.find_element_by_id("animation_container")

		self.lvl = self.driver.execute_script('return exportRoot.currentFrame')
		

	def get_pos(self):
		self.r_pos = self.driver.execute_script('''
		let rs = exportRoot.children;
		let res;

		for(let i = 1; i < rs.length; i++){		
			if(rs[i].name){
				if(rs[i].name == 'personaje'){
					res = [rs[i].x, rs[i].y];
				}
			}
		}

		return res;
	''')

		return self.get_pos

	def move_to(self, p1, t):
		t1 = radians(t)
		clr = abs(p1[0] * cos(t) + p1[1] * sin(t))
		p_axis = abs(self.r_pos[0] * cos(t) + self.r_pos[1] * sin(t))

		dd = abs(p_axis - clr)
		mx_att = 30
		while not clr + 2 >  p_axis > clr - 2 and mx_att >= 0:
			if self.lvl is not self.driver.execute_script('return exportRoot.currentFrame'):
				break
			dt = 0
			dv = p1 - np.array(self.r_pos)

			if t is 0 or t is 180:
				temp = sqrt(dv[0] ** 2)
				dt = acos(dv[0] / temp)
			else:
				temp = sqrt(dv[1] ** 2)
				dt = -asin(dv[1] / temp)

			w = self.mp(dd, 0, 300, 400, 1000)
			self.move(int(degrees(dt)) % 360, int(w))

			self.get_pos()
			p_axis = abs(self.r_pos[0] * cos(t) + self.r_pos[1] * sin(t))
			dd = abs(p_axis - clr)
			mx_att -= 1

	
	def move(self, t, w):
		key = self.dirs[t]
		print(f'm:({t},{w})')

		# btn = self.btn_p[key]
		
		# self.actionChains.reset_actions()
		self.actionChains = ActionChains(self.driver)
		# self.actionChains.key_down(key, element = self.canvas).key_up(key, element = self.canvas).perform()
		# self.actionChains.move_to_element_with_offset(self.canvas, btn[0], btn[1]).click().perform()
		self.actionChains.send_keys_to_element(self.canvas, key * w).perform()
		
		
	def mp(self, value, start1, stop1, start2, stop2):
		return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

	def update(self):
		while len(self.route):
			action = self.route.pop()
			print(f'a: {action}')
			self.move_to(np.array(action[1], dtype = int), action[0])

