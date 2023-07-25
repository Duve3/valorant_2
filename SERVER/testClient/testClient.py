# this is here because I want type hints but do not want to import pygame
import pygame

from enum import Enum

from src import constants


class Agents(Enum):
    JETT = "JETT"
    RAZE = "RAZE"
    BRIMSTONE = "BRIM"
    SOVA = "SOVA"
    CYPHER = "CYHR"
    SAGE = "SAGE"


class Models(Enum):
    JETT = ["JMA", "JMB", "JMC"]
    RAZE = []
    BRIMSTONE = []
    SOVA = []
    CYPHER = []
    SAGE = []


class Player:
    def __init__(self, pid, x, y, models, agent: Agents):
        self.id = pid
        self.x = x
        self.vx = 0
        self.y = y
        self.vy = 0
        self.width = 50
        self.height = 100
        self.models = models
        self.agent = agent
        self.currentModelID = 0
        self.currentWeapon = None  # add later
        self.health = 100
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.healthBar = pygame.Rect(self.x, self.y + 100, self.health//2, 5)
        self.redBar = pygame.Rect(self.x, self.y + 100, 50, 5)

    def draw(self, display: pygame.Surface, wireframe: bool = False):
        if wireframe:
            pygame.draw.rect(display, constants.blue, self.rect, width=5)
        else:
            pygame.draw.rect(display, constants.blue, self.rect)

        pygame.draw.rect(display, constants.red, self.redBar)
        pygame.draw.rect(display, constants.green, self.healthBar)

        # display.blit(self.models[self.currentModelID], self.rect)

    def update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.healthBar = pygame.Rect(self.x, self.y + 10, self.health//2, 5)
        self.redBar = pygame.Rect(self.x, self.y + 110, 50, 5)

    def handleMovement(self, keys):
        # key handling
        if keys[pygame.K_w]:
            self.vy += 5

        if keys[pygame.K_s]:
            self.vy -= 5

        if keys[pygame.K_a]:
            self.vx -= 5

        if keys[pygame.K_d]:
            self.vx += 5

        # movement
        self.x += self.vx
        self.y += self.vy

        # velo decay
        self.vy = self.vy - 1 if self.vy > 0 else 0
        self.vx = self.vx - 1 if self.vx > 0 else 0

    def __vars__(self):
        return vars(self)
