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
- Intercambia la visualización con récords cada cierto tiempo, para el cambio de escena se utilizan eventos de usuario
        
### Partida
- Se encuentra en el archivo `sc_partida.py`.
- Al instanciar desde game pasamos si el sonido está activo y el marcador.
- Escena principal del juego, es la encargada de gestionar la lógica del juego, en el bucle principal recojo los eventos y realizo las acciones que no tienen condiciones, el método `gestion_bucle` es el responsable de cuando y por qué deben de ocurrir las cosas, diría que es el método más importante de la Clase.
- Para realizar el cambio de escenas se han utilizado eventos de usuario

### Récords
- Se encuentra en el archivo `sc_records.py`.
- Al instanciar desde game pasamos si el sonido está activo y el marcador.
- Escena que se ejecuta al finalizar el juego, aunque también la llamamos al inicio para mostrar récord mientras la escena portada está esperando que el usuario interactúe, al igual que en partida en el bucle principal recogemos los eventos y realizamos las acciones que no tienen ninguna condición, el método `gestion_bucle` es el encargado de saber si hemos entrado en la lista de récords o no. En records también nos encargamos de realizar consultas ha la base de datos, para leer los records, escribir nuevo record y borrar el de menos relevancia. 
- Intercambia la visualización con portada cada cierto tiempo, para el cambio de escena se utilizan eventos de usuario

## dbmanager
- Se encuentra en el archivo `dbmanager.py`.
- Es la clase encargada de conectarse ha la base de datos.
1. `check_records_file` comprueba si el directorio y el archivo de la base de datos existen.
2. `crear_db` si al comprobar los archivos no existieran los creamos
3. `conectar` se utiliza en todos los mettodos para crear una conexión y retornar la conexión y el cursor.
4. `desconectar` una vez realizamos la consulta nos desconectamos de la base de datos.
5. `consultaSQL` retorna todos los datos que consultes en tu petición.
6. `consultaConParametros` escribe en la base de datos un nuevo registro.
7. `borrar` borra de la base de datos el registro con el id que proporcionemos en la consulta

## Entidades
- Todas las entidades las encontramos en el archivo `entidades.py`.

### Nave
- Crea la nave del juego
1. `update` al ejecutar update la nave hace caso de los controles configurados para que esta se mueva.
2. `explosion_nave` se utiliza al chocar con algún objeto, lo que hace es cambiar la imagen de la nave que visualizamos.
3. `aterrizar_nave` cuando cambiamos de nivel se produce un aterrizaje de la nave, este método es el encargado de girar y desplazar la nave.

### Nave1
- Hereda todas las características de la nave inicial, pero se añade el movimiento de izquierda a derecha, esta clase se instancia después del nivel 5.

### Proyectil
- Crea los proyectiles de la nave
- Al instanciar pasamos como parámetro la misma nave para que este sepa en cada momento donde está.
1. `update` lanza el proyectil desde la punta de la nave

### Obstáculo
- Crea los obstáculos que aparecen en el juego, estos se crean con posiciones aleatorias, imágenes aleatorias y velocidades aleatorias, los creamos fuera de la pantalla para que en un principio no se vean.
1. `update` actualizamos la posición de los objetos con la velocidad que tiene asignada cada uno.

### IndicadorVida
- Crea los indicadores de las vidas
1. `update` actualiza entre las imágenes para que se cree el efecto del fuego de la nave.

### IndicadorDisparo
- Crea los indicadores de los disparos disponibles

### Planeta
- Crea el planeta de cambio de nivel, se crea fuera de la pantalla
1. `update` cuando llamamos a update movemos el planeta hasta ocupar la posición deseada.

### Marcador
- Es el encargado de gestionar la partida, con él controlamos los puntos, las vidas, el nivel y la dificultad.
1. `reset` lo llamamos desde game reinicia los valores del marcador se realiza antes de comenzar la partida.
2. `incrementar_puntos` lo llamamos desde partida cada vez que un objeto se pierde por la parte izquierda de la pantalla.
3. `restar_vida` se utiliza en partida para restar una vida cada vez que sufrimos una colisión, también elimina un indicador de vida del grupo de sprites
4. `restar_disparo` desde el nivel 6 tenemos disponibles 3 disparos por nivel, se encarga de restar los disparos y eliminar el indicador de la pantalla.
5. `subir_nivel` cada vez que pasa el tiempo de escena establecido subimos un nivel y reiniciamos los disparos.
6. `pintar` se llama desde partida para mostrar toda la información que controla el marcador.
7. `pintar_texto` es un método estándar creado para la renderización de textos que se pintan en todo el juego, ya lo utilizamos en las escenas.
8. `consultar_max_records` realiza una consulta a la base de datos para saber cuál es el récord máximo del juego y así poder pintarlo.
9. `crear_vidas` crea los indicadores de vida y los añade al grupo de sprites
10. `crear_disparos` crea los indicadores de disparos y los añade al grupo de sprites



