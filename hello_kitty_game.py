import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Player settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 50
PLAYER_SPEED = 5
PLAYER_JUMP_FORCE = -15
GRAVITY = 0.8

# Enemy settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_SPEED = 2

class Player:
    def __init__(self):
        self.rect = pygame.Rect(100, 100, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.velocity = [0, 0]
        self.is_jumping = False
        self.on_ground = False

    def update(self, platforms):
        # Apply gravity
        self.velocity[1] += GRAVITY
        
        # Move horizontally
        self.rect.x += self.velocity[0]
        
        # Check horizontal collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity[0] > 0:  # Moving right
                    self.rect.right = platform.rect.left
                elif self.velocity[0] < 0:  # Moving left
                    self.rect.left = platform.rect.right

        # Move vertically
        self.rect.y += self.velocity[1]
        
        # Check vertical collisions
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                if self.velocity[1] > 0:  # Falling
                    self.rect.bottom = platform.rect.top
                    self.on_ground = True
                    self.velocity[1] = 0
                elif self.velocity[1] < 0:  # Jumping
                    self.rect.top = platform.rect.bottom
                    self.velocity[1] = 0

    def jump(self):
        if self.on_ground:
            self.velocity[1] = PLAYER_JUMP_FORCE
            self.on_ground = False

class Platform:
    def __init__(self, x, y, width, height):
        self.rect = pygame.Rect(x, y, width, height)

class Enemy:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, ENEMY_WIDTH, ENEMY_HEIGHT)
        self.direction = 1  # 1 for right, -1 for left

    def update(self, platforms):
        self.rect.x += self.direction * ENEMY_SPEED
        
        # Check for collisions with platforms
        for platform in platforms:
            if self.rect.colliderect(platform.rect):
                self.direction *= -1  # Reverse direction

def main():
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Hello Kitty Platformer")
    clock = pygame.time.Clock()

    # Create player
    player = Player()

    # Create platforms
    platforms = [
        Platform(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),  # Ground
        Platform(200, 400, 100, 20),
        Platform(400, 300, 100, 20),
        Platform(600, 200, 100, 20)
    ]

    # Create enemies
    enemies = [
        Enemy(300, 380),
        Enemy(500, 280)
    ]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    player.jump()

        # Get keys
        keys = pygame.key.get_pressed()
        
        # Update player movement
        player.velocity[0] = 0
        if keys[pygame.K_LEFT]:
            player.velocity[0] = -PLAYER_SPEED
        if keys[pygame.K_RIGHT]:
            player.velocity[0] = PLAYER_SPEED

        # Update game objects
        player.update(platforms)
        for enemy in enemies:
            enemy.update(platforms)

        # Check for collisions with enemies
        for enemy in enemies:
            if player.rect.colliderect(enemy.rect):
                print("Game Over!")
                running = False

        # Draw everything
        screen.fill(BLUE)
        
        # Draw platforms
        for platform in platforms:
            pygame.draw.rect(screen, WHITE, platform.rect)
        
        # Draw enemies
        for enemy in enemies:
            pygame.draw.rect(screen, (255, 100, 100), enemy.rect)
        
        # Draw player
        pygame.draw.rect(screen, WHITE, player.rect)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
