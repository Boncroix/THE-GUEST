import os


import pygame as pg


from .import ALTO, ANCHO, AZUL, BLANCO, FPS, RUTA_FUENTE, ROJO, TAM_FUENTE, TAM_1_FUENTE, VERDE


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
        self.tipo = pg.font.Font(RUTA_FUENTE, TAM_FUENTE)
        self.tipo1 = pg.font.Font(RUTA_FUENTE, TAM_1_FUENTE)
        ruta_image = os.path.join('resources', 'images', 'portada.jpg')
        self.image = pg.image.load(ruta_image)
        self.image = pg.transform.scale(self.image, (ANCHO, ALTO))

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena portada')
        salir = False
        while not salir:
            self.pintar_fondo()
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            pg.display.flip()

    def pintar_fondo(self):
        self.pantalla.blit(self.image, (0, 0))
        texto = self.tipo.render('THE QUEST', True, ROJO)
        pos_x = (ANCHO - texto.get_width()) / 2
        pos_y = (ALTO * 3/4 - texto.get_height() / 2)
        self.pantalla.blit(texto, (pos_x, pos_y))
        texto1 = self.tipo1.render(
            'Pulsa <ESPACIO> para comenzar el juego', True, BLANCO)
        pos_x = (ANCHO - texto1.get_width()) / 2
        pos_y = ALTO * 6/7
        self.pantalla.blit(texto1, (pos_x, pos_y))


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
