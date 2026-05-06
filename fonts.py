import pygame
import os

pygame.font.init()

font_path = os.path.join("fonts", "pixelated.otf")
font_path_1 = os.path.join("fonts", "RubikGlitch-Regular.ttf")
font_path_2 = os.path.join("fonts", "Silkscreen-Bold.ttf")

def get_font(size):
    return pygame.font.Font(font_path, size)

def get_font_glitch(size):
    return pygame.font.Font(font_path_1, size)

def get_font_silk_bold(size):
    return pygame.font.Font(font_path_2, size)

def draw_text_spacing(screen, text, font, color, x, y, spacing=0):
    for char in text:
        char_surface = font.render(char, True, color)
        screen.blit(char_surface, (x, y))
        x += char_surface.get_width() + spacing
