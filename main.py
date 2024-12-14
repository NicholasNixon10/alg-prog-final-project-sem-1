import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Initialize Pygame Mixer for Sounds
pygame.mixer.init()

# Load Background Music
pygame.mixer.music.load("./sound effects/escape.mp3")
pygame.mixer.music.set_volume(0.5)

# Load Sound Effect
collision_sound = pygame.mixer.Sound("./sound effects/vine-boom.mp3")
collision_sound.set_volume(0.5)

# Load Images
player_image = pygame.image.load("./images/nixonface.jpg")
rock_image = pygame.image.load("./images/the-rock.png")
menu_background = pygame.image.load("./images/lebron.jpg")
game_over_image = pygame.image.load("./images/the-rock-hungry.png")
background_image = pygame.image.load("./images/lebron2.jpg")
game_over_background = pygame.image.load("./images/hell.jpg")

# Resize Images for Consistent Display
player_image = pygame.transform.scale(player_image, (50, 50))
rock_image = pygame.transform.scale(rock_image, (50, 50))
menu_background = pygame.transform.scale(menu_background, (1200, 900))
game_over_image = pygame.transform.scale(game_over_image, (600, 450))
background_image = pygame.transform.scale(background_image, (1200, 900))
game_over_background = pygame.transform.scale(game_over_background, (1200, 900))

# Screen Dimensions
WIDTH, HEIGHT = 1200, 900
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Rock Falling Game")

# Colors for UI Elements
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 150, 0)
YELLOW = (232, 162, 23)
BLACK = (0, 0, 0)

# Clock for FPS Control
clock = pygame.time.Clock()
FPS = 60

# Font for Displaying Text
font = pygame.font.Font(None, 36)

# Player Class
class Player:
    def __init__(self, x, y, speed):
        self.x = x  # Player's horizontal position
        self.y = y  # Player's vertical position
        self.width = 50  # Player's width
        self.height = 50  # Player's height
        self.speed = speed  # Speed of movement

    def move(self, keys):
        # Move left if left arrow or 'A' is pressed, ensuring not to go off-screen
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.x > 0:
            self.x -= self.speed
        # Move right if right arrow or 'D' is pressed, ensuring not to go off-screen
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.x < WIDTH - self.width:
            self.x += self.speed

    def draw(self):
        # Draw the player image at the current position
        screen.blit(player_image, (self.x, self.y))

    def get_rect(self):
        # Get the rectangle representation of the player for collision detection
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Rock Class
class Rock:
    def __init__(self, speed):
        self.x = random.randint(0, WIDTH - 50)  # Random horizontal start position
        self.y = -50  # Start just above the screen
        self.width = random.randint(10, 100)  # Random width for variation
        self.height = random.randint(10, 100)  # Random height for variation
        self.speed = speed  # Falling speed

    def move(self):
        # Move the rock downward by its speed
        self.y += self.speed

    def draw(self):
        # Dynamically scale the rock image based on its size
        scaled_rock_image = pygame.transform.scale(rock_image, (self.width, self.height))
        screen.blit(scaled_rock_image, (self.x, self.y))

    def get_rect(self):
        # Get the rectangle representation of the rock for collision detection
        return pygame.Rect(self.x, self.y, self.width, self.height)

# Main Game Class
class Game:
    def __init__(self):
        self.player = Player(WIDTH // 2, HEIGHT - 60, 7)  # Create the player instance
        self.rocks = []  # List to hold falling rocks
        self.score = 0  # Initialize score
        self.high_scores = []  # Leaderboard of high scores
        self.running = True  # Flag to control game loop
        self.load_high_scores()  # Load saved high scores

    def load_high_scores(self):
        # Load high scores from a file, if it exists
        if os.path.exists("high_scores.txt"):
            with open("high_scores.txt", "r") as file:
                self.high_scores = [int(line.strip()) for line in file.readlines()]
        else:
            self.high_scores = []
        self.high_scores.sort(reverse=True)

    def save_high_scores(self):
        # Save top 5 high scores to a file
        with open("high_scores.txt", "w") as file:
            for score in self.high_scores[:5]:
                file.write(f"{score}\n")

    def create_rock(self):
        # Increase rock spawn rate and speed based on score
        if random.randint(1, max(20 - self.score // 100, 5)) == 1:
            speed = 5 + self.score // 100  # Increase speed as score increases
            self.rocks.append(Rock(speed))

    def update_rocks(self):
        # Move each rock and remove rocks that fall below the screen
        for rock in self.rocks:
            rock.move()
        self.rocks = [rock for rock in self.rocks if rock.y < HEIGHT]

    def detect_collision(self):
        # Check for collisions between the player and any rock
        player_rect = self.player.get_rect()
        for rock in self.rocks:
            if player_rect.colliderect(rock.get_rect()):
                collision_sound.play()  # Play collision sound
                self.running = False  # End the game

    def update_score(self):
        # Increment the score over time
        self.score += 1

    def update_leaderboard(self):
        # Update high scores with the current score
        self.high_scores.append(self.score)
        self.high_scores.sort(reverse=True)
        self.high_scores = self.high_scores[:5]  # Keep only the top 5 scores
        self.save_high_scores()

    def draw_text(self, text, x, y, color=WHITE):
        # Render and display text on the screen
        label = font.render(text, True, color)
        screen.blit(label, (x, y))

    def draw_rocks(self):
        # Draw all the rocks on the screen
        for rock in self.rocks:
            rock.draw()

    def main_menu(self):
        # Display the main menu and wait for user input
        menu_running = True
        while menu_running:
            screen.blit(menu_background, (0, 0))
            self.draw_text("Rock Falling Game", WIDTH // 2 - 150, HEIGHT // 2 - 100, WHITE)
            self.draw_text("Press ENTER to Start", WIDTH // 2 - 150, HEIGHT // 2, BLUE)
            self.draw_text("Press ESC to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 50, RED)
            self.draw_text("Use ARROW KEYS or A/D to Move", WIDTH // 2 - 200, HEIGHT // 2 + 100, YELLOW)
            self.draw_text("Avoid falling rocks!", WIDTH // 2 - 200, HEIGHT // 2 + 150, GREEN)
            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return  # Start the game
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def game_over_screen(self):
        # Display the game over screen with final score and leaderboard
        self.update_leaderboard()
        game_over_running = True
        while game_over_running:
            screen.blit(game_over_background, (0, 0))
            screen.blit(game_over_image, (WIDTH // 2 - 300, HEIGHT // 2 - 225))
            self.draw_text("GAME OVER :(", WIDTH // 2 - 100, HEIGHT // 2, RED)
            self.draw_text(f"Final Score: {self.score}", WIDTH // 2 - 150, HEIGHT // 2 + 50, BLUE)
            self.draw_text("Press ENTER to return to Main Menu", WIDTH // 2 - 150, HEIGHT // 2 + 100, GREEN)
            self.draw_text("Press ESC to Quit", WIDTH // 2 - 150, HEIGHT // 2 + 150, YELLOW)
            self.draw_text("Leaderboard", WIDTH - 200, 50, YELLOW)

            for i, high_score in enumerate(self.high_scores):
                self.draw_text(f"{i + 1}. {high_score}", WIDTH - 200, 100 + i * 40, WHITE)

            pygame.display.flip()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        return  # Return to main menu
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

    def play_game(self):
        # Core game loop
        self.running = True
        self.player.x, self.player.y = WIDTH // 2, HEIGHT - 60  # Reset player position
        self.rocks.clear()  # Clear existing rocks
        self.score = 0  # Reset score
        pygame.mixer.music.play()  # Play background music

        while self.running:
            screen.fill(BLACK)  # Clear screen
            screen.blit(background_image, (0, 0))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            keys = pygame.key.get_pressed()
            self.player.move(keys)  # Handle player movement

            self.create_rock()  # Spawn new rocks
            self.update_rocks()  # Move and manage rocks
            self.detect_collision()  # Check for collisions
            self.update_score()  # Update the score

            self.player.draw()  # Draw the player
            self.draw_rocks()  # Draw all rocks
            self.draw_text(f"Score: {self.score}", 10, 10)  # Display score

            pygame.display.flip()
            clock.tick(FPS)  # Maintain consistent frame rate

        pygame.mixer.music.stop()  # Stop music after game over
        self.game_over_screen()  # Show game over screen

    def run(self):
        # Main loop to display menu and play the game
        while True:
            self.main_menu()  # Show main menu
            self.play_game()  # Start game

# Run the Game
game = Game()
game.run()
