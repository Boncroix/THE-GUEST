import pygame as pg


class Escena:
    def __init__(self, pantalla):
        self.pantalla = pantalla

    def bucle_principal(self):
        print('Metodo vacio bucle principal de escena')
        pass


class Portada(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena portada')
        salir = False
        while not salir:
            for evento in pg.event.get():
                if evento.type == pg.QUIT:
                    salir = True
            self.pantalla.fill((99, 0, 0))
            pg.display.flip()


class Partida(Escena):
    def __init__(self, pantalla):
        super().__init__(pantalla)

    def bucle_principal(self):
        super().bucle_principal()
        print('Estamos en la escena partida')
        salir = False
        while not salir:
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
