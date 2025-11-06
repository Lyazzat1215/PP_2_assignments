#импортирование библиотек
import pygame, sys
from pygame.locals import* #импорт констант pygame
import random, time
#Initializing 
pygame.init()

FPS=60 # интересный факт: в мультах использую обычно 12-24 фпс 
FramePerSec=pygame.time.Clock()

# тюплы для цветов
BLUE=(0, 0, 255)
RED=(255, 0, 0)
GREEN=(0, 255, 0)
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
YELLOW=(255, 255, 0)

SCREEN_WIDTH=400  # размеры экрана
SCREEN_HEIGHT=600 
SPEED=5 # initial speed 
SCORE=0 # результаты игрока
COINS_COLLECTED=0  # собирание монеток
# экран редачим
DISPLAYSURF=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

#ну шрифты
font=pygame.font.SysFont("Verdana", 20)

class Enemy(pygame.sprite.Sprite): # класс для врагов от спрайта
    def __init__(self):
        super().__init__() 
        self.image =pygame.image.load("Enemy.png")
        self.rect=self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40), 0) # рандом позиция
    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)
        if (self.rect.top>SCREEN_HEIGHT):#прверяем чтоб не выходило за границы
            SCORE+=1
            self.rect.top=0
            self.rect.center=(random.randint(30, 370), 0) 
class Player(pygame.sprite.Sprite):# класс игрока
    def __init__(self):
        super().__init__() 
        self.image=pygame.image.load("Player.png")
        self.rect=self.image.get_rect()
        self.rect.center=(160, 520)
        
    def move(self):
        pressed_keys=pygame.key.get_pressed()
        if self.rect.left>0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right<SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# новый класс для экстра тасков
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # поверхность для монт
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        #желтий круг 
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        pygame.draw.circle(self.image, (200, 200, 0), (15, 15), 12)  # Inner circle
        self.rect = self.image.get_rect()
        # рондомная позиция сверху
        self.rect.center=(random.randint(40, SCREEN_WIDTH-40), 0)
        self.weight=random.choice([1, 2, 3])  # значение монет 
    
    def move(self):#функция для перемещение монет
        self.rect.move_ip(0, 3)  # Coins fall slower than enemies
        if self.rect.top>SCREEN_HEIGHT:
            self.rect.top=0
            self.rect.center=(random.randint(30, 370), 0)

P1=Player()
E1= Enemy()

# спрайтерский клуб 
enemies=pygame.sprite.Group()
enemies.add(E1)
coins= pygame.sprite.Group()  #экстр таск
all_sprites =pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)

# изначальные коины
for i in range(2):  #начнем с 2 
    C=Coin()
    coins.add(C)
    all_sprites.add(C)

#экстра таск новые ивенты 
INC_SPEED=pygame.USEREVENT+1
pygame.time.set_timer(INC_SPEED, 1000)

# ивенты для получения коинов
SPAWN_COIN=pygame.USEREVENT +2
pygame.time.set_timer(SPAWN_COIN, 2000)  # монета через каждые 2 сек 

#луп
while True:
       
    for event in pygame.event.get():
        if event.type ==INC_SPEED:
            SPEED+=0.5  # увеличение скорости ред
        if event.type==SPAWN_COIN:  #создание новой монеты
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type == QUIT:# выход из игры
            pygame.quit()
            sys.exit()

    DISPLAYSURF.fill(WHITE) #чистый экран

    # счет игрока и монеты 
    scores=font.render(f"Score: {SCORE}", True, BLACK)
    coins_text=font.render(f"Coins: {COINS_COLLECTED}", True, BLACK)  # NEW: Coin counter
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (300, 10))  # в правом верхнем углу счет монет

    #отрисовка всех sprites
    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # NEW: Coin collection
    coins_collected=pygame.sprite.spritecollide(P1, coins, True)
    for coin in coins_collected:
        COINS_COLLECTED+=coin.weight  # изменения количества монет
        new_coin=Coin() # создание новой монеты взамен собранной
        coins.add(new_coin)
        all_sprites.add(new_coin)

    if pygame.sprite.spritecollideany(P1, enemies):
        DISPLAYSURF.fill(RED) # при столкновений экран будет красным
        game_over=font.render("Game Over", True, WHITE) # отображение конца игры
        final_score = font.render(f"Final Score: {SCORE}", True, WHITE)
        final_coins = font.render(f"Coins Collected: {COINS_COLLECTED}", True, WHITE)  # NEW
        DISPLAYSURF.blit(game_over, (SCREEN_WIDTH//2 - 70, SCREEN_HEIGHT//2 - 50))
        DISPLAYSURF.blit(final_score, (SCREEN_WIDTH//2 - 80, SCREEN_HEIGHT//2))
        DISPLAYSURF.blit(final_coins, (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 30))  # NEW
        pygame.display.update()
        # удаление всего
        for entity in all_sprites:
            entity.kill() 
        time.sleep(3) # пайза перед закрытием 3 сек
        pygame.quit()
        sys.exit()        
         
    pygame.display.update() # обновление экрана
    FramePerSec.tick(FPS) # контроль фпс