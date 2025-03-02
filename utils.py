import pygame


def draw_circle(surface, x, y, radius, color):
    pygame.draw.circle(surface, color, (x, y), radius)