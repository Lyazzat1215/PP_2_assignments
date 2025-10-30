import pygame
pygame.init()
screen=pygame.display.set_mode((400, 200))
pygame.display.set_caption("Music Player")
songs=["MJ_YouRockMyWorld.mp3", "BTS_HouseOfCards.mp3", "Yungblud_Parents.mp3"]
index=0
pygame.mixer.music.load(songs[index])
running=True

while running:
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            running=False

        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_p:   #p-play играет музыка
                pygame.mixer.music.play()
            elif event.key==pygame.K_s: #s-stop пауза
                pygame.mixer.music.stop()
            elif event.key== pygame.K_n: #n-next следующая
                index=(index+1) %len(songs)
                pygame.mixer.music.load(songs[index])
                pygame.mixer.music.play()
            elif event.key== pygame.K_b: #b-back предыдущая
                index =(index-1) % len(songs)
                pygame.mixer.music.load(songs[index])
                pygame.mixer.music.play()

    pygame.display.flip()

pygame.quit()