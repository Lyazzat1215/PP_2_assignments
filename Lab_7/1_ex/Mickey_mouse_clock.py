import pygame
import math
import datetime
pygame.init()
screen =pygame.display.set_mode((500, 500))
pygame.display.set_caption("Mickey Clock")
clock=pygame.time.Clock()
base= pygame.image.load("base_micky.jpg")
right_hand=pygame.image.load("second.png")
left_hand=pygame.image.load("minute.png")
running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

    screen.fill((255, 255, 255))
    screen.blit(face, (0, 0))

    now=datetime.datetime.now()
    sec=now.second
    minute=now.minute

    sec_angle=-sec*6
    min_angle=-minute*6

    sec_rot=pygame.transform.rotate(left_hand, sec_angle)
    min_rot=pygame.transform.rotate(right_hand, min_angle)

    screen.blit(sec_rot, (250, 250))
    screen.blit(min_rot, (250, 250))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()