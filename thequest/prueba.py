import os


import pygame as pg


from .import (ALTO, ANCHO, AZUL, BLANCO, CENTRO_X, CENTRO_Y, FPS, HISTORIA, INFO, INSTRUCCIONES,
              INTERVALO_PARPADEO_INFO, MARGEN_X, FUENTE_NASA, FUENTE_CONTRAST,
              ROJO, TAM_FUENTE_1, TAM_FUENTE_2, TAM_FUENTE_3, TAM_FUENTE_4,
              VELOCIDAD_FONDO_PARTIDA, VERDE)

from .entidades import Nave


    def pintar_portada(self):
        # Pintar imagen de fondo
        self.pantalla.blit(self.image, (0, 0))
        self.pintar_titulo()
        self.pintar_informacion()
        self.pintar_historia()
        self.visualizar_instrucciones()
        self.visualizar_records()

    def pintar_titulo(self):
        self.pintar_texto(['THE QUEST',], self.tipo4, CENTRO_X,
                          ALTO * 17/20, 'centro', VERDE, False)

    def pintar_informacion(self):
        tiempo_actual = pg.time.get_ticks()
        if tiempo_actual - self.ultimo_cambio >= INTERVALO_PARPADEO_INFO:
            self.parpadeo_visible = not self.parpadeo_visible
            self.ultimo_cambio = tiempo_actual
        if self.parpadeo_visible:
            self.pintar_texto(INFO, self.tipo3, CENTRO_X,
                              0, 'centro', BLANCO, False)

    def pintar_historia(self):
        self.pintar_texto(HISTORIA, self.tipo2, CENTRO_X,
                          ALTO * 11/20, 'centro', BLANCO, False)

    def visualizar_instrucciones(self):
        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_i]:
            self.pintar_texto(INSTRUCCIONES, self.tipo2, MARGEN_X,
                              ALTO * 7/20, '', BLANCO, True)

    def visualizar_records(self):
        estado_teclas = pg.key.get_pressed()
        if estado_teclas[pg.K_r]:
            # Pintar imagen de fondo
            self.pantalla.blit(self.image, (0, 0))

    def pintar_texto(self, txt, tipo, pos_x, pos_y, alineacion, color, fondo):
if fondo == True:
    self.pantalla.blit(self.image, (0, 0))
for linea in txt:
    texto = tipo.render(linea[:-1], True, color)
    if alineacion == 'centro':
        pos_x_centro = pos_x - (texto.get_width() / 2)
        self.pantalla.blit(texto, (pos_x_centro, pos_y))
    else:
        self.pantalla.blit(texto, (pos_x, pos_y))
    pos_y += texto.get_height()











# import pygame
# import sys
# import time
# from .import HISTORIA
# pygame.init()

# # Configuración de la ventana
# screen_width = 800
# screen_height = 400
# screen = pygame.display.set_mode((screen_width, screen_height))
# pygame.display.set_caption("Escribiendo a máquina con saltos de línea")

# # Configuración de la fuente y texto
# font = pygame.font.Font(None, 36)
# text_color = (255, 255, 255)

# # Texto con saltos de línea
# text_lines = HISTORIA

# typing_speed = 20  # caracteres por segundo

# # Inicialización de variables
# current_text = ""
# line_index = 0
# char_index = 0
# last_update = 0
# pos_y = 100
# pos_y2 = 100
# texto_render = []

# running = True
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     screen.fill((0, 0, 0))

#     # Simula escribir una letra a la vez
#     if line_index < len(text_lines):
#         line = text_lines[line_index]
#         if char_index < len(line) and time.time() - last_update > 1 / typing_speed:
#             current_text += line[char_index]
#             char_index += 1
#             last_update = time.time()
#         elif char_index >= len(line):
#             texto_render.append(current_text)
#             char_index = 0
#             line_index += 1
#             current_text = ''
#             print(texto_render)
#             pos_y += rendered_text.get_height()
#     rendered_text = font.render(current_text, True, text_color)
#     screen.blit(rendered_text, (50, pos_y))
#     pos_y2 = 100
#     for linea in texto_render:
#         texto = font.render(linea, True, text_color)
#         screen.blit(texto, (50, pos_y2))
#         pos_y2 += texto.get_height()

#     pygame.display.flip()

#     if line_index >= len(text_lines):
#         pygame.quit()
#         sys.exit()

#     def pinttar_historia(self):
#         current_text = ""
#         line_index = 0
#         char_index = 0
#         last_update = 0
#         pos_y = 100
#         pos_y2 = 100
#         texto_render = []
#         typing_speed = 20
#         if line_index < len(HISTORIA):
#             line = HISTORIA[line_index]
#         if char_index < len(line) and time.time() - last_update > 1 / typing_speed:
#             current_text += line[char_index]
#             char_index += 1
#             last_update = time.time()
#         elif char_index >= len(line):
#             texto_render.append(current_text)
#             char_index = 0
#             line_index += 1
#             current_text = ''
#             print(texto_render)
#             pos_y += rendered_text.get_height()
#         rendered_text = font.render(current_text, True, text_color)
#         screen.blit(rendered_text, (50, pos_y))
#         pos_y2 = 100
#         for linea in texto_render:
#             texto = font.render(linea, True, text_color)
#             screen.blit(texto, (50, pos_y2))
#             pos_y2 += texto.get_height()
