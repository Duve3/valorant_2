import pygame


class Menu:
    def __init__(self,  window: pygame.Surface, fpsClock: pygame.time.Clock, width: int, height: int):
        self.screen = window
        self.fpsClock = fpsClock
        self.res = (width, height)
