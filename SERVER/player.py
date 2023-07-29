# this is here because I want type hints but do not want to import pygame
import math
import pickle
from enum import Enum

import pygame

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


class Bullet:
    def __init__(self, pos, startpos, endpos):
        self.pos = [pos[0], pos[1]]
        self.startpos = [startpos[0], startpos[1]]
        self.endpos = [endpos[0], endpos[1]]
        self.moveByChunks = 10
        self.rotation = self._getDegrees()
        self.model = pygame.image.load("../assets/bullet.png").convert_alpha()

    def _getDegrees(self):
        x1 = self.startpos[0]
        x2 = self.endpos[0]
        y1 = self.startpos[1]
        y2 = self.endpos[1]
        dx = x2 - x1
        dy = y2 - y1
        rads = math.atan2(-dy, dx)
        rads %= 2 * math.pi
        return math.degrees(rads)

    def move(self):
        rads = math.radians(self.rotation)
        nextx = self.pos[0] + self.moveByChunks * math.cos(rads)
        nexty = self.pos[1] + self.moveByChunks * math.sin(rads)

        self.pos = (nextx, nexty)


class Gun:
    def __init__(self, pos):
        self.model = None  # overridden by superior classes
        self.bullets: [Bullet] = []  # the list of bullets that have been fired by the gun
        self.pos: [] = [pos[0], pos[1]]  # the position of the gun currently
        self.rate: float = 10  # the rate of fire per second - can be overridden by superior classes
        self.modes: [] = ["semi", "auto", "burst"]  # the modes of fire in a list
        self.currentMode: str = "semi"  # the current mode
        self.lastFired = 0  # when the last shot was fired, 0 by default
        self.delay = 0  # the delay between shots (in ms) - overridden by superior classes

    def fire(self):
        if self.lastFired - pygame.time.get_ticks() > self.delay:
            mouse_pos = pygame.mouse.get_pos()
            delta = pygame.Vector2(mouse_pos[0], mouse_pos[1]) - pygame.Vector2(self.pos[0], self.pos[1])

            # Calculate the angle
            angle_to_mouse = math.atan2(delta.y, delta.x)
            looking_vector = (100 * math.cos(angle_to_mouse), 100 * math.sin(angle_to_mouse))
            dx = looking_vector[0] - self.pos[0]
            dy = looking_vector[1] - self.pos[1]
            rads = math.atan2(-dy, dx)
            rads %= 2 * math.pi

            length = 100
            endx = self.pos[0] + length * math.cos(rads)
            endy = self.pos[1] + length * math.sin(rads)

            nb = Bullet(self.pos, self.pos, (endx, endy))
            self.bullets.append(nb)
            self.lastFired = pygame.time.get_ticks()

    def tick(self):
        for bullet in self.bullets:
            bullet.move()


class Rifle(Gun):
    def __init__(self, pos):
        super().__init__(pos)
        self.model = pygame.image.load("../assets/rifle.png")
        self.rate = 10  # 10 bullets per second
        self.modes = ["auto"]
        self.mode = self.modes[0]
        self.delay = self.rate / 100


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
        self.__rifle = Rifle([self.x, self.y])
        self.weapons = [self.__rifle]
        self.currentWeapon = 0
        self.health = 100
        self.iframes = 0
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
        self.healthBar = pygame.Rect(self.x, self.y + 110, self.health//2, 5)
        self.redBar = pygame.Rect(self.x, self.y + 110, 50, 5)

    def __handleMovement(self, keys):
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

    def hookEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.weapons[self.currentWeapon].fire()

        keys = pygame.key.get_pressed()

        self.__handleMovement(keys)

    def __vars__(self):
        return vars(self)

    def __getstate__(self):
        sizes = [weapon.model.get_size() for weapon in self.weapons]
        for i, weapon in enumerate(self.weapons):
            weapon.model = [sizes[i], pygame.image.tobytes(weapon.model, "RGBA")]  # noqa - for some reason pycharm thinks that .tobytes doesnt exist on a surface as we are overwriting it with a list
        return self.__dict__

    def __setstate__(self, state):
        self.__dict__ = state
        for weapon in self.weapons:
            weapon.model = pygame.image.frombytes(weapon.model[1], weapon.model[0], "RGBA")  # noqa - same as above


if __name__ == "__main__":
    plr = Player(1, 1, 1, Models.JETT, Agents.JETT)
    test = pickle.dumps(plr)
    test = pickle.loads(test)

    if test.__vars__() == plr.__vars__():
        print("worked")
