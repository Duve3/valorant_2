import pygame.freetype
from constants import courierFont


def createFont(color, size, *, fontLocation=courierFont):
    font = pygame.freetype.Font(fontLocation)
    font.size = size
    font.fgcolor = color  # NOQA:TYPO
    return font


