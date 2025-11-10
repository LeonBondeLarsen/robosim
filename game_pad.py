import pygame

pygame.init()
pygame.joystick.init()

js = pygame.joystick.Joystick(0)
js.init()

running = True
while running:
    for event in pygame.event.get():
        print(event)
