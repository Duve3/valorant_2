import pygame
from pygame.math import Vector2
pygame.init()
clock = pygame.time.Clock()
#CON
font = pygame.font.SysFont('Courier New', 40)
size = 800

bullets = []
walls = []

class display:
    def __init__(self,sizes) -> None:
        self.screen = pygame.display.set_mode((sizes,sizes))

    def fill(self, color):
        self.screen.fill(color)

    def bulletsdraw(self, layer):
        for bullet in bullets:

            pygame.draw.rect(self.screen, (200, 0, 0), pygame.Rect(bullet.position.x+size/2-layer.x, bullet.position.y+size/2-layer.y, 5, 5))

            bullet.update()
            ammo = font.render(str(layer.gun.ammo), True, (255,0,0))
            self.screen.blit(ammo, (size-90,size-50))
    def drawself(self):
        pygame.draw.rect(self.screen, (0, 200, 0), pygame.Rect(size/2, size/2, 20, 20))



class gun:
    def __init__(self, damage, speed, maxammo,reloadinms) -> None:
        self.damage = damage
        self.speed = speed
        self.maxammo = maxammo
        self.ammo = self.maxammo
        self.reloadtime = reloadinms
        self.reloading = False
        self.countdown = 1
    def startreload(self):
         if not self.reloading:
            self.countdown = self.reloadtime
            self.reloading = True
    def reload(self):
        
        if self.reloading:
            self.countdown -= 1
            if self.countdown <= 0:
                self.ammo = self.maxammo
                self.reloading = False
    



class Bullet:
    def __init__(self, pos, target,damage,speed) -> None:
        self.damage = damage
        self.speed = speed
        self.is_active = False
        direction = target - pos
        self.position = Vector2(pos) 
        self.velocity = direction.normalize() * 11
        self.timealive = 1000#BULELELLTETTELTLETTELT

        
    def update(self):


        self.position += self.velocity
        self.timealive -= 1
        if self.timealive <= 0:
            self.kill()



    def kill(self):
        bullets.remove(self)





class wall:
    def __init__(self,x,y,width,height) -> None:

        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.rect = pygame.Rect(x,y,width,height)
        walls.append(self)




    def collision(self, player):
        self.rect = pygame.Rect(self.x+size/2-player.x, self.y+size/2-player.y, self.width, self.height)
        pygame.draw.rect(screen.screen, (200,200,200),self.rect)
        if self.rect.colliderect(pygame.Rect(size/2, size/2, 20, 20)):
            
            if player.xv > 0 or player.xv < 0:
                player.x -= player.xv
            if player.yv > 0 or player.yv < 0:
                player.y -= player.yv







class player:
    def __init__(self,x,y,guns) -> None:
        self.gun = guns
        self.x = x
        self.y = y
        self.yv = 0
        self.xv = 0
    def dropgun(self):
        self.gun.reloading = False
        self.gun.countdown = 1
    def shoot(self):
        if self.gun.ammo > 0:
            if not self.gun == None:
                if not self.gun.reloading:
                    x, y = pygame.mouse.get_pos()
                    target_x = x - size / 2 + self.x
                    target_y = y - size / 2 + self.y
                    bullets.append(Bullet(Vector2(self.x+8,self.y+8),Vector2(target_x,target_y),self.gun.damage,self.gun.speed))

                    self.gun.ammo -= 1

        else:
            self.gun.startreload()
        

    

    def update(self):

       
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_r]:
            self.gun.startreload()
        if pressed[pygame.K_LEFT]:
                self.xv = -1
        if pressed[pygame.K_RIGHT]:
                self.xv = 1
        if pressed[pygame.K_UP]:
                self.yv = -1
        if pressed[pygame.K_DOWN]:
                self.yv = 1
        if pygame.mouse.get_pressed()[0] == 1:
                self.shoot()
        self.gun.reload()
        self.x += self.xv
        self.y += self.yv

    def cleanup(self):
        self.yv = 0
        self.xv = 0
        
            
vandal = gun(10,3,25,100)
Player = player(400,400,vandal)
screen = display(size)
wallin = wall(300,300,20,20)
def Main():

    print("running")

    running = True

    while running:

        for events in pygame.event.get():

            if events.type == pygame.QUIT:
                
                running = False

        screen.fill((0,0,0))

        Player.update()

        screen.drawself()

        screen.bulletsdraw(Player)

        for wall in walls:

            wall.collision(Player)

        pygame.display.flip()


        clock.tick(60)

        Player.cleanup()


if __name__ == "__main__":
    Main()

            
            
