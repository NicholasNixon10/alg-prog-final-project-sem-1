# Rock Falling Game

This is a simple 2D game created using **Pygame** where you control a player character to avoid falling rocks. The goal is to survive as long as possible, scoring points while dodging the rocks.

## Features

- **Main Menu**: Press ENTER to start the game or ESC to quit.
- **Game Over Screen**: Displays the final score and the top 5 leaderboard. Press ENTER to return to the main menu or ESC to quit.
- **Player Movement**: Use the left/right arrow keys or A/D keys to move the player.
- **Falling Rocks**: Rocks fall from the top of the screen, and the player must avoid them.
- **Leaderboard**: Tracks and displays the top 5 high scores in the game.

## Installation

### Prerequisites

- **Python 3.x** installed on your computer.
- **Pygame** library. You can install it using pip:
  ```
  pip install pygame

## Files
The game requires several files for images, sounds, and music. Here's a breakdown of the file structure:

``` 
/sound effects/
  - escape.mp3      # Background music for the game
  - vine-boom.mp3   # Sound effect when the player collides with a rock

/images/
  - lebron.jpg      # Background image for the main menu
  - the-rock.png    # Image for the falling rocks
  - the-rock-hungry.png # Image for the game over screen
  - lebron2.jpg     # Background image for the game
  - hell.jpg         # Background image for the game over screen
  - nixonface.jpg   # Image for player character

high_scores.txt          # High score leaderboard
game.py             # Main game script
```

## How to Run:
- Download the required assets and place them in the corresponding folders:
- Place all image files in the /images/ directory.
- Place all sound files in the /sound effects/ directory.
- Run the game using the following command:

  ```
  python game.py
  ```

## How to Play the Game:
- Main Menu: Press ENTER to start the game or ESC to quit.
- In-Game: Use the left and right arrow keys or A/D to move the player character and avoid falling rocks.
- Game Over: After a collision, the game will show the game-over screen. Press ENTER to return to the main menu or ESC to quit.
- Controls:
  - Left/Right Arrow Keys or A/D: Move the player character left or right.
  - ENTER: Start the game, return to the main menu, or restart after a game over.
  - ESC: Quit the game.

## Leaderboard
The game keeps track of the top 5 high scores. These are saved in a text file called high_scores.txt. When the game ends, the leaderboard will be displayed on the game over screen.

## High Scores
High scores are stored in a text file (high_scores.txt). The top 5 highest scores are shown on the Game Over screen and are updated after each game.



