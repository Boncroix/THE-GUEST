
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
