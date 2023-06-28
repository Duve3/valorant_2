# this is here because yeah yeah
if __name__ == "__main__":
    import pygame

from enum import Enum


class Agents(Enum):
    JETT = "JETT"
    RAZE = "RAZE"
    BRIMSTONE = "BRIM"
    SOVA = "SOVA"
    CYPHER = "CYHR"
    SAGE = "SAGE"


class Player:
    def __init__(self, pid, x, y, models, agent: Agents):
        self.id = pid
        self.x = x
        self.y = y
        self.models = models
        self.agent = agent
        self.currentModelID = 0
        self.currentWeapon = None  # add later
        self.health = 100

    def draw(self, display: pygame.Surface):
        display.blit(self.models[self.currentModelID], (self.x, self.y))
