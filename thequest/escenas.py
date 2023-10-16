import os


import pygame as pg


from .import (ALTO, ANCHO, AZUL, BLANCO, CENTRO_Y, FPS, HISTORIA, RUTA_FUENTE, ROJO, TAM_FUENTE_GRA,
              TAM_FUENTE_MED, TAM_FUENTE_PEQ, VERDE)


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla
        self.reloj = pg.time.Clock()

    def bucle_principal(self):
        print('Metodo vacio bucle principal de escena')
        pass


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)
        self.tipo = pg.font.Font(RUTA_FUENTE, TAM_FUENTE_GRA)
        self.tipo1 = pg.font.Font(RUTA_FUENTE, TAM_FUENTE_MED)
        self.tipo2 = pg.font.Font(RUTA_FUENTE, TAM_FUENTE_PEQ)
        ruta_image = os.path.join('resources', 'images', 'portada.jpg')
        self.image = pg.image.load(ruta_image)
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))
        ruta_musica = os.path.join('resources', 'music', 'musica_espacial.mp3')
        pg.mixer.music.load(ruta_musica)
        pg.mixer.music.play(-1)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena portada')
        salir = False
        while not salir:
            self.pintar_portada()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            pg.display.flip()

    def pintar_portada(self):
        self.pantalla.blit(self.image, (0, 0))
        # Pintar titulo
        texto = self.tipo.render('THE QUEST', True, ROJO)
        pos_x = (ANCHO - texto.get_width()) / 2
        pos_y = ALTO * 6/7
        self.pantalla.blit(texto, (pos_x, pos_y))
        # Pintar información para comenzar ha jugar
        texto1 = self.tipo1.render(
            'Pulsa <ESPACIO> para comenzar el juego', True, BLANCO)
        pos_x = (ANCHO - texto1.get_width()) / 2
        pos_y = ALTO * 1/7
        self.pantalla.blit(texto1, (pos_x, pos_y))

        # TODO Pintar historia como si se estubiese tecleando en el teclado

        # Pintar historia
        pos_y = CENTRO_Y - TAM_FUENTE_PEQ
        for linea in HISTORIA:
            texto2 = self.tipo2.render(linea[:-1], True, BLANCO)
            pos_x = (ANCHO - texto2.get_width()) / 2
            pos_y += texto2.get_height()
            self.pantalla.blit(texto2, (pos_x, pos_y))


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena partida')
        salir = False
        while not salir:
            self.reloj.tick(FPS)
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((0, 99, 0))
            pg.display.flip()


class Records(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena records')
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((0, 0, 99))
            pg.display.flip()
