#библиотеки
import pygame, sys
from pygame.locals import* #импорт констант pygame
import random, time
#Initializing 
pygame.init()
# константы
WINDOW_WIDTH=800
WINDOW_HEIGHT=600
GRID_SIZE=20
GRID_WIDTH=WINDOW_WIDTH//GRID_SIZE
GRID_HEIGHT =WINDOW_HEIGHT//GRID_SIZE

#цвета
BLACK=(0, 0, 0)
WHITE=(255, 255, 255)
GREEN=(0, 255, 0)
RED=(255, 0, 0)
BLUE=(0, 0, 255)
GRAY=(100, 100, 100)

# напрвления
UP=(0, -1)
DOWN=(0, 1)
LEFT=(-1, 0)
RIGHT=(1, 0)

#экран
DISPLAY_SURF= pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
FONT=pygame.font.Font(None, 36)
SMALL_FONT=pygame.font.Font(None, 24)
#фпс часы для контролирования скоростии игры
FPS_CLOCK=pygame.time.Clock()

class Snake:
    def __init__(self):
        # Изначальная позиция и апрвление змеи
        self.positions=[(GRID_WIDTH//2, GRID_HEIGHT//2)]  #начинаем с центра
        self.direction=RIGHT
        self.next_direction=RIGHT
        self.grow=False
        self.color=GREEN# зелений змей
        
    def get_head_position(self):#позицтя головы змеи
        return self.positions[0]
    
    def update(self):
        current_head=self.get_head_position()
        x, y=self.next_direction
        self.direction=self.next_direction
        
        #расчитываем новые позиций головы 
        new_head=((current_head[0]+x)% GRID_WIDTH, (current_head[1] + y) % GRID_HEIGHT)
        
        #проверяем чтобы когда змея касалась себя то игра заканчивалась
        if new_head in self.positions[1:]:
            return False  #Game over
        
        #новая позиция головы
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow= False
            
        return True  #игра прдолжается
    
    def reset(self):#возвращаем изн позицию
        self.positions=[(GRID_WIDTH//2, GRID_HEIGHT// 2)]
        self.direction=RIGHT
        self.next_direction=RIGHT
        self.grow =False
    
    def render(self, surface):
        for position in self.positions:
            rect =pygame.Rect(position[0]*GRID_SIZE, position[1]*GRID_SIZE, 
                             GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1) 

class Food:
    def __init__(self, snake_positions):
        # появление еды в рандомном месте
        self.position=self.get_random_position(snake_positions)
        self.color=RED
        
    def get_random_position(self, snake_positions):
        while True:
            position=(random.randint(0, GRID_WIDTH-1), 
                       random.randint(0, GRID_HEIGHT-1))
            
            if position not in snake_positions:
                return position
    
    def render(self, surface):
        rect = pygame.Rect(self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE,
                          GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1

class Wall:
    def __init__(self):# делаем стены 
        self.positions=[]
        self.create_walls()
        self.color=GRAY
        
    def create_walls(self):
        for x in range(GRID_WIDTH):
            self.positions.append((x, 0))  #верхняя
            self.positions.append((x, GRID_HEIGHT-1))  # нижняя
        
        for y in range(1, GRID_HEIGHT-1):
            self.positions.append((0, y))  #левый
            self.positions.append((GRID_WIDTH-1, y))  # правый
    
    def render(self, surface):
        for position in self.positions:
            rect=pygame.Rect(position[0]*GRID_SIZE, position[1]*GRID_SIZE,
                              GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)
class Game:
    def __init__(self):
        # готовим осн состовляющие игры
        self.snake=Snake()
        self.wall=Wall()
        self.food=Food(self.snake.positions)
        self.score=0
        self.level=1
        self.foods_eaten=0
        self.foods_per_level=3
        self.base_speed=10 
        self.speed =self.base_speed
        self.frame_count = 0
        self.game_over=False
        
    def update(self):
        # обновление
        if self.game_over:
            return
        
        self.frame_count+=1
        
        if self.frame_count>=self.speed:
            self.frame_count= 0
            
            #обновляем позицию змеи
            if not self.snake.update():
                self.game_over=True
                return
        
            head_position=self.snake.get_head_position()
            if head_position in self.wall.positions:
                self.game_over=True
                return
            
            if head_position==self.food.position:
                self.snake.grow=True
                self.score+=10*self.level 
                self.foods_eaten+=1
                
                if self.foods_eaten>=self.foods_per_level:
                    self.level_up()
                    self.food=Food(self.snake.positions)
    
    def level_up(self):
        self.level+=1
        self.foods_eaten=0
        self.speed=max(5, self.base_speed-(self.level -1)*1)
    
    def handle_keys(self):
            if event.type==QUIT:
                pygame.quit()
                sys.exit()
            elif event.type==KEYDOWN:
                if self.game_over:
                    if event.key==K_r:
                        self.reset_game()
                else:
                    if event.key==K_UP and self.snake.direction != DOWN:
                        self.snake.next_direction=UP
                    elif event.key==K_DOWN and self.snake.direction != UP:
                        self.snake.next_direction=DOWN
                    elif event.key==K_LEFT and self.snake.direction != RIGHT:
                        self.snake.next_direction=LEFT
                    elif event.key==K_RIGHT and self.snake.direction != LEFT:
                        self.snake.next_direction=RIGHT
    
    def reset_game(self):
        self.snake.reset()
        self.food=Food(self.snake.positions)
        self.score=0
        self.level=1
        self.foods_eaten=0
        self.speed=self.base_speed
        self.frame_count=0
        self.game_over=False
    
    def render(self):
        
        self.wall.render(DISPLAY_SURF)
        self.snake.render(DISPLAY_SURF)
        self.food.render(DISPLAY_SURF)
        
        score_text=FONT.render(f'Score: {self.score}', True, WHITE)
        level_text=FONT.render(f'Level: {self.level}', True, WHITE)
        foods_text= SMALL_FONT.render(f'Foods: {self.foods_eaten}/{self.foods_per_level}', True, WHITE)
        speed_text=SMALL_FONT.render(f'Speed: {self.speed}', True, WHITE)
        
        DISPLAY_SURF.blit(score_text, (10, 10))
        DISPLAY_SURF.blit(level_text, (10, 50))
        DISPLAY_SURF.blit(foods_text, (10, 90))
        DISPLAY_SURF.blit(speed_text, (10, 110))
        
        if self.game_over:
            game_over_text=FONT.render('GAME OVER! Press R to restart', True, RED)
            text_rect=game_over_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
            DISPLAY_SURF.blit(game_over_text, text_rect)
            
            final_score_text=FONT.render(f'Final Score: {self.score}', True, WHITE)
            final_level_text =FONT.render(f'Final Level: {self.level}', True, WHITE)
            
            final_score_rect=final_score_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 40))
            final_level_rect=final_level_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 + 80))
            
            DISPLAY_SURF.blit(final_score_text, final_score_rect)
            DISPLAY_SURF.blit(final_level_text, final_level_rect)
        
        pygame.display.update()

def main():
    game=Game()
    #loop
    while True:
        game.handle_keys()
        game.update()
        game.render()
        FPS_CLOCK.tick(60) 
if __name__=='__main__':
    main()