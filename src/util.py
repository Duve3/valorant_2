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

from src import constants

Coordinate = Union[Tuple[float, float], Sequence[float], Vector2]

# This typehint is used when a function would return an RGBA tuble
RGBAOutput = Tuple[int, int, int, int]
ColorValue = Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]

STYLE_DEFAULT = pygame.freetype.STYLE_DEFAULT


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


# Btw if something isn't type checked (doesn't have the arg: thing) its probably in the util.pyi file.
# This is because of some type checking things not working in normal python files and must be put in pyi files.
class BetterFont(pygame.freetype.Font):
    def __init__(self, fgColor: Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]], fontSize: Union[float, Tuple[float, float]], location: str, font_index: int = 0, resolution: int = 0, ucs4: int = False, ColorList: list[Union[Color, int, str, Tuple[int, int, int], RGBAOutput, Sequence[int]]] = None):
        super().__init__(location, size=fontSize, font_index=font_index, resolution=resolution, ucs4=ucs4)
        self.fgcolor = fgColor
        self.ColorList = ColorList

    def multiline_render_to(self, surf: Surface, dest, text: str, fgcolor: Optional[ColorValue] = None, bgcolor: Optional[ColorValue] = None, style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0) -> list[pygame.rect.Rect]:
        ListText = text.splitlines()
        ListRects = []
        useColorList = True if self.ColorList is not None else False
        for i, line in enumerate(ListText):
            if useColorList:
                self.fgcolor = self.ColorList[i % len(self.ColorList)]
            rect = self.render_to(surf=surf, dest=(dest[0], dest[1] + (i * self.size + 10)), text=line, fgcolor=fgcolor, bgcolor=bgcolor, style=style, rotation=rotation, size=size)
            ListRects.append(rect)

        return ListRects

    # probably works IDK
    def multiline_render(self, text: str, fgcolor: Optional[ColorValue] = None, bgcolor: Optional[ColorValue] = None, style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0) -> list[Tuple[Surface, pygame.rect.Rect]]:
        ListText = text.splitlines()
        ListSurfs = []
        for i, line in enumerate(ListText):
            surfRect = self.render(text=line, fgcolor=fgcolor, bgcolor=bgcolor, style=style, rotation=rotation, size=size)
            ListSurfs.append(surfRect)

        return ListSurfs

    def get_center(self, surf: Surface, text: str, style: int = STYLE_DEFAULT, rotation: int = 0, size: float = 0, x: bool = True, y: bool = False) -> pygame.rect.Rect:
        rect = self.get_rect(text=text, style=style, rotation=rotation, size=size)
        if x:
            rect.centerx = surf.get_rect().centerx

        if y:
            rect.centery = surf.get_rect().centery

        return rect


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


def prompt_file(filetypes: list = None, savedialog=False):
    """Create a Tk file dialog and cleanup when finished"""
    if filetypes is None:
        filetypes = [("EasyHotkey Files", "*.ehk")]
    top = tkinter.Tk()
    top.withdraw()  # hide window
    if not savedialog:
        file_name = tkinter.filedialog.askopenfilename(parent=top, filetypes=filetypes)
    else:
        file_name = tkinter.filedialog.asksaveasfilename(parent=top, filetypes=filetypes)
    top.destroy()
    return file_name


class MenuResponses(Enum):
    QUIT = 1
    EnterPCMMenu = 2
    EnterMainMenu = 3
    EnterExecuteMenu = 4


class FileSelector:
    def __init__(self, Pos: Coordinate, Width: float, FontColor: ColorValue, RectColor: ColorValue, ButtonSize: float, ButtonActiveColor: ColorValue, ButtonInactiveColor: ColorValue, TitleText: str, ButtonWidth: int = 0, rounding: int = 0, FontLocation: str = "./assets/CourierPrimeCode-Regular.ttf"):
        self.FileLocationOutline = pygame.Rect(Pos, (Width, 50))
        self.FONT_FileLocation = createFont(FontColor, 25, FontLocation)
        buttonPos = (self.FileLocationOutline.x + (self.FileLocationOutline.w + 20), self.FileLocationOutline.y)
        buttonSize = (ButtonSize, self.FileLocationOutline.height)
        buttonFont = createFont(FontColor, 30, FontLocation)
        self.FileButton = Button(buttonPos, buttonSize, buttonFont, "browse", ButtonActiveColor, ButtonInactiveColor,
                                 width=ButtonWidth, rounding=rounding)
        self.FONT_FileToParse = createFont(FontColor, 40, FontLocation)
        self.directoryToFile = ""
        self.Title = TitleText
        self.RectColor = RectColor

    def render_to(self, display: pygame.Surface):
        self.FONT_FileToParse.render_to(display, (30, self.FileLocationOutline.y - 40), self.Title)
        pygame.draw.rect(display, self.RectColor, self.FileLocationOutline, self.FileButton.width, self.FileButton.rounding)
        if self.FONT_FileLocation.get_rect(self.directoryToFile, size=self.FONT_FileLocation.size).width > self.FileLocationOutline.width:
            self.FONT_FileLocation.size -= 1
        self.FONT_FileLocation.render_to(display, (self.FileLocationOutline.x + 10, self.FileLocationOutline.y + 15), self.directoryToFile)
        self.FileButton.draw(display, offsets=(2, 14))

    def handle_events(self, events: list[pygame.event], HandleTrigger: bool = True, CustomFunc=None, FileTypes: list[tuple[str, str]] = None) -> bool | None:
        if FileTypes is None:
            FileTypes = [("SimpleHotkey Files", "*.shk"), ("EasyHotkey Files", "*.ehk")]
        self.FileButton.handleEvents(events)

        if self.FileButton.triggered:
            if HandleTrigger:
                self.directoryToFile = prompt_file(savedialog=False, filetypes=FileTypes)
                self.FileButton.triggered = False
            elif CustomFunc is not None:
                CustomFunc()
                self.FileButton.triggered = False
                return True
            else:
                self.FileButton.triggered = False
                return True


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
