import pygame
import sys
import random
import json
import psycopg2
from datetime import datetime

class GameDatabase:
    def __init__(self):
        self.conn =psycopg2.connect(
            host="localhost",
            database="firstDB",
            user="postgres",
            password="1215"
        )
        self.create_tables()
    
    def create_tables(self):
        with self.conn.cursor() as cur:
            cur.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    username VARCHAR(50) UNIQUE NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            cur.execute("""
                CREATE TABLE IF NOT EXISTS user_scores (
                    id SERIAL PRIMARY KEY,
                    user_id INTEGER REFERENCES users(id) ON DELETE CASCADE,
                    score INTEGER DEFAULT 0,
                    level INTEGER DEFAULT 1,
                    speed INTEGER DEFAULT 10,
                    walls TEXT,
                    saved_state TEXT,
                    played_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            self.conn.commit()
    
    def get_or_create_user(self, username):
        with self.conn.cursor() as cur:
            cur.execute("SELECT id FROM users WHERE username=%s", (username,))
            user=cur.fetchone()
            
            if user:
                user_id=user[0]
                print(f"Добро пожаловать, {username}")
            else:
                cur.execute(
                    "INSERT INTO users (username) VALUES (%s) RETURNING id",
                    (username,)
                )
                user_id=cur.fetchone()[0]
                print(f"Новый пользователь {username} создан")
            
            self.conn.commit()
            return user_id
    
    def get_user_stats(self, user_id):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT score, level, speed 
                FROM user_scores 
                WHERE user_id = %s 
                ORDER BY played_at DESC 
                LIMIT 1
            """, (user_id,))
            stats=cur.fetchone()
            
            if stats:
                return {
                    "score": stats[0],
                    "level": stats[1],
                    "speed": stats[2]
                }
            return {"score": 0, "level": 1, "speed": 10}
    
    def save_game_state(self, user_id, score, level, speed, walls, snake_body, food_pos):
        saved_state = json.dumps({
            "snake_body": snake_body,
            "food_pos": food_pos,
            "timestamp": str(datetime.now())
        })
        
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO user_scores 
                (user_id, score, level, speed, walls, saved_state) 
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (user_id, score, level, speed, json.dumps(walls), saved_state))
            self.conn.commit()
        print("Игра сохранена")
    
    def get_top_scores(self, limit=5):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT u.username, us.score, us.level, us.played_at
                FROM user_scores us
                JOIN users u ON u.id = us.user_id
                ORDER BY us.score DESC, us.level DESC
                LIMIT %s
            """, (limit,))
            return cur.fetchall()

class SnakeGame:
    def __init__(self, username):
        self.db =GameDatabase()
        self.user_id=self.db.get_or_create_user(username)
        self.stats=self.db.get_user_stats(self.user_id)
        
        self.WIDTH, self.HEIGHT=800, 600
        self.GRID_SIZE=20
        self.FPS=self.stats["speed"]
        self.level=self.stats["level"]
        self.scor =self.stats["score"]
    
        self.BLACK=(0, 0, 0)
        self.GREEN =(0, 255, 0)
        self.RED=(255, 0, 0)
        self.WHITE=(255, 255, 255)
        self.BLUE=(0, 120, 255)
        self.WALL_COLOR=(100, 100, 100)
    
        pygame.init()
        self.screen=pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption(f"Snake Game-{username} | Level: {self.level}")
        self.clock=pygame.time.Clock()
        
        self.walls = self.generate_walls()
        self.snake=[(self.WIDTH//2, self.HEIGHT//2)]
        self.direction=(self.GRID_SIZE, 0)
        self.food=self.generate_food()
        self.game_paused=False
        self.font=pygame.font.SysFont(None, 36)
        self.small_font=pygame.font.SysFont(None, 24)
    
    def generate_walls(self):
        walls=[]
        if self.level==1:
            for x in range(0, self.WIDTH, self.GRID_SIZE):
                walls.append((x, 0))
                walls.append((x, self.HEIGHT-self.GRID_SIZE))
            for y in range(0, self.HEIGHT, self.GRID_SIZE):
                walls.append((0, y))
                walls.append((self.WIDTH-self.GRID_SIZE, y))
        
        elif self.level==2:
            walls=[(x, 100) for x in range(200, 600, self.GRID_SIZE)]
            walls+=[(x, 400) for x in range(200, 600, self.GRID_SIZE)]
        
        elif self.level >=3:
            for x in range(100, 700, 100):
                for y in range(100, 500, 100):
                    if random.random()>0.3:
                        walls.append((x, y))
        
        return walls
    
    def generate_food(self):
        while True:
            x=random.randint(1, (self.WIDTH//self.GRID_SIZE)-2)*self.GRID_SIZE
            y=random.randint(1, (self.HEIGHT//self.GRID_SIZE)-2) *self.GRID_SIZE
            if (x, y) not in self.snake and (x, y) not in self.walls:
                return (x, y)
    
    def draw(self):
        self.screen.fill(self.BLACK)
        for wall in self.walls:
            pygame.draw.rect(self.screen, self.WALL_COLOR, 
                           (*wall, self.GRID_SIZE, self.GRID_SIZE))
        for i, segment in enumerate(self.snake):
            color=self.GREEN if i==0 else (0, 200, 0)
            pygame.draw.rect(self.screen, color, 
                           (*segment, self.GRID_SIZE, self.GRID_SIZE))
        pygame.draw.rect(self.screen, self.RED, 
                       (*self.food, self.GRID_SIZE, self.GRID_SIZE))

        score_text=self.font.render(f"Score: {self.score}", True, self.WHITE)
        level_text=self.font.render(f"Level: {self.level}", True, self.WHITE)
        pause_text =self.small_font.render("P - Пауза | S - Сохранить | ESC - Выход", True, self.WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (10, 50))
        self.screen.blit(pause_text, (10, self.HEIGHT-30))
        
        if self.game_paused:
            pause_msg = self.font.render("пауза", True, self.RED)
            self.screen.blit(pause_msg, (self.WIDTH//2-50, self.HEIGHT//2))
        
        pygame.display.flip()
    
    def move_snake(self):
        if self.game_paused:
            return
        
        head_x, head_y=self.snake[0]
        dx, dy=self.direction
        new_head=(head_x + dx, head_y + dy)
        if (new_head in self.snake or 
            new_head in self.walls or
            new_head[0] < 0 or new_head[0]>=self.WIDTH or
            new_head[1] < 0 or new_head[1]>=self.HEIGHT):
            self.game_over()
            return False
        
        self.snake.insert(0, new_head)
        if new_head==self.food:
            self.score+=10*self.level
            self.food=self.generate_food()
            
            if self.score%100==0:
                self.level+=1
                self.FPS+=2 
                self.walls=self.generate_walls()
                print(f" Уровень {self.level}! Скорость: {self.FPS}")
        else:
            self.snake.pop()
        
        return True
    
    def game_over(self):
        print(f" Game Over! Final Score: {self.score}")
    
        self.db.save_game_state(
            self.user_id, 
            self.score, 
            self.level, 
            self.FPS,
            self.walls,
            self.snake,
            self.food
        )
        
        self.show_leaders()
        
        pygame.quit()
        sys.exit()
    
    def show_leaders(self):
        print("\n" + "="*40)
        print("Leader positions")
        print("="*40)
        
        top_scores=self.db.get_top_scores(5)
        for i, (username, score, level, date) in enumerate(top_scores, 1):
            print(f"{i}. {username}: {score} (Уровень {level})")
    
    def run(self):
        running=True
        
        while running:
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    running=False
                
                elif event.type==pygame.KEYDOWN:
                    if event.key==pygame.K_ESCAPE:
                        running=False
                    
                    elif event.key==pygame.K_UP and self.direction !=(0, self.GRID_SIZE):
                        self.direction=(0, -self.GRID_SIZE)
                    elif event.key==pygame.K_DOWN and self.direction !=(0, -self.GRID_SIZE):
                        self.direction=(0, self.GRID_SIZE)
                    elif event.key==pygame.K_LEFT and self.direction !=(self.GRID_SIZE, 0):
                        self.direction=(-self.GRID_SIZE, 0)
                    elif event.key==pygame.K_RIGHT and self.direction !=(-self.GRID_SIZE, 0):
                        self.direction=(self.GRID_SIZE, 0)
                    
                    elif event.key==pygame.K_p:
                        self.game_paused=not self.game_paused
                        print("Пауза" if self.game_paused else "Продолжить")
                    
                    elif event.key==pygame.K_s and self.game_paused:
                        self.db.save_game_state(
                            self.user_id,
                            self.score,
                            self.level,
                            self.FPS,
                            self.walls,
                            self.snake,
                            self.food
                        )
            
            if self.move_snake():
                self.draw()
                self.clock.tick(self.FPS)
            else:
                running=False
        
        pygame.quit()

if __name__=="__main__":
    print("="*40)
    print("SNAKE GAME WITH POSTGRESQL")
    print("="*40)

    username=input("Введите имя: ").strip()
    
    if not username:
        print("Имя обязательно!")
        sys.exit()
    
    game=SnakeGame(username)
    game.run()