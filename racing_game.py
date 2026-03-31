import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Highway Racer")
clock = pygame.time.Clock()

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
DARK_GRAY = (50, 50, 50)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
BROWN = (139, 69, 19)
GRASS_GREEN = (34, 139, 34)
ROAD_GRAY = (80, 80, 80)

# Game variables
LANES = 3
LANE_WIDTH = SCREEN_WIDTH // LANES
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
ENEMY_WIDTH = 38
ENEMY_HEIGHT = 58
BASE_SPEED = 5
SPEED_INCREASE = 0.2
MAX_SPEED = 12

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 24)

class Player:
    def __init__(self):
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.x = SCREEN_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20
        self.lane = 1  # 0=left, 1=middle, 2=right
        self.speed = BASE_SPEED
        
    def move_left(self):
        if self.lane > 0:
            self.lane -= 1
            self.x = self.lane * LANE_WIDTH + (LANE_WIDTH // 2 - self.width // 2)
    
    def move_right(self):
        if self.lane < LANES - 1:
            self.lane += 1
            self.x = self.lane * LANE_WIDTH + (LANE_WIDTH // 2 - self.width // 2)
    
    def draw(self):
        # Draw car body
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        # Draw windows
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 8, 8, 15))
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 13, self.y + 8, 8, 15))
        # Draw headlights
        pygame.draw.circle(screen, YELLOW, (self.x + 5, self.y + self.height - 5), 4)
        pygame.draw.circle(screen, YELLOW, (self.x + self.width - 5, self.y + self.height - 5), 4)
        # Draw wheels
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + self.height - 10, 8, 8))
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 13, self.y + self.height - 10, 8, 8))
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 5, 8, 8))
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 13, self.y + 5, 8, 8))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Enemy:
    def __init__(self, lane, speed):
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.lane = lane
        self.x = lane * LANE_WIDTH + (LANE_WIDTH // 2 - self.width // 2)
        self.y = -self.height
        self.speed = speed
        self.color = random.choice([RED, GREEN, ORANGE, GRAY])
        
    def update(self):
        self.y += self.speed
        
    def draw(self):
        # Draw enemy car
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
        # Draw windows
        pygame.draw.rect(screen, BLACK, (self.x + 5, self.y + 8, 8, 15))
        pygame.draw.rect(screen, BLACK, (self.x + self.width - 13, self.y + 8, 8, 15))
        # Draw headlights
        pygame.draw.circle(screen, YELLOW, (self.x + 5, self.y + 5), 3)
        pygame.draw.circle(screen, YELLOW, (self.x + self.width - 5, self.y + 5), 3)
        
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Road:
    def __init__(self):
        self.lines = []
        self.line_spacing = 50
        self.line_width = 8
        self.line_height = 30
        self.scroll_y = 0
        
    def update(self, speed):
        self.scroll_y += speed
        if self.scroll_y >= self.line_spacing:
            self.scroll_y = 0
    
    def draw(self):
        # Draw road background
        pygame.draw.rect(screen, ROAD_GRAY, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
        
        # Draw lane dividers
        for i in range(1, LANES):
            x = i * LANE_WIDTH
            pygame.draw.line(screen, WHITE, (x, 0), (x, SCREEN_HEIGHT), 3)
        
        # Draw moving road lines
        for i in range(LANES - 1):
            line_x = (i + 1) * LANE_WIDTH
            for y in range(int(-self.line_height), SCREEN_HEIGHT, self.line_spacing):
                line_y = (y + self.scroll_y) % SCREEN_HEIGHT
                if 0 <= line_y <= SCREEN_HEIGHT:
                    pygame.draw.rect(screen, WHITE, 
                                   (line_x - self.line_width // 2, line_y, 
                                    self.line_width, self.line_height))
        
        # Draw road edges
        pygame.draw.rect(screen, GRASS_GREEN, (0, 0, 20, SCREEN_HEIGHT))
        pygame.draw.rect(screen, GRASS_GREEN, (SCREEN_WIDTH - 20, 0, 20, SCREEN_HEIGHT))
        pygame.draw.line(screen, WHITE, (20, 0), (20, SCREEN_HEIGHT), 3)
        pygame.draw.line(screen, WHITE, (SCREEN_WIDTH - 20, 0), (SCREEN_WIDTH - 20, SCREEN_HEIGHT), 3)

def show_start_screen():
    screen.fill(BLACK)
    title = big_font.render("HIGHWAY RACER", True, WHITE)
    start = font.render("Press SPACE to Start", True, WHITE)
    controls1 = small_font.render("Use LEFT and RIGHT arrows to switch lanes", True, WHITE)
    controls2 = small_font.render("Avoid red, green, and orange cars", True, WHITE)
    controls3 = small_font.render("Survive as long as you can!", True, WHITE)
    
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(start, (SCREEN_WIDTH // 2 - start.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(controls1, (SCREEN_WIDTH // 2 - controls1.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    screen.blit(controls2, (SCREEN_WIDTH // 2 - controls2.get_width() // 2, SCREEN_HEIGHT // 2 + 90))
    screen.blit(controls3, (SCREEN_WIDTH // 2 - controls3.get_width() // 2, SCREEN_HEIGHT // 2 + 120))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def show_game_over(score, high_score):
    screen.fill(BLACK)
    game_over = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    high_score_text = font.render(f"Best: {high_score}", True, YELLOW)
    restart = font.render("Press SPACE to Restart", True, WHITE)
    
    screen.blit(game_over, (SCREEN_WIDTH // 2 - game_over.get_width() // 2, SCREEN_HEIGHT // 2 - 100))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
    screen.blit(high_score_text, (SCREEN_WIDTH // 2 - high_score_text.get_width() // 2, SCREEN_HEIGHT // 2))
    screen.blit(restart, (SCREEN_WIDTH // 2 - restart.get_width() // 2, SCREEN_HEIGHT // 2 + 60))
    
    pygame.display.flip()
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False
    return True

def main():
    # Show start screen
    if not show_start_screen():
        return
    
    # Game variables
    high_score = 0
    running = True
    
    while running:
        # Initialize game objects
        player = Player()
        road = Road()
        enemies = []
        score = 0
        frame_count = 0
        spawn_delay = 80  # Frames between enemy spawns
        current_speed = BASE_SPEED
        
        game_active = True
        
        # Game loop
        while game_active:
            # Handle events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    game_active = False
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        player.move_left()
                    elif event.key == pygame.K_RIGHT:
                        player.move_right()
            
            # Update road scrolling
            road.update(current_speed)
            
            # Spawn enemies
            if frame_count >= spawn_delay:
                # Random lane, avoid spawning on player's lane sometimes
                lane = random.randint(0, LANES - 1)
                enemies.append(Enemy(lane, current_speed))
                frame_count = 0
                # Decrease spawn delay as score increases (more cars)
                spawn_delay = max(40, 80 - score // 50)
            else:
                frame_count += 1
            
            # Update enemies
            for enemy in enemies[:]:
                enemy.update()
                if enemy.y > SCREEN_HEIGHT:
                    enemies.remove(enemy)
                    score += 10
            
            # Check collisions
            player_rect = player.get_rect()
            for enemy in enemies:
                if player_rect.colliderect(enemy.get_rect()):
                    game_active = False
            
            # Increase speed gradually
            current_speed = min(MAX_SPEED, BASE_SPEED + (score // 300) * SPEED_INCREASE)
            
            # Draw everything
            road.draw()
            
            # Draw enemies
            for enemy in enemies:
                enemy.draw()
            
            # Draw player
            player.draw()
            
            # Draw score and speed
            score_text = font.render(f"Score: {score}", True, WHITE)
            speed_text = small_font.render(f"Speed: {int(current_speed * 10)} mph", True, WHITE)
            screen.blit(score_text, (10, 10))
            screen.blit(speed_text, (10, 50))
            
            # Draw lane indicator
            for i in range(LANES):
                if i == player.lane:
                    pygame.draw.rect(screen, YELLOW, 
                                   (i * LANE_WIDTH, SCREEN_HEIGHT - 10, LANE_WIDTH, 5))
            
            pygame.display.flip()
            clock.tick(60)
        
        # Update high score
        if score > high_score:
            high_score = score
        
        # Show game over screen
        if not show_game_over(score, high_score):
            running = False
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()