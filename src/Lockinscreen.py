import sys

import pygame
from button import Button
from util import createFont
import constants

pygame.init()
lockinscreen = pygame.display.set_mode([400, 400])
agents = ["jett"]
buttons = []
listofcordforbutton = []  # I could make agents a llist of dic and have the cords attached to the valorant agents
count = 0
for x in agents:
    button = Button("Blue", listofcordforbutton[count], listofcordforbutton[count], 20, 20,
                    createFont(constants.white, 20, fontLocation="../assets/CourierPrimeCode-Regular.ttf"), x)
    count += 1
    buttons.append(button)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # also tabbed in the following code because it seems like it should be tabbed in (using event.type)
        mouse = pygame.mouse.get_pos()
        for button in buttons:
            button.draw(lockinscreen)
            if button.isOver(mouse) and event.type == pygame.MOUSEBUTTONDOWN:
                agentchosen = buttons[5]

    pygame.display.flip()

pygame.quit()


# ^^^^ above code is original, but isn't designed well here's some properly designed code:

class LockInScreen:
    """
    LockInScreen:
    The screen for locking in
    """

    def __init__(self, screen: pygame.Surface, fpsClock: pygame.time.Clock, width: int, height: int):
        self.res = (width, height)
        self.display = screen
        self.fpsClock = fpsClock

        self.agents = {"Jett": Button(constants.blue, 50, 50, 20, 20, createFont(constants.white, 20,
                                                                                 fontLocation="../assets/CourierPrimeCode-Regular.ttf"),
                                      "Jett")}

    def run(self):
        while True:
            self.fpsClock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()  # exit but better

            # actual game code here:
