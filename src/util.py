import pygame.freetype
from constants import courierFont
import constants


def createFont(color, size, *, fontLocation=courierFont):
    font = pygame.freetype.Font(fontLocation)
    font.size = size
    font.fgcolor = color  # NOQA:TYPO
    return font


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


# TODO: fix text not correct color when using placeholder object.
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

                    # get text input from 0 to -1 i.e. end.
                    self.text = self.text[:-1]

                # Unicode standard is used for string
                # formation
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
    def __init__(self, pos, size, font, text, surfaceOffsets=(0, 0)):
        self.x = pos[0]
        self.y = pos[1]
        self.w = size[0]
        self.h = size[1]
        self.rect = pygame.Rect(self.x, self.y, self.w, self.h)
        self.font = font
        self.text = text
        self.triggered = False
        self.surfaceOffset = surfaceOffsets

    def handleEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mx, my = pygame.mouse.get_pos()
                mx -= self.surfaceOffset[0]
                my -= self.surfaceOffset[1]
                if self.rect.collidepoint(mx, my):
                    self.triggered = True
