import pygame
from pygame.math import Vector2
pygame.init()
bullets = []#bullets.append(bullet(x,y,damage))
size = 800
screen = pygame.display.set_mode([size, size])
fpsClock = pygame.time.Clock()
reloading = False
rcountdown = 0
class Bullet:
    def __init__(self, pos, target,damage):
        self.damage = damage
        self.speed = 5
        self.heading = None
        self.is_active = False
        direction = target - pos
        self.position = Vector2(pos) 
        radius, angle = direction.as_polar()
        self.velocity = direction.normalize() * 11
        self.timealive = 1000
    def update(self):
        self.position += self.velocity
        self.timealive -= 1
        if self.timealive <= 0:
            self.kill()

    def draw(self, screen):
        #A little bit silly
        pygame.draw.rect(screen,(0, 0, 0),(self.x, self.y, 10, 10))
    def kill(self):
        bullets.remove(self)
    

        

        
class world:
    def __init__(self, blocklist):
        self.count = 0
        self.blocklist = blocklist
        self.x = 400
        self.y = 400
        self.maxbullets = 25
        self.bulletcount = self.maxbullets
        self.reloading = False
        self.playersize = 20
        self.rcountdown = 0
    def checkup(self):
        for block in self.blocklist:
            if self.x + size > block["x"] and self.x - size < block["x"] and self.y + size > block["y"] and self.y - size < block["y"]:
                pygame.draw.rect(block["screen"], block["color"], pygame.Rect(block["x"]+size/2-self.x, block["y"]+size/2-self.y, block["width"], block["height"]))
                self.count += 1
    def bulletsdraw(self):
        for bullet in bullets:
            pygame.draw.rect(screen, (200, 0, 0), pygame.Rect(bullet.position.x+size/2-self.x, bullet.position.y+size/2-self.y, 5, 5))
            bullet.update()

            
    def drawself(self):
        pygame.draw.rect(screen, (0, 200, 0), pygame.Rect(size/2, size/2, self.playersize, self.playersize))
    def movement(self, dx, dy):
        self.x += dx
        self.y += dy
    def shoot(self,damage):
        x, y = pygame.mouse.get_pos()
        target_x = x - size / 2 + self.x
        target_y = y - size / 2 + self.y
        bullets.append(Bullet(Vector2(self.x+8,self.y+8),Vector2(target_x,target_y),damage))
    def checkmove(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_LEFT]:
            self.movement(-1,0)
        if pressed[pygame.K_RIGHT]:
            self.movement(1,0)
        if pressed[pygame.K_UP]:
            self.movement(0,-1)
        if pressed[pygame.K_DOWN]:
            self.movement(0,1)
    def shootcheck(self):
            if pygame.mouse.get_pressed()[0]:
                if self.bulletcount > 0 and not reloading:
                    self.shoot(10)
                    self.bulletcount -= 1
                elif not self.reloading:
                    self.reloading = True
                    self.rcountdown = 120#This is 2 seconds(well 2 seconds + 1/60 of a second but who cares)
                    self.bulletcount = self.maxbullets
                
            elif self.rcountdown < 0:
                self.reloading = False
            self.rcountdown -= 1
        
    def checkall(self):
        self.checkmove()
        self.shootcheck()
        self.checkup()
        self.drawself()
        self.bulletsdraw()
        
        


bind = world([{"screen": screen, "color": (0, 0, 200), "x": 400, "y": 400, "width": 20, "height": 20}])

pygame.display.set_caption("2D Space")

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((0,0,0))
    bind.checkall()
    fpsClock.tick(60)
    pygame.display.flip()
pygame.quit()
    fpsClock.tick(60)
    print(len(bullets))

pygame.quit()
