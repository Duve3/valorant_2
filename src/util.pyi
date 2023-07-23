from builtins import function

import pygame.freetype
from _common import RGBAOutput, ColorValue, RectValue, Coordinate, FontValue
from typing import Union, Tuple, Sequence, Optional, Iterable
from pygame import Color, Surface, Rect
from enum import Enum


STYLE_DEFAULT: int


class BetterFont(pygame.freetype.Font):
    ColorList: list[Union[Color, int, str, Tuple[int, int, int]]] | None
    def __init__(self,
                 fgColor: Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]],
                 fontSize: Union[float, Tuple[float, float]],
                 location: str,
                 font_index: int = 0,
                 resolution: int = 0,
                 ucs4: int = False,
                 ColorList: list[Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]] = None) -> None: ...

    def multiline_render_to(self,
                            surf: Surface,
                            dest: RectValue,
                            text: str,
                            fgcolor: Optional[ColorValue] = None,
                            bgcolor: Optional[ColorValue] = None,
                            style: int = STYLE_DEFAULT,
                            rotation: int = 0,
                            size: float = 0) -> list[pygame.rect.Rect]: ...

    def multiline_render(self,
                         text: str,
                         fgcolor: Optional[ColorValue] = None,
                         bgcolor: Optional[ColorValue] = None,
                         style: int = STYLE_DEFAULT,
                         rotation: int = 0,
                         size: float = 0,) -> list[Tuple[Surface, pygame.rect.Rect]]: ...

    def get_center(self,
                   surf: Surface,
                   text: str,
                   style: int = STYLE_DEFAULT,
                   rotation: int = 0,
                   size: float = 0,
                   x: bool = True,
                   y: bool = False) -> pygame.rect.Rect: ...


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

class FileSelector:
    FileLocationOutline: pygame.Rect
    FONT_FileLocation: pygame.freetype.Font
    FileButton: Button
    FONT_FileToParse: pygame.freetype.Font
    directoryToFile: str
    Title: str
    RectColor: ColorValue
    def __init__(self,
                 Pos: Coordinate,
                 Width: float,
                 FontColor: ColorValue,
                 RectColor: ColorValue,
                 ButtonSize: float,
                 ButtonActiveColor: ColorValue,
                 ButtonInactiveColor: ColorValue,
                 TitleText: str,
                 ButtonWidth: int = 0,
                 rounding: int = 0,
                 FontLocation: str = "./assets/CourierPrimeCode-Regular.ttf"): ...

    def render_to(self,
                  display: pygame.Surface): ...

    def handle_events(self,
                      events: list[pygame.event],
                      HandleTrigger: bool = True,
                      CustomFunc: function = None,
                      FileTypes: list[tuple[str, str]] = None) -> bool | None: ...


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
