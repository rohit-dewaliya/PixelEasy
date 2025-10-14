import pygame

pygame.init()
screen = pygame.display.set_mode((400, 400))
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((30, 30, 30))

    # Draw a filled ellipse
    pygame.draw.ellipse(screen, (0, 255, 0), (100, 100, 200, 100))

    # Draw only the border (outline)
    pygame.draw.ellipse(screen, (255, 0, 0), (100, 250, 200, 100), 3)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
