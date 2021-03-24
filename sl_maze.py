from selenium import webdriver
# from selenium.webdriver import ActionChains

import time
import os
import json

from PIL import Image
import numpy as np

options = webdriver.ChromeOptions()
options.add_argument("--log-level=OFF")
options.add_argument("--log-level=3")
options.add_argument("--log-level=0")
options.add_experimental_option('excludeSwitches', ['enable-logging'])


chromedriver = "C:/chromedriver/chromedriver.exe"
# driver = webdriver.Chrome(executable_path=r'C:/chromedriver/chromedriver.exe')
driver = webdriver.Chrome(options=options)

driver.get('https://www.juegosinfantilespum.com/laberintos-online/12-auto-buhos.php')

# time.sleep(5)
# play_coords = (float(driver.execute_script("return exportRoot.children[3].x")), float(driver.execute_script("return exportRoot.children[3].y")))

# canvas = driver.find_element_by_id("canvas")
# actionChains.move_to_element(canvas).click(canvas).perform()

# time.sleep(1)


def esperar():
	res = input('escriba 1 para sensar o 0 para salir: ')
	if res == '1':
		sensar(True)
	elif res == '0':
		exit
	else:
		esperar()

def sensar(gdr):
	entorno = procesar(leer())
	print(entorno)
	if gdr:
		guardar(entorno)

	esperar()


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
	print(len(fn),len(fn[0]))

	for i, x in enumerate(pix):
		for j, y in enumerate(x):
			fn[i][j] = 0 if np.sum(y) > 255*3/2 else 1

	objetos = fn
	coords_plyr = objts['player']
	coords_fnsh = objts['finish']
	objetos[int(coords_plyr[1])][int(coords_plyr[0])] = 2
	objetos[int(coords_fnsh[1])][int(coords_fnsh[0])] = 3


	return objetos

def guardar(objetos):
	np.savetxt("data/out.txt", objetos, fmt="%d")


esperar()
