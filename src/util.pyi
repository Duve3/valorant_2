from builtins import function

import pygame.freetype
from pygame._common import RGBAOutput, ColorValue, RectValue, Coordinate, FontValue
from typing import Union, Tuple, Sequence, Optional, Iterable
from pygame import Color, Surface, Rect
from enum import Enum

class InputField:
    x: Union[float, int]
    y: Union[float, int]
    active: bool
    rect: Rect
    text = ""
    ColorActive: ColorValue
    ColorUnactive: ColorActive
    color: ColorValue
    charLimit: int
    font: FontValue
    FONTPlaceholder: FontValue
    placeholderText: str
    surfaceOffset: Coordinate

    def __init__(self,
                 pos: Coordinate,
                 size: Coordinate,
                 activeColor: ColorValue,
                 unactiveColor: ColorValue,
                 font: FontValue,
                 placeholderFont: FontValue,
                 charLimit: int = 20,
                 surfaceOffset: Coordinate = (0, 0),
                 placeHolderText: str = ""): ...

    def handleEvents(self,
                     events: Iterable): ...

    def draw(self,
             screen: Surface,
             offsets: Coordinate = (5, 5)): ...


class Button:
    x: Union[float, int]
    y: Union[float, int]
    w: Union[float, int]
    h: Union[float, int]
    rect: Rect
    font: FontValue
    text: str
    color: ColorValue
    activeColor: ColorValue
    unactiveColor: ColorValue
    triggered: bool
    hovered: bool
    surfaceOffset: Coordinate
    width: int
    rounding: int
    def __init__(self,
                 pos: Coordinate,
                 size: Coordinate,
                 font: FontValue,
                 text: str,
                 activeColor: ColorValue,
                 unactiveColor: ColorValue,
                 surfaceOffsets: Coordinate = (0, 0),
                 width: int = 0,
                 rounding: int = -1): ...

    def handleEvents(self,
                     events: Iterable): ...

    def draw(self,
             screen: Surface,
             offsets: Coordinate = (5, 5)): ...


def createFont(color: Union[pygame.Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]],
               size: Union[float, Tuple[float, float]],
               fontLocation: str) -> pygame.freetype.Font: ...


def prompt_file(filetypes: list,
                savedialog: bool) -> str: ...


class MenuResponses(Enum):
    QUIT = 1
    EnterPCMMenu = 2
    EnterMainMenu = 3
    EnterExecuteMenu = 4

class UIPopup:
    x: int
    y: int
    enabled: bool
    surface: Surface
    def __init__(self,
                 pos: Coordinate,
                 size: Coordinate): ...

    def resetSurface(self,
                     givenSize: Coordinate): ...

    def placeElements(self): ...

    def draw(self,
             screen: Surface,
             redrawElements: bool): ...
