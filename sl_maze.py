from selenium import webdriver
from selenium.webdriver import ActionChains
import time
import os
import json

chromedriver = "C:/chromedriver/chromedriver.exe"
driver = webdriver.Chrome(executable_path=r'C:/chromedriver/chromedriver.exe')
actionChains = ActionChains(driver)

driver.get('https://www.juegosinfantilespum.com/laberintos-online/12-auto-buhos.php')

time.sleep(5)
play_coords = (float(driver.execute_script("return exportRoot.children[3].x")), float(driver.execute_script("return exportRoot.children[3].y")))

canvas = driver.find_element_by_id("canvas")
actionChains.move_to_element(canvas).click(canvas).perform()

time.sleep(1)
objts = (driver.execute_script('''
	let rs = exportRoot.children;
	let res = {
		'obst' : []
	};

	for(let i = 1; i < rs.length; i++){
		console.log(rs[i].name);
		if(rs[i].name == 'personaje'){
			res['player'] = [rs[i].x, rs[i].y];
		}
        if(rs[i].name == 'puerta'){
			res['finish'] = [rs[i].x, rs[i].y];
		}
		else if(rs[i].name != null && rs[i].name.charAt(0) == "o"){
 			res['obst'].push([rs[i].x, rs[i].y]);
		}
		else if(rs[i].name == 'pared'){
 			res['wall'] = rs[i].children[0].graphics._instructions
		}
	}

	return res;
'''))

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

from PIL import Image
import numpy as np

im = Image.open('maze.jpg')
pix = np.array(im).T[0]
pix = pix.T

fn = np.zeros(shape=(len(pix),len(pix[0])))
print(len(fn),len(fn[0]))

for i, x in enumerate(pix):
    for j, y in enumerate(x):
        fn[i][j] = 1 if y > 255/2 else 0

unique, count = np.unique(fn, return_counts = True) 

objetos = fn
coords_plyr = objts['player']
coords_fnsh = objts['finish']
objetos[int(coords_plyr[1])][int(coords_plyr[0])] = 2
objetos[int(coords_fnsh[1])][int(coords_fnsh[0])] = 3

objetos
np.savetxt("data/out.txt", objetos, fmt="%d")

exit