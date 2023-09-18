"""
abcdefghijk
"""
import math
from enum import Enum
import json
import pygame
import constants


class Agents(Enum):
    JETT = "JETT"
    RAZE = "RAZE"
    BRIMSTONE = "BRIM"
    SOVA = "SOVA"
    CYPHER = "CYHR"
    SAGE = "SAGE"
    Placeholder = "PHDR"


class Ranks(Enum):
    Iron1 = "Iron 1"
    Iron2 = "Iron 2"
    Iron3 = "Iron 3"
    Bronze1 = "Bronze 1"
    Bronze2 = "Bronze 2"
    Bronze3 = "Bronze 3"
    Silver1 = "Silver 1"
    Silver2 = "Silver 2"
    Silver3 = "Silver 3"
    Gold1 = "Gold 1"
    Gold2 = "Gold 2"
    Gold3 = "Gold 3"
    Plat1 = "Platinum 1"
    Plat2 = "Platinum 2"
    Plat3 = "Platinum 3"
    Dia1 = "Diamond 1"
    Dia2 = "Diamond 2"
    Dia3 = "Diamond 3"
    Asc1 = "Ascendant 1"
    Asc2 = "Ascendant 2"
    Asc3 = "Ascendant 3"
    Immo1 = "Immortal 1"
    Immo2 = "Immortal 2"
    Immo3 = "Immortal 3"
    Radiant = "Radiant"
    rankMap = [Iron1, Iron2, Iron3, Bronze1, Bronze2, Bronze3, Silver1, Silver2, Silver3, Gold1, Gold2, Gold3, Plat1, Plat2, Plat3, Dia1, Dia2, Dia3, Asc1, Asc2, Asc3, Immo1, Immo2, Immo3, Radiant]

    @staticmethod
    def fromValue(value):
        try:
            return Ranks.rankMap.value[value]
        except ValueError:
            return Ranks.Radiant


class Models(Enum):
    JETT = ["JMA", "JMB", "JMC"]
    RAZE = []
    BRIMSTONE = []
    SOVA = []
    CYPHER = []
    SAGE = []
    PLACEHOLDER = ['ph']
    RIFLE = [r"C:\Users\laksh\PycharmProjects\valorant_2\assets\rifle.png"]


class Guntypes(Enum):
    AUTO = "auto"
    SEMI = "semi"
    BURST = "burst"


class _Models(Enum):
    JETT = Models.JETT
    RAZE = Models.RAZE
    BRIM = Models.BRIMSTONE
    SOVA = Models.SOVA
    CYHR = Models.CYPHER
    SAGE = Models.SAGE
    PHDR = Models.PLACEHOLDER


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
        self.modes: [] = [Guntypes.AUTO.value, Guntypes.SEMI.value, Guntypes.BURST.value]  # the modes of fire in a list
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

    def draw(self, surf: pygame.Surface):
        surf.blit(pygame.image.load(self.model).convert_alpha(), self.pos)


class Rifle(Gun):
    def __init__(self, pos):
        super().__init__(pos)
        self.model = Models.RIFLE.value
        self.rate = 10  # 10 bullets per second
        self.modes = [Guntypes.AUTO.value]
        self.mode = self.modes[0]
        self.delay = self.rate / 100


class Player:
    def __init__(self, pid, x, y, agent):
        self.id = pid
        self.x = x
        self.vx = 0
        self.ax = 0
        self.y = y
        self.vy = 0
        self.ay = 0
        self.width = 50
        self.height = 100
        self.agent = agent.value
        self.models = getattr(_Models, self.agent).value.value
        __rifle = Rifle([self.x, self.y])
        self.weapons = [__rifle]
        self.currentWeapon = 0
        self.health = 100
        self.iframes = 0
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.healthBar = pygame.Rect(self.x, self.y + 100, self.health // 2, 5)
        self.redBar = pygame.Rect(self.x, self.y + 100, 50, 5)
        self.maxSpeed = 10
        self.startSpeed = 5

    def draw(self, display: pygame.Surface, wireframe: bool = False):
        self.__update()
        if wireframe:
            pygame.draw.rect(display, constants.blue, self.rect, width=5)
        else:
            pygame.draw.rect(display, constants.blue, self.rect)

        pygame.draw.rect(display, constants.red, self.redBar)
        pygame.draw.rect(display, constants.green, self.healthBar)

        # display.blit(self.models[self.currentModelID], self.rect)

    def __update(self):
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.healthBar = pygame.Rect(self.x, self.y + 110, self.health // 2, 5)
        self.redBar = pygame.Rect(self.x, self.y + 110, 50, 5)

    @staticmethod
    def decay(var):
        return var - 1 if var > 0 else 0

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
        self.vy = self.decay(self.vy)
        self.vx = self.decay(self.vx)

    def hookEvents(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.weapons[self.currentWeapon].fire()

        keys = pygame.key.get_pressed()

        self.__handleMovement(keys)

    def __vars__(self):
        return vars(self)


def JSONToPlayer(JSON: str) -> Player:
    JSON = json.loads(JSON)

    player = Player(0, 0, 0, Agents.Placeholder)  # this is all bs and is just designed as placeholders

    # recreating the weapons and bullets from JSON
    guns = JSON['weapons']
    for i, weapon in enumerate(guns):
        dummyGun = Gun((0, 0))
        dummyGun.__dict__ = weapon
        guns[i] = dummyGun
        for i, bullet in enumerate(dummyGun.bullets):
            dummyBullet = Bullet((0, 0), (0, 0), (0, 0))
            dummyBullet.__dict__ = bullet
            dummyGun.bullets[i] = dummyBullet

    JSON['rect'] = pygame.Rect([int(i) for i in JSON['rect'].split(",")])
    JSON['healthBar'] = pygame.Rect([int(i) for i in JSON['healthBar'].split(",")])
    JSON['redBar'] = pygame.Rect([int(i) for i in JSON['redBar'].split(",")])

    player.__dict__ = JSON

    return player


def playerToJSON(plr: Player) -> str:
    cmd = plr.__reduce__()
    res: dict = {key: value for key, value in cmd[2].items()}  # deepcopies the dict to avoid any issues with the player

    for weapon in res['weapons']:
        weapon.bullets = [bullet.__reduce__()[2] for bullet in weapon.bullets]
    res['weapons'] = [weapon.__reduce__()[2] for weapon in res['weapons']]

    res['rect'] = str(res['rect']).replace('Rect(', "").replace(")", "")
    res['healthBar'] = str(res['healthBar']).replace('Rect(', "").replace(")", "")
    res['redBar'] = str(res['redBar']).replace('Rect(', "").replace(")", "")

    return str(res).replace("'", '"')


if __name__ == "__main__":
    import logging

    logger = logging.getLogger('player')
    logger = constants.setupLogger(logger)

    newPlayer = Player(3, 0, 1, Agents.Placeholder)
    JSONPlayer = playerToJSON(newPlayer)

    logger.debug(f"jsonplr: {JSONPlayer}")
    evenBetterPlayer = JSONToPlayer(JSONPlayer)

    logger.debug(f"newPlayerDICT: {newPlayer.__dict__}")
    logger.debug(f"evenBetterPlayerDICT: {evenBetterPlayer.__dict__}")
