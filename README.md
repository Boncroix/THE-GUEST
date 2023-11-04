# the-Guest
Proyecto final bootcamp: Aprender a programar desde cero (Pygame The-Guest)

## Dependencias necesarias
- Para desarrolladores requirements.dev.txt 
- Para el resto requirements.txt

### Instalación
1. Clona o descarga este repositorio.
2. Crea un entorno virtual
3. Instala las dependencias con `pip install -r requirements.txt` o `pip install -r requirements.dev.txt`

## Uso 
Inicia el juego ejecutando `main.py`: `python main.py` o `python3 main.py`

## Ajustes pricipales del juego
En el archivo `init.py` se encuentran los ajustes principales del juego
- FPS = Frames por segundo del juego.
- DIFICULTAD_INI = Dificultad en la que comienza la partida.
- NIVEL_INI = Nivel en el que comienza la partida.
- VIDAS_INI = Vidas con las que comienza la partida.
- TIEMPO_NIVEL = Tiempo de permanencia para subir de nivel
- PUNTOS_POR_OBSTACULO = Cantidad de puntos que suman cada vez que se sortea un obstáculo
- DISPAROS_POR_NIVEL = Disparos habilitados por nivel (Solo disponible desde el nivel 6)

## Recomendaciones
- No es recomendable cambiar los ajustes del juego.
- La resolución recomendada es de 1200 x 800, aunque el juego se adapta a otro tipo de resoluciones (No a todas)

# Clases del juego
## TheGues
- Se encuentra en el archivo `game.py` es la Clase principal del juego y es la encargada de instanciar y gestionar las escenas junto con la música de cada escena, en ella también instaciamos la Clase Marcador, ya que con él compartimos datos entre escenas.

## Escenas
### Escena:
- Se encuentra en el archivo `sc_escena.py` Clase que se hereda en todas las escenas, en ella se crean atributos y métodos que se utilizan en varias escenas.
#### Métodos
1. `pintar_texto` con este método podemos pintar texto en cualquiera de las escenas simplemente indicando el mensaje a mostrar, la tipografía que vamos a utilizar, posx y posy donde queremos pintar el texto, la alineación del texto ('centro', 'derecha', ''), el color del texto y por último True o False si queremos pintar el fondo para que se vea solo el fondo con el texto proporcionado.

2. `comprobar_sonido` en el siguiente método comprobamos el sonido a lo largo de todo el juego y recogemos si el usuario lo quiere desactivar.  (para desactivar utilizar la tecla TAB)

3. `ton_toff` temporizador configurado para activar y desactivar una salida durante un periodo de tiempo.

4. `ton` temporizador con retardo para la conexión.

5. `toff` temporizador con retardo para la desconexión.

### Portada:
- Se encuentra en el archivo `sc_portada.py`.
- Al instanciar desde game pasamos si el sonido está activo.
- Escena inicial del juego, en ella se muestra el título del juego, las indicaciones para interactuar y la historia, entre las indicaciones pulsando la tecla i se muestran las instrucciones, sería recomendable leerlas antes de jugar.
- Intercambia la visualización con récords cada cierto tiempo para el cambio de escena se utilizan eventos de usuario
        
### Partida
- Se encuentra en el archivo `sc_partida.py`.
- Al instanciar desde game pasamos si el sonido está activo y el marcador.
- Escena principal del juego, es la encargada de gestionar la lógica del juego, en el bucle principal recojo los eventos y realizo las acciones que no tienen condiciones, el método `gestion_bucle` es el responsable de cuando y por qué deben de ocurrir las cosas, diría que es el método más importante de la Clase.
- Para realizar el cambio de escenas se han utilizado eventos de usuario

### Récords
- Se encuentra en el archivo `sc_records.py`.
- Al instanciar desde game pasamos si el sonido está activo y el marcador.
- Escena que se ejecuta al finalizar el juego, aunque también la llamamos al inicio para mostrar récord mientras la escena portada está esperando que el usuario interactúe, al igual que en partida en el bucle principal recogemos los eventos y realizamos las acciones que no tienen ninguna condición, el método `gestion_bucle` es el encargado de saber si hemos entrado en la lista de récords o no.
- Intercambia la visualización con portada cada cierto tiempo para el cambio de escena se utilizan eventos de usuario

## dbmanager
## Entidades
### Nave
### Nave1
### Proyectil
### Obstaculo
### IndicadorVida
### IndicadorDisparo
### Planeta
### Marcador
##game


