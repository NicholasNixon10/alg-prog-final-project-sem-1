import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer for Sounds
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load("./sound effects/escape.mp3")  # Load background music
pygame.mixer.music.set_volume(0.5)  # Set volume for the music

# Load Sound Effect
collision_sound = pygame.mixer.Sound("./sound effects/vine-boom.mp3")  # Load collision sound effect
collision_sound.set_volume(0.5)  # Set volume for the sound effect

# Load Images
player_image = pygame.image.load("./images/nixonface.jpg")  # Load player image
rock_image = pygame.image.load("./images/the-rock.png")  # Load rock image

# Resize Images
player_image = pygame.transform.scale(player_image, (50, 50))  # Scale player image to 50x50
rock_image = pygame.transform.scale(rock_image, (50, 50))  # Scale rock image to 50x50

# Load Main Menu Background Image
menu_background = pygame.image.load("./images/lebron.jpg")  # Load menu background image
menu_background = pygame.transform.scale(menu_background, (1200, 900))  # Resize menu background to screen size

# Load Game Over Image
game_over_image = pygame.image.load("./images/the-rock-hungry.png")  # Load "Game Over" image
game_over_image = pygame.transform.scale(game_over_image, (600, 450))  # Resize "Game Over" image

# Load and Resize Background Image
background_image = pygame.image.load("./images/lebron2.jpg")  # Load game background image
background_image = pygame.transform.scale(background_image, (1200, 900))  # Resize background image to screen size

# Load and Resize Game Over Background Image
game_over_background = pygame.image.load("./images/hell.jpg")  # Load "Game Over" background image
game_over_background = pygame.transform.scale(game_over_background, (1200, 900))  # Resize "Game Over" background image

# Screen Dimensions
WIDTH, HEIGHT = 1200, 900  # Set screen width and height
screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Create the game window
pygame.display.set_caption("Rock Falling Game")  # Set window title

# Colors
WHITE = (255, 255, 255)  # RGB value for white
BLACK = (0, 0, 0)  # RGB value for black
RED = (255, 0, 0)  # RGB value for red
BLUE = (0, 0, 255)  # RGB value for blue
GREEN = (0, 150, 0)  # RGB value for green
YELLOW = (232, 162, 23)  # RGB value for yellow
GRAY = (120, 120, 120)  # RGB value for gray

# Clock for FPS
clock = pygame.time.Clock()  # Create a clock to control frame rate
FPS = 60  # Set frames per second

# Player Properties
player_width, player_height = 50, 50  # Player dimensions
player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10  # Start position for the player
player_speed = 7  # Speed of the player movement

# Rock Properties
rock_width, rock_height = 50, 50  # Default rock dimensions
rock_speed = 5  # Initial speed of falling rocks
rocksss = []  # List to store all falling rocks

# Score
score = 0  # Initialize the player's score
font = pygame.font.Font(None, 36)  # Set font for text rendering

# Leaderboard
high_scores = []  # List to store high scores

# Load High Scores from file
def load_high_scores():
    global high_scores
    if os.path.exists("high_scores.txt"):  # Check if leaderboard file exists
        with open("high_scores.txt", "r") as file:  # Open file for reading
            high_scores = [int(line.strip()) for line in file.readlines()]  # Read and parse scores
    else:
        high_scores = []  # Initialize an empty leaderboard if file doesn't exist
    high_scores.sort(reverse=True)  # Sort scores in descending order

# Save High Scores to file
def save_high_scores():
    with open("high_scores.txt", "w") as file:  # Open file for writing
        for score in high_scores:  # Write each score on a new line
            file.write(f"{score}\n")

# Function to create a rock
def create_rock():
    x = random.randint(0, WIDTH - 50)  # Random x-coordinate within screen width
    y = -50  # Start above the screen
    width = random.randint(10, 100)  # Random width for the rock
    height = random.randint(10, 100)  # Random height for the rock
    return [x, y, width, height]  # Return rock's properties

# Function to draw text
def draw_text(text, x, y, color=WHITE):
    label = font.render(text, True, color)  # Render the text
    screen.blit(label, (x, y))  # Display the text on the screen

# Function to update leaderboard
def update_leaderboard(score):
    global high_scores
    high_scores.append(score)  # Add the new score
    high_scores.sort(reverse=True)  # Sort scores in descending order
    high_scores = high_scores[:5]  # Keep only top 5 scores
    save_high_scores()  # Save updated scores to file

# Function for the main menu
def main_menu():
    global running, player_x, player_y, rocksss, score
    menu_running = True
    while menu_running:
        screen.blit(menu_background, (0, 0))  # Draw the background
        draw_text("Rock Falling Game", WIDTH // 2 - 150, HEIGHT // 2 - 100, WHITE)  # Title
        draw_text("Press ENTER to Start", WIDTH // 2 - 150, HEIGHT // 2, BLUE)  # Start instruction
        draw_text("Press ESC to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 50, RED)  # Quit instruction
        pygame.display.flip()  # Update display

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_RETURN:  # Start game
                    return
                if event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    sys.exit()

# Function for the Game Over Screen
def game_over_screen(score):
    global running, player_x, player_y, rocksss
    game_over_running = True

    # Update leaderboard before entering the event loop
    update_leaderboard(score)  # Add the final score to the leaderboard

    while game_over_running:
        screen.blit(game_over_background, (0, 0))  # Draw the Game Over background image
        screen.blit(game_over_image, (WIDTH // 2 - 300, HEIGHT // 2 - 225))  # Center the "Game Over" image
        draw_text("GAME OVER :(", WIDTH // 2 - 100, HEIGHT // 2, RED)  # Display "Game Over" text
        draw_text(f"Final Score: {score}", WIDTH // 2 - 150, HEIGHT // 2 + 50, BLUE)  # Display the player's score
        draw_text("Press ENTER to return to Main Menu", WIDTH // 2 - 150, HEIGHT // 2 + 100, GREEN)  # Restart instruction
        draw_text("Press ESC to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 150, YELLOW)  # Quit instruction

        # Display Leaderboard in the top-right corner
        draw_text("Leaderboard", WIDTH - 200, 50, YELLOW)  # Display leaderboard title
        for i, high_score in enumerate(high_scores):  # Display the top 5 high scores
            draw_text(f"{i + 1}. {high_score}", WIDTH - 200, 100 + i * 40, WHITE)

        pygame.display.flip()  # Update the display

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit game if window is closed
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:  # Check for key presses
                if event.key == pygame.K_RETURN:  # Return to main menu
                    game_over_running = False  # Exit game over screen
                if event.key == pygame.K_ESCAPE:  # Quit game
                    pygame.quit()
                    sys.exit()

# Function to run the main game loop
def play_game():
    global running, player_x, player_y, rocksss, score, rock_speed

    # Reset game variables
    running = True
    player_x, player_y = WIDTH // 2, HEIGHT - player_height - 10  # Reset player position
    rocksss.clear()  # Clear all existing rocks
    score = 0  # Reset score
    rock_speed = 5  # Reset rock speed

    # Play background music
    pygame.mixer.music.play()  # Start the background music loop

    while running:
        screen.fill(BLACK)  # Clear the screen

        # Draw Background
        screen.blit(background_image, (0, 0))  # Draw the game background

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Quit the game if the window is closed
                pygame.quit()
                sys.exit()

        # Player Movement
        keys = pygame.key.get_pressed()  # Get current key states
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and player_x > 0:  # Move left if left arrow or 'A' is pressed
            player_x -= player_speed
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and player_x < WIDTH - player_width:  # Move right if right arrow or 'D' is pressed
            player_x += player_speed

        # Create Rocks Periodically
        if random.randint(1, max(20 - score // 100, 5)) == 1:  # Decrease interval as score increases
            rocksss.append(create_rock())  # Add a new rock to the list

        # Adjust rock speed based on score
        rock_speed = 5 + (score // 100)  # Increase speed as score increases

        # Move Rocks
        for rock in rocksss:
            rock[1] += rock_speed  # Move rocks downward

        # Remove Rocks Out of Screen
        rocksss = [rock for rock in rocksss if rock[1] < HEIGHT]  # Keep only rocks within the screen

        # Collision Detection
        player_rect = player_image.get_rect(topleft=(player_x, player_y))  # Get player's bounding box
        for rock in rocksss:
            rock_rect = rock_image.get_rect(topleft=(rock[0], rock[1]))  # Get rock's bounding box
            if player_rect.colliderect(rock_rect):  # Check for collision
                collision_sound.play()  # Play collision sound
                running = False  # End the game if collision occurs

        # Draw Player
        screen.blit(player_image, (player_x, player_y))  # Draw the player

        # Draw Rocks
        for rock in rocksss:
            scaled_rock_image = pygame.transform.scale(rock_image, (rock[2], rock[3]))  # Scale rock image to random size
            screen.blit(scaled_rock_image, (rock[0], rock[1]))  # Draw the rock

        # Update Score
        score += 1  # Increment score
        draw_text(f"Score: {score}", 10, 10)  # Display current score

        # Update Display
        pygame.display.flip()  # Refresh the screen

        # Control FPS
        clock.tick(FPS)  # Ensure game runs at the specified FPS

    # Stop the background music
    pygame.mixer.music.stop()  # Stop music when the game ends

    # Call Game Over Screen
    game_over_screen(score)  # Show the "Game Over" screen

# Main Program Execution
def main():
    load_high_scores()  # Load high scores at the start
    while True:
        main_menu()  # Show main menu
        play_game()  # Start the game when the player chooses to play

# Call the main function to run the game
main()
