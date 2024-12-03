import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer for Sounds
pygame.mixer.init()

# Load Sound Effect
collision_sound = pygame.mixer.Sound("fein-meme-sound-effect.mp3")
collision_sound.set_volume(0.5)  # Volume ranges from 0.0 to 1.0

# Load Images
player_image = pygame.image.load("nixonface.jpg")
rock_image = pygame.image.load("the-rock.png")

# Resize Images
player_image = pygame.transform.scale(player_image, (50, 50))
rock_image = pygame.transform.scale(rock_image, (50, 50))

# Load Game Over Image
game_over_image = pygame.image.load("kevin.jpg")  # Replace with your image file
game_over_image = pygame.transform.scale(game_over_image, (600, 450))  # Scale as needed

# Screen Dimensions
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Falling Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Clock for FPS
clock = pygame.time.Clock()
FPS = 60

# Player Properties
player_width, player_height = 50, 50
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
player_speed = 7

# Rock Properties
rock_width, rock_height = 50, 50
rock_speed = 5
rocks = []

# Score
score = 0
font = pygame.font.Font(None, 36)

# Function to create a rock
def create_rock():
    x = random.randint(0, WIDTH - 50)  # Ensure rocks stay on screen
    y = -50  # Start above the screen
    width = random.randint(10, 100)  # Random width
    height = random.randint(10, 100)  # Random height
    return [x, y, width, height]

# Function to draw text
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)
    screen.blit(label, (x, y))

# Main Game Loop
running = True
while running:
    screen.fill(BLACK)

    # Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Player Movement
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
    if keys[pygame.K_RIGHT] and player_x < WIDTH - player_width:
        player_x += player_speed

    # Create Rocks Periodically
    if random.randint(1, 20) == 1:  # Adjust frequency by changing range
        rocks.append(create_rock())

    # Adjust rock speed based on score
    rock_speed = 5 + (score // 100)  # Increase speed every 100 points

    # Move Rocks
    for rock in rocks:
        rock[1] += rock_speed # Move rock down

    # Remove Rocks Out of Screen
    rocks = [rock for rock in rocks if rock[1] < HEIGHT]

    # Collision Detection
    player_rect = player_image.get_rect(topleft=(player_x, player_y))
    for rock in rocks:
        rock_rect = rock_image.get_rect(topleft=(rock[0], rock[1]))
        if player_rect.colliderect(rock_rect):
            collision_sound.play(-1)  # Play the collision sound loop
            running = False  # End game on collision

   # Draw Player
    screen.blit(player_image, (player_x, player_y))

    # Draw Rocks
    for rock in rocks:
        scaled_rock_image = pygame.transform.scale(rock_image, (rock[2], rock[3]))
        screen.blit(scaled_rock_image, (rock[0], rock[1]))

    # Update Score
    score += 1
    draw_text(f"Score: {score}", 10, 10)

    # Update Display
    pygame.display.flip()

    # Control FPS
    clock.tick(FPS)

# Game Over Screen
screen.fill(BLACK)
screen.blit(game_over_image, (WIDTH // 2 - 300, HEIGHT // 2 - 225))  # Center the image
draw_text("GAME OVER :(", WIDTH // 2 - 100, HEIGHT // 2, RED)
draw_text(f"Final Score: {score}", WIDTH // 2 - 100, HEIGHT // 2 + 50, BLUE)
pygame.display.flip()
pygame.time.wait(5000)

# Quit Game
pygame.quit()
sys.exit() # Ensures script exits cleanly