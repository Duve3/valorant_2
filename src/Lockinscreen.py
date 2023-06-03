import pygame
from button import Button
from util import createFont
import constants

pygame.init()
lockinscreen = pygame.display.set_mode([400, 400])
agents = ["jett"]
buttons = []
listofcordforbutton = []#i could make agents a llist of dic and have the cords attached to the valorant agents
count = 0
for x in agents:
    button = Button("Blue", listofcordforbutton[count], listofcordforbutton[count], 20, 20, createFont(constants.white, 20, fontLocation="../assets/CourierPrimeCode-Regular.ttf"), x)
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
                agentchosen = button[5]
                

    pygame.display.flip()

pygame.quit()
  
  
  
  
  
  
