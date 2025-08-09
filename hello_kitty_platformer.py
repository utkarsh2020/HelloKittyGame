import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 235)  # Sky blue
GREEN = (0, 255, 0)
RED = (255, 0, 0)
PINK = (255, 192, 203)
YELLOW = (255, 255, 0)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
# Additional colors for coastal theme
OCEAN_BLUE = (0, 119, 190)
DEEP_OCEAN = (0, 82, 147)
SAND = (238, 203, 173)
PALM_GREEN = (34, 139, 34)
COCONUT_BROWN = (101, 67, 33)
SUN_YELLOW = (255, 223, 0)
DOLPHIN_GRAY = (128, 128, 128)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hello Kitty Platformer")
clock = pygame.time.Clock()

class HelloKitty:
    def __init__(self):
        self.width = 40
        self.height = 40
        self.x = 100
        self.y = SCREEN_HEIGHT - self.height - 60
        self.speed = 6
        self.jump_power = -16
        self.gravity = 0.8
        self.velocity = 0
        self.is_jumping = False
        self.on_ground = False
        self.lives = 3
        self.score = 0
        self.has_power_up = False
        self.power_up_timer = 0
        self.invincible = False
        self.invincible_timer = 0

    def update(self, platforms):
        keys = pygame.key.get_pressed()
        
        # Horizontal movement
        if keys[K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        
        # Jumping
        if keys[K_SPACE] and self.on_ground:
            self.velocity = self.jump_power
            self.is_jumping = True
            self.on_ground = False
        
        # Apply gravity
        if not self.on_ground:
            self.velocity += self.gravity
            self.y += self.velocity
        
        # Check platform collisions
        self.on_ground = False
        player_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        
        for platform in platforms:
            platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
            if player_rect.colliderect(platform_rect):
                if self.velocity > 0:  # Falling down
                    self.y = platform.y - self.height
                    self.velocity = 0
                    self.on_ground = True
                    self.is_jumping = False
        
        # Check ground collision
        if self.y > SCREEN_HEIGHT - self.height - 60:
            self.y = SCREEN_HEIGHT - self.height - 60
            self.velocity = 0
            self.on_ground = True
            self.is_jumping = False
        
        # Update power-up timer
        if self.has_power_up:
            self.power_up_timer -= 1
            if self.power_up_timer <= 0:
                self.has_power_up = False
                self.speed = 6
        
        # Update invincibility timer
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False

    def draw(self, screen):
        # Use PNG image if available, otherwise fallback to drawn sprite
        if hello_kitty_image:
            # Apply invincibility effect by modifying the image
            if self.invincible and (self.invincible_timer // 5) % 2:
                # Create a semi-transparent version for blinking effect
                temp_surface = hello_kitty_image.copy()
                temp_surface.set_alpha(128)
                screen.blit(temp_surface, (self.x, self.y))
            else:
                screen.blit(hello_kitty_image, (self.x, self.y))
            
            # Power-up indicator (golden outline when powered up)
            if self.has_power_up:
                # Golden glow around Hello Kitty
                pygame.draw.rect(screen, YELLOW, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 3)
        else:
            # Fallback to drawn sprite if image not available
            color = WHITE if not self.invincible or (self.invincible_timer // 5) % 2 else (200, 200, 200)
            
            # Body (rounded rectangle)
            body_rect = pygame.Rect(self.x + 5, self.y + 18, self.width - 10, self.height - 18)
            pygame.draw.ellipse(screen, color, body_rect)
            pygame.draw.rect(screen, color, (self.x + 5, self.y + 25, self.width - 10, self.height - 25))
            
            # Head (large circle)
            head_center = (self.x + self.width // 2, self.y + 12)
            pygame.draw.circle(screen, color, head_center, 15)
            
            # Hello Kitty's iconic red bow (always present on left side)
            pygame.draw.circle(screen, RED, (self.x + 8, self.y + 5), 2)
            bow_left_wing = [(self.x + 2, self.y + 3), (self.x + 6, self.y + 5), (self.x + 2, self.y + 7)]
            bow_right_wing = [(self.x + 10, self.y + 3), (self.x + 14, self.y + 5), (self.x + 10, self.y + 7)]
            pygame.draw.polygon(screen, RED, bow_left_wing)
            pygame.draw.polygon(screen, RED, bow_right_wing)
            
            # Power-up indicator
            if self.has_power_up:
                pygame.draw.circle(screen, YELLOW, head_center, 17, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Platform:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.top = y
        self.bottom = y + height
        self.left = x
        self.right = x + width
    
    def colliderect(self, rect):
        return pygame.Rect(self.x, self.y, self.width, self.height).colliderect(rect)
    
    def draw(self, screen):
        pygame.draw.rect(screen, BROWN, (self.x, self.y, self.width, self.height))
        pygame.draw.rect(screen, BLACK, (self.x, self.y, self.width, self.height), 2)

class Kiromi:
    def __init__(self, x, y=None, enemy_type="normal"):
        self.width = 35
        self.height = 35
        self.x = x
        self.y = y if y else SCREEN_HEIGHT - self.height - 60
        self.speed = 2
        self.direction = -1
        self.enemy_type = enemy_type
        self.jump_timer = 0
        self.velocity = 0
        
        if enemy_type == "fast":
            self.speed = 4
        elif enemy_type == "jumper":
            self.speed = 1

    def update(self, platforms):
        if self.enemy_type == "jumper":
            self.jump_timer += 1
            if self.jump_timer > 60:  # Jump every second
                self.velocity = -12
                self.jump_timer = 0
            
            # Apply gravity
            self.velocity += 0.8
            self.y += self.velocity
            
            # Check platform collisions
            enemy_rect = pygame.Rect(self.x, self.y, self.width, self.height)
            for platform in platforms:
                platform_rect = pygame.Rect(platform.x, platform.y, platform.width, platform.height)
                if enemy_rect.colliderect(platform_rect) and self.velocity > 0:
                    self.y = platform.y - self.height
                    self.velocity = 0
            
            # Ground collision
            if self.y > SCREEN_HEIGHT - self.height - 60:
                self.y = SCREEN_HEIGHT - self.height - 60
                self.velocity = 0
        
        # Horizontal movement
        self.x += self.speed * self.direction
        
        # Boundary checking
        if self.x < 0 or self.x > SCREEN_WIDTH - self.width:
            self.direction *= -1

    def draw(self, screen):
        # Use PNG image if available, otherwise fallback to drawn sprite
        if kiromi_image:
            # Create colored versions for different enemy types
            if self.enemy_type == "fast":
                # Tint red for fast enemies
                tinted_image = kiromi_image.copy()
                red_overlay = pygame.Surface(kiromi_image.get_size(), pygame.SRCALPHA)
                red_overlay.fill((255, 100, 100, 100))
                tinted_image.blit(red_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted_image, (self.x, self.y))
                
                # Speed lines
                pygame.draw.line(screen, RED, (self.x - 5, self.y + 10), (self.x - 2, self.y + 8), 2)
                pygame.draw.line(screen, RED, (self.x - 5, self.y + 15), (self.x - 2, self.y + 13), 2)
                
            elif self.enemy_type == "jumper":
                # Tint purple for jumper enemies
                tinted_image = kiromi_image.copy()
                purple_overlay = pygame.Surface(kiromi_image.get_size(), pygame.SRCALPHA)
                purple_overlay.fill((200, 100, 200, 100))
                tinted_image.blit(purple_overlay, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                screen.blit(tinted_image, (self.x, self.y))
                
                # Spring effect under feet when on ground
                if self.velocity == 0:
                    pygame.draw.arc(screen, PURPLE, (self.x + 5, self.y + self.height - 8, 25, 8), 0, 3.14, 2)
            else:
                # Normal green kiromi
                screen.blit(kiromi_image, (self.x, self.y))
        else:
            # Fallback to drawn sprite if image not available
            if self.enemy_type == "fast":
                color = RED
                accent_color = (150, 0, 0)
            elif self.enemy_type == "jumper":
                color = PURPLE
                accent_color = (80, 0, 80)
            else:
                color = GREEN
                accent_color = (0, 150, 0)
            
            # Simple fallback drawing
            body_rect = pygame.Rect(self.x + 3, self.y + 15, self.width - 6, self.height - 15)
            pygame.draw.ellipse(screen, color, body_rect)
            head_center = (self.x + self.width // 2, self.y + 10)
            pygame.draw.circle(screen, color, head_center, 12)
            
            # Special effects
            if self.enemy_type == "fast":
                pygame.draw.line(screen, accent_color, (self.x - 5, self.y + 10), (self.x - 2, self.y + 8), 1)
            elif self.enemy_type == "jumper" and self.velocity == 0:
                pygame.draw.arc(screen, accent_color, (self.x + 5, self.y + self.height - 8, 25, 8), 0, 3.14, 2)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Load character images (reload to get updated transparent versions)
def load_images():
    global hello_kitty_image, kiromi_image
    try:
        hello_kitty_image = pygame.image.load("hello kitty.png").convert_alpha()
        hello_kitty_image = pygame.transform.scale(hello_kitty_image, (40, 40))
        print("Successfully loaded hello kitty.png with transparency")
    except:
        hello_kitty_image = None
        print("Could not load hello kitty.png")

    try:
        kiromi_image = pygame.image.load("kiromi.png").convert_alpha()
        kiromi_image = pygame.transform.scale(kiromi_image, (35, 35))
        print("Successfully loaded kiromi.png with transparency")
    except:
        kiromi_image = None
        print("Could not load kiromi.png")

# Load the images
load_images()

class Background:
    def __init__(self):
        pass
    
    def update(self):
        pass  # Static background, no updates needed
    
    def draw(self, screen):
        # Bright sky gradient (lighter and more vibrant)
        for y in range(SCREEN_HEIGHT // 2 + 100):
            color_ratio = y / (SCREEN_HEIGHT // 2 + 100)
            r = int(200 + (255 - 200) * (1 - color_ratio))
            g = int(230 + (255 - 230) * (1 - color_ratio))
            b = int(255)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Sun (brighter and larger)
        sun_center = (SCREEN_WIDTH - 100, 80)
        pygame.draw.circle(screen, (255, 255, 100), sun_center, 45)
        pygame.draw.circle(screen, SUN_YELLOW, sun_center, 40)
        
        # Sun rays (more prominent)
        for i in range(12):
            angle = i * (2 * math.pi / 12)
            start_x = sun_center[0] + math.cos(angle) * 55
            start_y = sun_center[1] + math.sin(angle) * 55
            end_x = sun_center[0] + math.cos(angle) * 75
            end_y = sun_center[1] + math.sin(angle) * 75
            pygame.draw.line(screen, (255, 255, 150), (start_x, start_y), (end_x, end_y), 4)
        
        # Static ocean (brighter blue)
        ocean_y = SCREEN_HEIGHT // 2 + 50
        bright_ocean = (100, 180, 255)
        ocean_rect = pygame.Rect(0, ocean_y, SCREEN_WIDTH, SCREEN_HEIGHT - ocean_y - 60)
        pygame.draw.rect(screen, bright_ocean, ocean_rect)
        
        # Beach/sand (brighter)
        bright_sand = (255, 220, 180)
        sand_rect = pygame.Rect(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60)
        pygame.draw.rect(screen, bright_sand, sand_rect)
        
        # Coconut trees
        self.draw_coconut_tree(screen, 50, SCREEN_HEIGHT - 60)
        self.draw_coconut_tree(screen, SCREEN_WIDTH - 80, SCREEN_HEIGHT - 60)
    
    def draw_coconut_tree(self, screen, x, ground_y):
        # Tree trunk
        trunk_rect = pygame.Rect(x - 5, ground_y - 80, 10, 80)
        pygame.draw.rect(screen, COCONUT_BROWN, trunk_rect)
        
        # Palm leaves
        leaf_color = PALM_GREEN
        # Left leaves
        pygame.draw.ellipse(screen, leaf_color, (x - 30, ground_y - 100, 25, 8))
        pygame.draw.ellipse(screen, leaf_color, (x - 35, ground_y - 95, 30, 6))
        pygame.draw.ellipse(screen, leaf_color, (x - 25, ground_y - 105, 20, 10))
        
        # Right leaves
        pygame.draw.ellipse(screen, leaf_color, (x + 5, ground_y - 100, 25, 8))
        pygame.draw.ellipse(screen, leaf_color, (x + 5, ground_y - 95, 30, 6))
        pygame.draw.ellipse(screen, leaf_color, (x + 5, ground_y - 105, 20, 10))
        
        # Top leaves
        pygame.draw.ellipse(screen, leaf_color, (x - 12, ground_y - 110, 8, 25))
        pygame.draw.ellipse(screen, leaf_color, (x + 4, ground_y - 110, 8, 25))
        
        # Coconuts
        pygame.draw.circle(screen, COCONUT_BROWN, (x - 8, ground_y - 85), 4)
        pygame.draw.circle(screen, COCONUT_BROWN, (x + 3, ground_y - 88), 4)
        pygame.draw.circle(screen, COCONUT_BROWN, (x - 2, ground_y - 92), 4)

class Collectible:
    def __init__(self, x, y, collectible_type="coin"):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.collectible_type = collectible_type
        self.collected = False
        self.animation_timer = 0
    
    def update(self):
        self.animation_timer += 1
    
    def draw(self, screen):
        if not self.collected:
            offset = math.sin(self.animation_timer * 0.1) * 3
            
            if self.collectible_type == "coin":
                pygame.draw.circle(screen, YELLOW, (int(self.x + self.width//2), int(self.y + self.height//2 + offset)), 8)
                pygame.draw.circle(screen, ORANGE, (int(self.x + self.width//2), int(self.y + self.height//2 + offset)), 8, 2)
            elif self.collectible_type == "power_up":
                pygame.draw.rect(screen, RED, (int(self.x), int(self.y + offset), self.width, self.height))
                pygame.draw.circle(screen, WHITE, (int(self.x + self.width//2), int(self.y + self.height//2 + offset)), 3)
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.level = 1
        self.max_level = 3
        self.kitty = HelloKitty()
        self.enemies = []
        self.platforms = []
        self.collectibles = []
        self.background = Background()
        self.game_over = False
        self.level_complete = False
        self.font = pygame.font.Font(None, 36)
        self.load_level()
    
    def load_level(self):
        self.enemies.clear()
        self.platforms.clear()
        self.collectibles.clear()
        
        # Ground platform
        self.platforms.append(Platform(0, SCREEN_HEIGHT - 60, SCREEN_WIDTH, 60))
        
        if self.level == 1:
            # Level 1: Basic platforms and enemies
            self.platforms.extend([
                Platform(200, 450, 100, 20),
                Platform(400, 350, 100, 20),
                Platform(600, 250, 100, 20)
            ])
            
            self.enemies.extend([
                Kiromi(300),
                Kiromi(500, 330, "fast"),
                Kiromi(150, 430, "normal")
            ])
            
            self.collectibles.extend([
                Collectible(220, 420),
                Collectible(420, 320),
                Collectible(620, 220),
                Collectible(50, SCREEN_HEIGHT - 120),
                Collectible(750, SCREEN_HEIGHT - 120),
                Collectible(420, 310, "power_up")
            ])
        
        elif self.level == 2:
            # Level 2: More complex layout
            self.platforms.extend([
                Platform(150, 500, 80, 20),
                Platform(300, 400, 80, 20),
                Platform(500, 300, 80, 20),
                Platform(100, 200, 80, 20),
                Platform(650, 150, 100, 20)
            ])
            
            self.enemies.extend([
                Kiromi(200, 480, "normal"),
                Kiromi(350, 380, "fast"),
                Kiromi(550, 280, "jumper"),
                Kiromi(400),
                Kiromi(600)
            ])
            
            self.collectibles.extend([
                Collectible(170, 470),
                Collectible(320, 370),
                Collectible(520, 270),
                Collectible(120, 170),
                Collectible(670, 120),
                Collectible(320, 360, "power_up"),
                Collectible(670, 110, "power_up")
            ])
        
        elif self.level == 3:
            # Level 3: Challenging final level
            self.platforms.extend([
                Platform(100, 480, 60, 20),
                Platform(250, 420, 60, 20),
                Platform(400, 360, 60, 20),
                Platform(550, 300, 60, 20),
                Platform(200, 240, 60, 20),
                Platform(400, 180, 60, 20),
                Platform(600, 120, 100, 20)
            ])
            
            self.enemies.extend([
                Kiromi(150, 460, "fast"),
                Kiromi(300, 400, "jumper"),
                Kiromi(450, 340, "fast"),
                Kiromi(250, 220, "jumper"),
                Kiromi(200),
                Kiromi(500),
                Kiromi(700, SCREEN_HEIGHT - 95, "fast")
            ])
            
            self.collectibles.extend([
                Collectible(120, 450),
                Collectible(270, 390),
                Collectible(420, 330),
                Collectible(570, 270),
                Collectible(220, 210),
                Collectible(420, 150),
                Collectible(620, 90),
                Collectible(270, 380, "power_up"),
                Collectible(420, 140, "power_up")
            ])
    
    def check_collisions(self):
        kitty_rect = self.kitty.get_rect()
        
        # Check enemy collisions
        for enemy in self.enemies:
            if kitty_rect.colliderect(enemy.get_rect()) and not self.kitty.invincible:
                if self.kitty.has_power_up:
                    # Remove enemy if player has power-up
                    self.enemies.remove(enemy)
                    self.kitty.score += 50
                else:
                    self.kitty.lives -= 1
                    self.kitty.invincible = True
                    self.kitty.invincible_timer = 120  # 2 seconds of invincibility
                    
                    if self.kitty.lives <= 0:
                        self.game_over = True
        
        # Check collectible collisions
        for collectible in self.collectibles[:]:
            if kitty_rect.colliderect(collectible.get_rect()) and not collectible.collected:
                collectible.collected = True
                self.collectibles.remove(collectible)
                
                if collectible.collectible_type == "coin":
                    self.kitty.score += 10
                elif collectible.collectible_type == "power_up":
                    self.kitty.has_power_up = True
                    self.kitty.power_up_timer = 300  # 5 seconds
                    self.kitty.speed = 8
        
        # Check level completion
        if len(self.collectibles) == 0:
            if self.level < self.max_level:
                self.level += 1
                self.kitty.x = 100
                self.kitty.y = SCREEN_HEIGHT - self.kitty.height - 60
                self.load_level()
            else:
                self.level_complete = True
    
    def update(self):
        # Always update background animation
        self.background.update()
        
        if not self.game_over and not self.level_complete:
            self.kitty.update(self.platforms)
            
            for enemy in self.enemies:
                enemy.update(self.platforms)
            
            for collectible in self.collectibles:
                collectible.update()
            
            self.check_collisions()
    
    def draw(self, screen):
        # Draw coastal background first
        self.background.draw(screen)
        
        # Draw platforms
        for platform in self.platforms:
            platform.draw(screen)
        
        # Draw collectibles
        for collectible in self.collectibles:
            collectible.draw(screen)
        
        # Draw enemies
        for enemy in self.enemies:
            enemy.draw(screen)
        
        # Draw player
        self.kitty.draw(screen)
        
        # Draw UI
        score_text = self.font.render(f"Score: {self.kitty.score}", True, BLACK)
        lives_text = self.font.render(f"Lives: {self.kitty.lives}", True, BLACK)
        level_text = self.font.render(f"Level: {self.level}", True, BLACK)
        
        screen.blit(score_text, (10, 10))
        screen.blit(lives_text, (10, 50))
        screen.blit(level_text, (10, 90))
        
        if self.kitty.has_power_up:
            power_text = self.font.render("POWER UP!", True, RED)
            screen.blit(power_text, (SCREEN_WIDTH - 150, 10))
        
        if self.game_over:
            game_over_text = self.font.render("GAME OVER! Press R to restart", True, RED)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(game_over_text, text_rect)
        
        if self.level_complete:
            win_text = self.font.render("YOU WIN! Press R to play again", True, GREEN)
            text_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            screen.blit(win_text, text_rect)
    
    def restart(self):
        self.level = 1
        self.kitty = HelloKitty()
        self.game_over = False
        self.level_complete = False
        self.load_level()

def main():
    game = Game()

    while True:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_r and (game.game_over or game.level_complete):
                    game.restart()

        # Update game
        game.update()

        # Draw everything
        game.draw(screen)
        
        # Update display
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
