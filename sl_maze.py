from selenium import webdriver
from selenium.webdriver.common.keys import Keys

from selenium.webdriver import ActionChains

import time
import os
import json

from PIL import Image
import numpy as np

import math
from Agent import Agent
from math import pi, sin, cos

import matplotlib.pyplot as plt

def esperar(canvas):
	res = input('Escriba 1 para resolver o 0 para salir: ')
	if res == '1':
		sensar(True, canvas)
	elif res == '0':
		exit
	else:
		esperar(canvas)

def sensar(gdr, canvas):
	entorno = procesar(leer())

	if gdr:
		guardar(entorno[0])

	actuar(entorno[0], entorno[1], entorno[2], canvas, 0)
	# actionChains.key_down(Keys.ARROW_DOWN, element = canvas).key_up(Keys.ARROW_DOWN, element = canvas).pause(0.1).perform()
	esperar(canvas)


def leer():
	objts = (driver.execute_script('''
		let rs = exportRoot.children;
		let res = {
			'obst' : []
		};

		for(let i = 1; i < rs.length; i++){		
			if(rs[i].name){
				console.log(rs[i].name);
				console.log(rs[i].name.substring(0, 5))
				if(rs[i].name == 'personaje'){
					res['player'] = [rs[i].x, rs[i].y];
				}
				if(rs[i].name.substring(0, 6) == 'puerta'){
					res['finish'] = [rs[i].x, rs[i].y];
				}
				else if(rs[i].name != null && rs[i].name.charAt(0) == "o"){
					res['obst'].push([rs[i].x, rs[i].y]);
				}
				else if(rs[i].name.substring(0, 5) == 'pared'){
					res['wall'] = rs[i].children[0].graphics._instructions
				}
			}
		}

		return res;
	'''))

	return objts

def mp(value, start1, stop1, start2, stop2):
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))

def procesar(objts):
	prc_walls = []
	i = -1
	temp_cdr = []
	for pr in objts['wall']:
		if 'bitmap' not in pr.keys():
			if 'x' in pr.keys() and 'y' in pr.keys():
				temp_cdr.append([pr['x'], pr['y']])
			else:
				if i >= 0:
					prc_walls.append({'coords': temp_cdr, 'color': i == 1})
					temp_cdr = []
				i += 1
	objts['wall'] = prc_walls

	with open('data/data.json', 'w') as fp:
		json.dump(objts, fp)

	os.system("processing-java --sketch=%cd%/proc_img --run")

	im = Image.open('maze.png')
	gray = im.convert('L')
	bw = np.asarray(gray).copy()
	bw[bw < 128] = 0 
	bw[bw >= 128] = 255 
	im = Image.fromarray(bw)
	im = im.convert("RGBA")

	pixdata = im.load()

	width, height = im.size
	for y in range(height):
		for x in range(width):
			if pixdata[x, y] == (255, 255, 255, 255):
				pixdata[x, y] = (255, 255, 255, 0)

	pix = np.array(im)

	fn = np.zeros(shape=(len(pix),len(pix[0])))


	for i, x in enumerate(pix):
		for j, y in enumerate(x):
			fn[i][j] = 0 if np.sum(y) > 255*3/2 else 1

	objetos = fn
	coords_plyr = objts['player']
	coords_fnsh = objts['finish']
	objetos[int(coords_plyr[1])][int(coords_plyr[0])] = 2

	fnX = int(coords_fnsh[0])
	fnY = int(coords_fnsh[1])

	for x in range(fnX - 9, fnX + 9):
		for y in range(fnY - 9, fnY + 9):
			objetos[y][x] = 3

	return [objetos, coords_plyr, 3]

def guardar(objetos):
	np.savetxt("data/out.txt", objetos, fmt="%d", delimiter='')



def actuar(maze, inicio, objetivo, canvas, dr):

	fig,ax = plt.subplots(1,1)
	im = ax.imshow(maze)
	fig.show()

	agentes = [Agent(int(inicio[0]), int(inicio[1]), -pi/2, None, objetivo)]
	res = None
	fn = True

	i = 0
	while fn:
		tmp = []
		for agente in agentes:
			x = agente.update(maze)

			# print(f'c: ({agente.x}, {agente.y})\nlvl: {i}\nagentes={x}')
			
			if type(x) is bool: 
				res = agente
				fn = False
				# print(f'c: ({agente.x}, {agente.y})\nlvl: {i}\nagentes={x}')
				break
			else:
				tmp.extend(x)



		
		im.set_data(maze)
		fig.canvas.draw()
		plt.pause(1)

		i += 1
		agentes = tmp
		if not len(agentes):
			break


	if res is None:
		actuar(maze, inicio, objetivo, canvas, dr + pi/2)
		# exit()

	else:
		print('solving')
		solve(traceback(res), canvas)

def traceback(last):
	sz = 950
	actns_mp = {
		0   : Keys.ARROW_RIGHT,
		90  : Keys.ARROW_UP,
		180 : Keys.ARROW_LEFT,
		270 : Keys.ARROW_DOWN
	}

	actns_mp = {
		0   : 'd' * sz,
		90  : 'w' * sz,
		180 : 'a' * sz,
		270 : 's' * sz
	}

	actions = []
	current = last
	while current.parent is not None:
		dr = int(math.degrees(current.dir) % 360)

		actions.append(actns_mp[dr])
		current = current.parent
	return actions

def solve(actions, canvas):
	actionChains.move_to_element(canvas).click(canvas)
	while len(actions) > 0:
		action = actions.pop()
		# print(action)
		# actionChains.key_down(action, element = canvas).key_up(action, element = canvas).pause(0.1)

		actionChains.send_keys_to_element(canvas, action).pause(0.1)
	actionChains.perform()
	# print('performing')






options = webdriver.ChromeOptions()
options.add_argument("--log-level=OFF")
options.add_argument("--log-level=3")
options.add_argument("--log-level=0")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


chromedriver = "C:/chromedriver/chromedriver.exe"
# driver = webdriver.Chrome(executable_path=r'C:/chromedriver/chromedriver.exe')
driver = webdriver.Chrome(options=options)
actionChains = ActionChains(driver)

driver.get('https://www.juegosinfantilespum.com/laberintos-online/12-auto-buhos.php')

# play_coords = (float(driver.execute_script("return exportRoot.children[3].x")), float(driver.execute_script("return exportRoot.children[3].y")))

canvas = driver.find_element_by_id("animation_container")

# time.sleep(1)



esperar(canvas)
