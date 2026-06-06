import pygame

pygame.init()

screen = pygame.display.set_mode((600, 400))

pygame.display.set_caption("Pygame Test")

running = True

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

    screen.fill((30, 40, 80))

    pygame.display.update()

pygame.quit()