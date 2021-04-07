## Lenguajes
- [processing 3 (java)](https://processing.org/)
- [python 3](https://www.python.org)

## Librerias
- [selenium](https://pypi.org/project/selenium/)
- [pillow](https://pypi.org/project/Pillow/)
- [numpy](https://pypi.org/project/numpy/)

## Drivers
- [chromedriver](https://chromedriver.chromium.org)
  
**Es importante tener processing y chromedriver en las variables de entorno (PATH)**

## Run
```
python3 sl_maze.py
```

La salidade datos esta en data/out.txt

- El camino permitido es 1
- El camino no permitido es 0 (incluye buhos)
- La Posicion del jugador es 2
- La posicion de la meta es 3

## TODO
- [X] Iniciar el juego para la recoleccion de datos
- [X] Mapa permitido (camino)
- [X] Area no permitida del mapa
- [X] Posición del jugador
- [X] Posición de los búhos
- [X] Posición de la meta
- [ ] ~~Convertir imagen en grafo~~
- [X] Solucionar laberinto con imagen
- [X] Manipular agente


## Estructura del proyecto
<pre>
maze/
├─ maze.jpg ........ Imagen generada por sketch processing
├─ readme.md ....... 
├─ sl_maze.py ...... Programa de reconocimiento
├─ Car.py .......... Modelo del carro
├─ Agent.py ........ Agente para solucionar el laberinto
├─ data/ ........... 
│  ├─ data.json .... Estructura con coordenadas de los objetos en pantalla 
│  └─ out.txt ...... Matriz final sin compresion
└─ proc_img/ ....... 
   └─ proc_img.pde . Sketch de processing para la creacion de imagen
</pre>

