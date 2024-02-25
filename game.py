import pygame
import random

# Constants
WIDTH = 600
HEIGHT = 600
PIXEL_SIZE = 20
FPS = 30
SPEED = 0.1

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 128, 0)  # Dark green for maze
DARK_BLUE = (0, 0, 128)  # Dark blue for walls
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)  # Orange for rewards

class Pixel(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        self.image.fill(YELLOW)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.direction = 'RIGHT'
        self.score = 0
        self.font = pygame.font.SysFont(None, 36)

    def update(self):
        if self.direction == 'RIGHT':
            self.rect.x += PIXEL_SIZE * SPEED
        elif self.direction == 'LEFT':
            self.rect.x -= PIXEL_SIZE * SPEED
        elif self.direction == 'UP':
            self.rect.y -= PIXEL_SIZE * SPEED
        elif self.direction == 'DOWN':
            self.rect.y += PIXEL_SIZE * SPEED

    def draw_score(self, screen):
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

class Reward(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((PIXEL_SIZE, PIXEL_SIZE))
        self.image.fill(ORANGE)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Maze:
    def __init__(self):
        self.grid = [[0] * (WIDTH // PIXEL_SIZE) for _ in range(HEIGHT // PIXEL_SIZE)]
        self.generate_maze()

    def generate_maze(self):
        # Generate maze using randomized Prim's algorithm or any other maze generation algorithm
        # For simplicity, we'll just randomly fill some cells as obstacles
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if random.random() < 0.3:  # Adjust this probability to control maze density
                    self.grid[i][j] = 1

    def draw(self, screen):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                if self.grid[i][j] == 1:
                    pygame.draw.rect(screen, DARK_BLUE, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))
                else:
                    pygame.draw.rect(screen, GREEN, (j * PIXEL_SIZE, i * PIXEL_SIZE, PIXEL_SIZE, PIXEL_SIZE))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Minimalist Maze Game")
    clock = pygame.time.Clock()

    player = Pixel()
    rewards = [Reward(random.randint(0, WIDTH - PIXEL_SIZE), random.randint(0, HEIGHT - PIXEL_SIZE)) for _ in range(5)]  # Five rewards for now
    maze = Maze()

    all_sprites = pygame.sprite.Group()
    rewardsGroup = pygame.sprite.Group(rewards)
    all_sprites.add(player)
    all_sprites.add(rewards)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        print(keys)
        if keys[pygame.K_LEFT]:
            player.direction = 'LEFT'
        elif keys[pygame.K_RIGHT]:
            player.direction = 'RIGHT'
        elif keys[pygame.K_UP]:
            player.direction = 'UP'
        elif keys[pygame.K_DOWN]:
            player.direction = 'DOWN'

        player.update()

        # Check for collisions with rewards
        rewards_collected = pygame.sprite.spritecollide(player, rewardsGroup, True)
        for reward in rewards_collected:
            player.score += 10

        screen.fill(BLACK)  # Black background
        maze.draw(screen)
        player.draw_score(screen)
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
