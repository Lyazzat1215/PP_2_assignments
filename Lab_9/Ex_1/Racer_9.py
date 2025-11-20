import pygame, sys
from pygame.locals import *
import random, time
 
pygame.init()
FPS=60
FramePerSec=pygame.time.Clock()
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
SCORE = 0
COINS_COLLECTED = 0  #новая переменная для подсчета монет
 
DISPLAYSURF=pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
pygame.display.set_caption("Game")

font = pygame.font.SysFont("Verdana", 20)
 
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Загрузка изображения врага из файла
        self.image=pygame.image.load("Enemy.png")
        self.rect=self.image.get_rect()
        self.rect.center=(random.randint(40,SCREEN_WIDTH-40), 0)    
 
    def move(self):
        global SCORE
        # Перемещение врага вниз
        self.rect.move_ip(0,SPEED)
        # Если враг ушел за нижнюю границу экрана
        if (self.rect.top>SCREEN_HEIGHT):
            SCORE+=1 # Увеличиваем счет за уклонение
            # Возвращаем врага наверх в случайной позиции
            self.rect.top=0
            self.rect.center=(random.randint(30, 370), 0)
 
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        # Загрузка изображения игрока из файла
        self.image=pygame.image.load("Player.png")
        self.rect=self.image.get_rect()
        # Установка начальной позиции игрока
        self.rect.center=(160, 520)
        
    def move(self):
        # Получение состояния всех клавиш
        pressed_keys = pygame.key.get_pressed()
      
        # Движение влево с проверкой границы экрана
        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        # Движение вправо с проверкой границы экрана
        if self.rect.right < SCREEN_WIDTH:        
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

# Класс для монет, которые можно собирать
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Создание поверхности для монеты
        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        # Рисование желтого круга монеты
        pygame.draw.circle(self.image, YELLOW, (15, 15), 15)
        # Рисование внутреннего круга для эффекта монеты
        pygame.draw.circle(self.image, (200, 200, 0), (15, 15), 12)
        self.rect = self.image.get_rect()
        # Случайная позиция вверху экрана
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)
        # Случайное значение монеты (1, 2 или 3 очка)
        self.weight=random.choice([1, 2, 3])
    
    def move(self):
        # Перемещение монеты вниз
        self.rect.move_ip(0, 3)
        # Если монета ушла за нижнюю границу
        if self.rect.top>SCREEN_HEIGHT:
            # Возвращаем монету наверх в новой позиции
            self.rect.top=0
            self.rect.center=(random.randint(30, 370), 0)
 
P1=Player()
E1=Enemy()
Groups
enemies=pygame.sprite.Group()
enemies.add(E1)
coins=pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(E1)
 
# Создание начальных монет
for i in range(3):
    C=Coin()
    coins.add(C)
    all_sprites.add(C)
 
INC_SPEED=pygame.USEREVENT+1
pygame.time.set_timer(INC_SPEED, 1000)

# Событие для создания новых монет
SPAWN_COIN=pygame.USEREVENT+2
pygame.time.set_timer(SPAWN_COIN, 2000)  # Новая монета каждые 2 секунды
 
#Game Loop
while True:
       
    for event in pygame.event.get():
        if event.type==INC_SPEED:
              SPEED+=0.5
        # Обработка создания новой монеты
        if event.type==SPAWN_COIN:
            new_coin=Coin()
            coins.add(new_coin)
            all_sprites.add(new_coin)
        if event.type==QUIT:
            pygame.quit()
            sys.exit()
 
    DISPLAYSURF.fill(WHITE)
    scores=font.render(f"Score: {SCORE}", True, BLACK)
    coins_text =font.render(f"Coins: {COINS_COLLECTED}", True, BLACK)
    DISPLAYSURF.blit(scores, (10, 10))
    DISPLAYSURF.blit(coins_text, (300, 10))  # Счетчик монет в правом верхнем углу
 
    for entity in all_sprites:
        # Отрисовка каждого спрайта
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    # Проверка сбора монет
    coins_collected=pygame.sprite.spritecollide(P1, coins, True)
    for coin in coins_collected:
        COINS_COLLECTED+=coin.weight
        new_coin=Coin()
        coins.add(new_coin)
        all_sprites.add(new_coin)
 
    if pygame.sprite.spritecollideany(P1, enemies):
          DISPLAYSURF.fill(RED)
          # Отображение сообщения о конце игры
          game_over=font.render("Game Over", True, WHITE)
          final_score=font.render(f"Final Score: {SCORE}", True, WHITE)
          final_coins=font.render(f"Coins Collected: {COINS_COLLECTED}", True, WHITE)
          DISPLAYSURF.blit(game_over, (SCREEN_WIDTH//2-70, SCREEN_HEIGHT//2-50))
          DISPLAYSURF.blit(final_score, (SCREEN_WIDTH//2-80, SCREEN_HEIGHT//2))
          DISPLAYSURF.blit(final_coins, (SCREEN_WIDTH//2-100, SCREEN_HEIGHT//2+30))
          pygame.display.update()
          for entity in all_sprites:
                entity.kill() 
          time.sleep(3)
          pygame.quit()
          sys.exit()        
    FramePerSec.tick(FPS)