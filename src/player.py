import pygame

class world:
    def __init__(self, blocklist):
        self.blocklist = blocklist
        self.x = 400
        self.y = 400 # #location in the world
    
    def checkup(self):
        for block in self.blocklist:
            if self.x + 500 > block["x"] and self.x - 500 < block["x"] and self.y + 500 > block["y"] and self.y - 500 < block["y"]: #onley draws things that you see
                pygame.draw.rect(block["screen"], block["color"], pygame.Rect(block["x"]-self.x, block["y"]-self.y, block["width"], block["height"]))
    
    def movement(self, dx, dy):
        self.x += dx
        self.y += dy
