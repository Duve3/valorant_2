import sys
import pygame
from util import createFont
from util.menu import Menu
import constants


class LockIn(Menu):
    def __init__(self, window: pygame.Surface, fpsClock: pygame.time.Clock, width: int, height: int):
        super().__init__(window, fpsClock, width, height)
