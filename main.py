import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer for Sounds
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load("./sound effects/escape.mp3")
pygame.mixer.music.set_volume(0.5)  # Set volume (0.0 to 1.0)


# Load Sound Effect
collision_sound = pygame.mixer.Sound("./sound effects/vine-boom.mp3")
collision_sound.set_volume(0.5)  

# Load Images
player_image = pygame.image.load("./images/nixonface.jpg")
rock_image = pygame.image.load("./images/the-rock.png")

# Resize Images
player_image = pygame.transform.scale(player_image, (50, 50))
rock_image = pygame.transform.scale(rock_image, (50, 50))

# Load Main Menu Background Image
menu_background = pygame.image.load("./images/lebron.jpg")
menu_background = pygame.transform.scale(menu_background, (1200, 900))

# Load Game Over Image
game_over_image = pygame.image.load("./images/the-rock-hungry.png")  
game_over_image = pygame.transform.scale(game_over_image, (600, 450))  

# Load and Resize Background Image
background_image = pygame.image.load("./images/lebron2.jpg")  
background_image = pygame.transform.scale(background_image, (1200, 900))  

# Load and Resize Game Over Background Image
game_over_background = pygame.image.load("./images/hell.jpg")  
game_over_background = pygame.transform.scale(game_over_background, (1200, 900))  

# Screen Dimensions
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Falling Game")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 150, 0)
YELLOW = (232, 162, 23)
GRAY = (120, 120, 120)

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
rocksss = []

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

# Function for the main menu
def main_menu():
    global running, player_x, player_y, rocksss, score
    menu_running = True
    while menu_running:
        screen.blit(menu_background, (0, 0))  # Draw the background
        
        # Game Title and Instructions
        draw_text("Rock Falling Game", WIDTH // 2 - 150, HEIGHT // 2 - 100, WHITE)
        draw_text("Press ENTER to Start", WIDTH // 2 - 150, HEIGHT // 2, BLUE)
        draw_text("Press ESC to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 50, RED)

         # Movement Instructions
        draw_text("Movement: Use Left/Right Arrow keys or A/D to move", WIDTH // 2 - 200, HEIGHT // 2 + 300, GREEN)
        draw_text("Avoid falling rocks!", WIDTH // 2 - 150, HEIGHT // 2 + 350, GREEN)

        pygame.display.flip() # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN: # Start game on Enter key
                    return  # Exit the menu and start the game
                if event.key == pygame.K_ESCAPE: # Quit game on Escape key
                    pygame.quit()
                    sys.exit()

# Function for the Game Over Screen
def game_over_screen(score):
    global running, player_x, player_y, rocksss
    game_over_running = True
    while game_over_running:
        screen.blit(game_over_background, (0, 0))  # Draw the Game Over background
        screen.blit(game_over_image, (WIDTH // 2 - 300, HEIGHT // 2 - 225))  # Center the Game Over image
        draw_text("GAME OVER :(", WIDTH // 2 - 100, HEIGHT // 2, RED)
        draw_text(f"Final Score: {score}", WIDTH // 2 - 150, HEIGHT // 2 + 50, BLUE)
        draw_text("Press ENTER to return to Main Menu", WIDTH // 2 - 150, HEIGHT // 2 + 100, GREEN)
        draw_text("Press ESC to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 150, YELLOW)

        pygame.display.flip()  # Update the display

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Return to Main Menu
                    game_over_running = False
                    return  # End the game loop and go back to the main menu
                if event.key == pygame.K_ESCAPE:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Function to run the main game loop
def play_game():
    global running, player_x, player_y, rocksss, score, rock_speed

    # Reset game variables
    running = True
    player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10
    rocksss.clear()
    score = 0
    rock_speed = 5

# Start background music for gameplay
    pygame.mixer.music.play(-1)  # Play the music infinitely (-1 for looping)

    while running:
        screen.fill(BLACK)

        # Draw Background
        screen.blit(background_image, (0, 0))

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # Player Movement
        keys = pygame.key.get_pressed()
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:
            player_x += player_speed

        # Create Rocks Periodically and More Frequently Based on Score
        if random.randint(1, max(20 - score // 100,5)) == 1:  # Adjust frequency by changing range
            rocksss.append(create_rock()) 

        # Adjust rock speed based on score
        rock_speed = 5 + (score // 100)  # Increase speed every 100 points

        # Move Rocks
        for rock in rocksss:
            rock[1] += rock_speed  # Move rock down

        # Remove Rocks Out of Screen
        rocksss = [rock for rock in rocksss if rock[1] < HEIGHT]

        # Collision Detection
        player_rect = player_image.get_rect(topleft=(player_x, player_y))
        for rock in rocksss:
            rock_rect = rock_image.get_rect(topleft=(rock[0], rock[1]))
            if player_rect.colliderect(rock_rect):
                collision_sound.play()  # Play the collision sound
                running = False  # End game on collision

        # Draw Player
        screen.blit(player_image, (player_x, player_y))

        # Draw Rocks
        for rock in rocksss:
            scaled_rock_image = pygame.transform.scale(rock_image, (rock[2], rock[3]))
            screen.blit(scaled_rock_image, (rock[0], rock[1]))

        # Update Score
        score += 1
        draw_text(f"Score: {score}", 10, 10)

        # Update Display
        pygame.display.flip()

        # Control FPS
        clock.tick(FPS)

    # Stop music when the game loop ends
    pygame.mixer.music.stop()

    # Call Game Over Screen
    game_over_screen(score)

# Main Program Execution
def main():
    while True:
        main_menu()  # Display the main menu and wait for Enter
        play_game()  # Start the gameplay after Enter is pressed

# Call the main function to run the game
main()