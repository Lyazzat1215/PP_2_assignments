import pygame
import random
import sys
from pygame.locals import *

pygame.init()
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (100, 100, 100)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
CYAN = (0, 255, 255)

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)
DISPLAY_SURF = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('Snake Game')
FONT = pygame.font.Font(None, 36)
SMALL_FONT = pygame.font.Font(None, 24)
FPS_CLOCK = pygame.time.Clock()

class Snake:
    def __init__(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]  
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
        self.color = GREEN
        
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        current_head = self.get_head_position()
        x, y = self.next_direction
        self.direction = self.next_direction
        new_head = ((current_head[0] + x) % GRID_WIDTH, (current_head[1] + y) % GRID_HEIGHT)
        if new_head in self.positions[1:]:
            return False
        self.positions.insert(0, new_head)
        if not self.grow:
            self.positions.pop()
        else:
            self.grow = False
            
        return True
    
    def reset(self):
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = RIGHT
        self.grow = False
    
    def render(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1] * GRID_SIZE, 
                             GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1) 

class Food:
    def __init__(self, snake_positions, wall_positions):
        self.position = self.get_random_position(snake_positions, wall_positions)
        self.weight = random.choices([1, 2, 3], weights=[70, 20, 10])[0]
        if self.weight == 1:
            self.color = RED
            self.lifetime = 5000 
        elif self.weight == 2:
            self.color = ORANGE
            self.lifetime = 7000
        else:
            self.color = PURPLE
            self.lifetime = 10000  
            
        self.spawn_time = pygame.time.get_ticks()
        self.is_expired = False
        
    def get_random_position(self, snake_positions, wall_positions):
        while True:
            position = (random.randint(1, GRID_WIDTH - 2), 
                       random.randint(1, GRID_HEIGHT - 2))
            if position not in snake_positions and position not in wall_positions:
                return position
    
    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.spawn_time > self.lifetime:
            self.is_expired = True
    
    def get_remaining_time(self):
        current_time=pygame.time.get_ticks()
        remaining = max(0, self.lifetime-(current_time - self.spawn_time))
        return remaining/1000  
    
    def render(self, surface):
        rect = pygame.Rect(self.position[0]*GRID_SIZE, self.position[1]*GRID_SIZE,
                          GRID_SIZE, GRID_SIZE)
        if self.weight == 1:
            pygame.draw.rect(surface, self.color, rect)
        elif self.weight==2:
            points = [
                (rect.centerx, rect.top),
                (rect.right, rect.centery),
                (rect.centerx, rect.bottom),
                (rect.left, rect.centery)
            ]
            pygame.draw.polygon(surface, self.color, points)
        else: 
            pygame.draw.rect(surface, self.color, rect)
            inner_rect = pygame.Rect(
                rect.left + 4, rect.top + 4,
                rect.width - 8, rect.height - 8
            )
            pygame.draw.rect(surface, YELLOW, inner_rect)
        
        pygame.draw.rect(surface, BLACK, rect, 1)
        if self.weight > 1:
            weight_text=SMALL_FONT.render(str(self.weight), True, WHITE)
            text_rect =weight_text.get_rect(center=rect.center)
            surface.blit(weight_text, text_rect)
        if not self.is_expired:
            time_remaining=self.get_remaining_time()
            total_time=self.lifetime/1000
            percentage=time_remaining/total_time
            timer_height =3
            timer_width=GRID_SIZE
            timer_rect=pygame.Rect(
                rect.left, rect.top-timer_height-2,
                timer_width * percentage, timer_height
            )
            timer_color=(
                int(255*(1-percentage)),
                int(255*percentage),
                0
            )
            pygame.draw.rect(surface, timer_color, timer_rect)

class Wall:
    def __init__(self):
        self.positions=[]
        self.create_walls()
        self.color = GRAY
        
    def create_walls(self):
        for x in range(GRID_WIDTH):
            self.positions.append((x, 0))
            self.positions.append((x, GRID_HEIGHT - 1))
        
        for y in range(1, GRID_HEIGHT - 1):
            self.positions.append((0, y))  
            self.positions.append((GRID_WIDTH-1, y))
    
    def render(self, surface):
        for position in self.positions:
            rect = pygame.Rect(position[0] * GRID_SIZE, position[1]*GRID_SIZE,
                              GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Game:
    def __init__(self):
        # Initialize game state
        self.snake=Snake()
        self.wall=Wall()
        self.foods=[] 
        self.score=0
        self.level=1
        self.foods_eaten=0
        self.foods_per_level=5
        self.base_speed=10 
        self.speed=self.base_speed
        self.frame_count=0
        self.game_over=False
        self.spawn_food_timer=0
        self.max_foods=3  
        self.spawn_food()
        
    def spawn_food(self):
        if len(self.foods)<self.max_foods:
            new_food=Food(self.snake.positions, self.wall.positions)
            self.foods.append(new_food)
    
    def update(self):
        if self.game_over:
            return
        
        self.frame_count+=1
        for food in self.foods[:]:
            food.update()
            if food.is_expired:
                self.foods.remove(food)
        self.spawn_food_timer+=1
        if self.spawn_food_timer>=180:
            self.spawn_food()
            self.spawn_food_timer=0
        if self.frame_count>=self.speed:
            self.frame_count=0
  
            if not self.snake.update():
                self.game_over=True
                return

            head_position=self.snake.get_head_position()
            if head_position in self.wall.positions:
                self.game_over=True
                return
            
            for food in self.foods[:]:
                if head_position==food.position:
                    self.snake.grow=True
                    points=10*self.level*food.weight 
                    self.score+=points
                    self.foods_eaten+=1
                    self.foods.remove(food)
                    self.show_points_popup(head_position, points)
                    if self.foods_eaten>=self.foods_per_level:
                        self.level_up()
                    self.spawn_food()
                    break
    
    def show_points_popup(self, position, points):
        points_text=SMALL_FONT.render(f"+{points}", True, CYAN)
        popup_rect=points_text.get_rect(
            center=(position[0]*GRID_SIZE+GRID_SIZE//2, 
                   position[1]*GRID_SIZE-10)
        )
        DISPLAY_SURF.blit(points_text, popup_rect)
        pygame.display.update()
        pygame.time.delay(100)
    
    def level_up(self):
        self.level+=1
        self.foods_eaten=0
        self.speed=max(5, self.base_speed-(self.level-1))
        if self.level %3==0:
            self.max_foods+=1
    
    def handle_keys(self):
        for event in pygame.event.get():
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
        self.foods=[]
        self.score=0
        self.level=1
        self.foods_eaten=0
        self.speed=self.base_speed
        self.frame_count=0
        self.game_over=False
        self.spawn_food_timer=0
        self.max_foods=3
        self.spawn_food()
    
    def render(self):
        DISPLAY_SURF.fill(BLACK)
        self.wall.render(DISPLAY_SURF)
        for food in self.foods:
            food.render(DISPLAY_SURF)
        self.snake.render(DISPLAY_SURF)
        score_text=FONT.render(f'Score: {self.score}', True, WHITE)
        level_text=FONT.render(f'Level: {self.level}', True, WHITE)
        foods_text=SMALL_FONT.render(f'Foods: {self.foods_eaten}/{self.foods_per_level}', True, WHITE)
        speed_text=SMALL_FONT.render(f'Speed: {self.speed}', True, WHITE)
        active_foods_text=SMALL_FONT.render(f'Active Foods: {len(self.foods)}/{self.max_foods}', True, WHITE)
        
        DISPLAY_SURF.blit(score_text, (10, 10))
        DISPLAY_SURF.blit(level_text, (10, 50))
        DISPLAY_SURF.blit(foods_text, (10, 90))
        DISPLAY_SURF.blit(speed_text, (10, 110))
        DISPLAY_SURF.blit(active_foods_text, (10, 130))
        
        if self.game_over:
            game_over_text=FONT.render('GAME OVER! Press R to restart', True, RED)
            text_rect=game_over_text.get_rect(center=(WINDOW_WIDTH //2, WINDOW_HEIGHT//2))
            DISPLAY_SURF.blit(game_over_text, text_rect)
            
            final_score_text=FONT.render(f'Final Score: {self.score}', True, WHITE)
            final_level_text =FONT.render(f'Final Level: {self.level}', True, WHITE)
            
            final_score_rect=final_score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT // 2+40))
            final_level_rect=final_level_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT // 2+80))
            
            DISPLAY_SURF.blit(final_score_text, final_score_rect)
            DISPLAY_SURF.blit(final_level_text, final_level_rect)
        pygame.display.update()

def main():
    game=Game()
    while True:
        game.handle_keys()
        game.update()
        game.render()
        FPS_CLOCK.tick(60)

if __name__=='__main__':
    main()