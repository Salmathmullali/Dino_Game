import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 400

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Chrome Dino with Partner")

# Clock for controlling frame rate
clock = pygame.time.Clock()

# Dino class
class Dino(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/dinosaur-6273164_640.png").convert_alpha()  # Load the dino image
        self.image = pygame.transform.scale(self.image, (40, 40))  # Resize the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.gravity = 0

    def update(self):
        # Apply gravity
        self.gravity += 1
        self.rect.y += self.gravity

        # Stay on the ground
        if self.rect.y >= 300:
            self.rect.y = 300
            self.gravity = 0

    def jump(self):
        if self.rect.y == 300:
            self.gravity = -15

# Obstacle class
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("images/cac.png").convert_alpha()  # Load the cactus image
        self.image = pygame.transform.scale(self.image, (30, 30))  # Resize the image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x -= 10
        if self.rect.x < -30:
            self.rect.x = SCREEN_WIDTH + random.randint(50, 300)

# Game variables
dino = Dino(50, 300)
dino_partner = Dino(-100, 300)  # Initialize partner dino off-screen
all_sprites = pygame.sprite.Group()
obstacles = pygame.sprite.Group()
all_sprites.add(dino)
all_sprites.add(dino_partner)

# Generate obstacles
for i in range(3):
    obstacle = Obstacle(SCREEN_WIDTH + i * 300, 300)
    obstacles.add(obstacle)
    all_sprites.add(obstacle)

obstacles_passed = 0
font = pygame.font.Font(None, 36)

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                dino.jump()
                dino_partner.jump()

    # Update sprites
    all_sprites.update()

    # Check for collisions
    if pygame.sprite.spritecollideany(dino, obstacles):
        print("Game Over!")
        running = False

    # Check if any obstacle has been passed
    for obstacle in obstacles:
        if obstacle.rect.right < dino.rect.left:  # Obstacle has moved past the dino
            obstacles_passed += 1
            obstacles.remove(obstacle)  # Remove passed obstacle
            all_sprites.remove(obstacle)

            # Add a new obstacle
            new_obstacle = Obstacle(SCREEN_WIDTH + random.randint(50, 300), 300)
            obstacles.add(new_obstacle)
            all_sprites.add(new_obstacle)

    # Move the partner dino alongside the main dino
    if obstacles_passed >= 5:
        dino_partner.rect.x = dino.rect.x - 50  # Keep partner behind the main dino
        dino_partner.rect.y = dino.rect.y      # Match vertical position

    # Drawing everything
    screen.fill(WHITE)
    all_sprites.draw(screen)

    # Display score (obstacles passed)
    score_text = font.render(f"Score: {obstacles_passed}", True, BLACK)
    screen.blit(score_text, (10, 10))

    # Refresh the screen
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(20)

pygame.quit()
sys.exit()



