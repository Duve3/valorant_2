from __future__ import annotations

from enum import Enum
from typing import Optional
import pygame.freetype
from pygame import Surface
import tkinter
import tkinter.filedialog
from typing import Sequence, Tuple, Union
from pygame import Color
from pygame import Vector2
import constants

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

# This typehint is used when a function would return an RGBA tuble
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]


def createFont(color: Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]], size: Union[float, Tuple[float, float]], fontLocation: str):
    """
    Outdated func for easily creating fonts, please use the class BetterFont if you can.
    Creates a pygame.freetype.font and sets the color and size for you
    :param color: Any color supported by pygame - anything that follows this: typing.Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]
    :param size: Just and int for the size value
    :param fontLocation: the location of the .ttf or similar font file
    :return: pygame.freetype.Font
    """
    font = pygame.freetype.Font(fontLocation, size=size)
    font.fgcolor = color
    return font


class InputField:
    def __init__(self, pos, size, activeColor, unactiveColor, font, placeholderFont, charLimit: int = 20, surfaceOffset=(0, 0), placeHolderText=""):
        self.x = pos[0]
        self.y = pos[1]
        self.active = False
        self.rect = pygame.Rect(pos, size)
        self.text = ""
        self.ColorActive = activeColor
        self.ColorUnactive = unactiveColor
        self.color = self.ColorUnactive
        self.charLimit = charLimit
        self.font = font
        self.FONTPlaceholder = placeholderFont
        self.placeholderText = placeHolderText
        self.surfaceOffset = surfaceOffset

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                if self.rect.collidepoint(mx, my):
                    self.active = True
                else:
                    self.active = False

            elif event.type == pygame.KEYDOWN and self.active:

                # Check for backspace
                if event.key == pygame.K_BACKSPACE:

                    # get text input from 0 to -1
                    self.text = self.text[:-1]

                # Unicode standard is used for string formation
                elif len(self.text) < self.charLimit:
                    self.text += event.unicode

        if self.active:
            self.color = self.ColorActive
        else:
            self.color = self.ColorUnactive

    def draw(self, screen, offsets=(5, 5)):
        self.rect = pygame.Rect((self.x, self.y), (self.rect.w, self.rect.h))
        pygame.draw.rect(screen, self.color, self.rect)
        if len(self.text) <= 0:
            self.FONTPlaceholder.render_to(screen, ((self.rect.centerx - self.FONTPlaceholder.get_rect(self.placeholderText, size=self.FONTPlaceholder.size).centerx) + offsets[0], self.y + offsets[1]), self.placeholderText)
        else:
            self.font.render_to(screen, ((self.rect.centerx - self.font.get_rect(self.text, size=self.font.size).centerx) + offsets[0], self.y + offsets[1]), self.text)


class Button:
    def __init__(self, pos, size, font, text, activeColor, unactiveColor, surfaceOffsets=(0, 0), width: int = 0, rounding: int = -1):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = font
        self.text = text
        self.color = unactiveColor
        self.activeColor = activeColor
        self.unactiveColor = unactiveColor
        self.triggered = False
        self.hovered = False
        self.surfaceOffset = surfaceOffsets
        self.width = width
        self.rounding = rounding

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                self.triggered = self.rect.collidepoint(mx, my)

            elif event.type == pygame.MOUSEMOTION:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                self.hovered = self.rect.collidepoint(mx, my)

    def draw(self, screen, offsets=(5, 5)):
        self.rect = pygame.Rect((self.x, self.y), (self.rect.w, self.rect.h))
        self.color = self.unactiveColor if not self.hovered else self.activeColor
        pygame.draw.rect(screen, self.color, self.rect, self.width, self.rounding)
        self.font.fgcolor = self.color
        self.font.render_to(screen, ((self.rect.centerx - self.font.get_rect(self.text, size=self.font.size).centerx) + offsets[0], self.y + offsets[1]), self.text)

class UIPopup:
    def __init__(self, pos, size):
        self.x = pos[0]
        self.y = pos[1]
        self.enabled = False
        self.surface = pygame.Surface(size=(size[0], size[1]))

    def resetSurface(self, givenSize=None):
        newSize = self.surface.get_size() if givenSize is None else givenSize
        self.surface = pygame.Surface(size=newSize)  # recreate surface

    def placeElements(self):  # the function for placing items
        self.surface.fill(constants.white)  # placeholder

    def draw(self, screen: pygame.Surface, redrawElements: bool = False):
        if self.enabled:
            if redrawElements:
                self.placeElements()
            screen.blit(self.surface, (self.x, self.y))
