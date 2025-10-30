import pygame

pygame.init()
screen=pygame.display.set_mode((600, 400))
pygame.display.set_caption("Moving Ball")
x, y=300, 200
radius=25
speed=20

running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    keys=pygame.key.get_pressed()
    if keys[pygame.K_UP] and y-radius>0:
        y-=speed
    if keys[pygame.K_DOWN] and y +radius<400:
        y+=speed
    if keys[pygame.K_LEFT] and x-radius>0:
        x-=speed
    if keys[pygame.K_RIGHT] and x+ radius<600:
        x+=speed
    screen.fill((255, 255, 255))
    pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
    pygame.display.flip()

pygame.quit()