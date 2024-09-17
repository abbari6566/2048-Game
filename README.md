# 2048-Game

This project is an implementation of the popular sliding puzzle game 2048 using the Pygame library. The objective of the game is to combine tiles of the same number by sliding them across a 4x4 grid. When two tiles with the same number collide, they merge into one, and the value of the tile doubles. The goal is to create a tile with the value 2048 or more.

Features
4x4 grid: The game is played on a 4x4 grid, with tiles that can slide in four directions (up, down, left, right).
Tile merging: When two tiles of the same value collide, they merge into one with double the original value.
Random tile generation: After each move, a new tile (2 or 4) is added to the grid at a random, empty position.
Grid rendering: The grid is drawn dynamically using Pygame, including the tile values and colors.

Prerequisites
Before running the game, you need to have Python installed on your system, along with the Pygame library.

Install Python: Download and install Python from python.org.
Install Pygame: Install the Pygame library by running the following command in your terminal or command prompt:

pip install pygame

Controls
Arrow Keys: Move the tiles in the respective direction.
Left Arrow: Move tiles left
Right Arrow: Move tiles right
Up Arrow: Move tiles up
Down Arrow: Move tiles down

Code Explanation
Tile Class: Represents each tile in the game. Tiles have a value, row, and column and are rendered with specific colors based on their values.
Grid and Drawing: The grid is dynamically drawn based on the current position and values of the tiles. The game window is updated after each move.
Tile Movement and Merging: The tiles can move in four directions. After each move, the game checks if tiles can merge (if they have the same value), and merges them accordingly.
Game Logic: Handles the logic for moving, merging, and generating new tiles. If the grid is full and no moves are possible, the game ends.
Key Functions
draw(window, tiles): Redraws the entire game window, including all tiles and the grid.
move_tiles(window, tiles, clock, direction): Handles the logic of moving and merging tiles in the given direction.
get_random_pos(tiles): Finds an empty position in the grid for placing a new tile after each move.
generate_tiles(): Initializes the grid with two tiles at random positions.

Game Flow
Initialization: The game starts with two tiles on the grid, each with a value of 2.
Player Input: The player uses the arrow keys to move the tiles in the desired direction.
Tile Movement: Tiles slide in the direction of the move, and if two tiles with the same value collide, they merge.
New Tile Generation: After each move, a new tile (2 or 4) is generated at a random empty position.
Game Over: The game continues until no more moves are possible, i.e., the grid is full and no tiles can merge.

Future Enhancements
Some ideas for future improvements include:
Game Over Screen: Display a message when the player wins (reaches 2048) or loses (no more possible moves).
Undo Move: Allow players to undo their last move.
High Score Tracker: Implement a high score system to track and display the player's best performance.
Advanced AI: Create an AI that can play the game using algorithms like Minimax.
