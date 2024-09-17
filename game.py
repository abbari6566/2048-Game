# Import necessary libraries for game development and randomization
import pygame
import random
import math

# Initialize pygame module
pygame.init()

# Set the frames per second for the game
FPS = 60

# Define the game window's width and height
WIDTH, HEIGHT = 800, 800

# Define the number of rows and columns in the grid
ROWS = 4
COLS = 4

# Calculate the width and height of each tile in the grid
RECT_HEIGHT = HEIGHT // ROWS
RECT_WIDTH = WIDTH // COLS

# Set visual parameters: outline color, thickness, background color, font color
OUTLINE_COLOR = (187, 173, 160)
OUTLINE_THICKNESS = 10
BACKGROUND_COLOR = (205, 192, 180)
FONT_COLOR = (119, 110, 101)

# Define the font style and size for tile values
FONT = pygame.font.SysFont("comicsans", 60, bold=True)

# Set the velocity of tile movement in pixels per frame
MOVE_VEL = 20

# Create a window with defined dimensions
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("2048")  # Set the window title


class Tile:
    """Class representing individual tiles in the 2048 game."""
    
    # Define colors for tiles depending on their values
    COLORS = [
        (237, 229, 218), (238, 225, 201), (243, 178, 122), (246, 150, 101),
        (247, 124, 95), (247, 95, 59), (237, 208, 115), (237, 204, 99),
        (236, 202, 80)
    ]

    def __init__(self, value, row, col):
        """Initialize a tile with a value, row, and column."""
        self.value = value
        self.row = row
        self.col = col
        self.x = col * RECT_WIDTH  # X coordinate based on column
        self.y = row * RECT_HEIGHT  # Y coordinate based on row

    def get_color(self):
        """Get color based on the value of the tile."""
        color_index = int(math.log2(self.value)) - 1
        return self.COLORS[color_index]

    def draw(self, window):
        """Draw the tile on the game window."""
        color = self.get_color()  # Get appropriate color for the value
        pygame.draw.rect(window, color, (self.x, self.y, RECT_WIDTH, RECT_HEIGHT))

        # Render the text of the tile value and center it within the tile
        text = FONT.render(str(self.value), 1, FONT_COLOR)
        window.blit(
            text,
            (
                self.x + (RECT_WIDTH / 2 - text.get_width() / 2),
                self.y + (RECT_HEIGHT / 2 - text.get_height() / 2),
            ),
        )

    def set_pos(self, ceil=False):
        """Set the position of the tile based on its X and Y coordinates."""
        if ceil:
            self.row = math.ceil(self.y / RECT_HEIGHT)
            self.col = math.ceil(self.x / RECT_WIDTH)
        else:
            self.row = math.floor(self.y / RECT_HEIGHT)
            self.col = math.floor(self.x / RECT_WIDTH)

    def move(self, delta):
        """Move the tile by a delta value (change in X and Y)."""
        self.x += delta[0]
        self.y += delta[1]


def draw_grid(window):
    """Draw the grid lines in the game window."""
    for row in range(1, ROWS):
        y = row * RECT_HEIGHT
        pygame.draw.line(window, OUTLINE_COLOR, (0, y), (WIDTH, y), OUTLINE_THICKNESS)

    for col in range(1, COLS):
        x = col * RECT_WIDTH
        pygame.draw.line(window, OUTLINE_COLOR, (x, 0), (x, HEIGHT), OUTLINE_THICKNESS)

    pygame.draw.rect(window, OUTLINE_COLOR, (0, 0, WIDTH, HEIGHT), OUTLINE_THICKNESS)


def draw(window, tiles):
    """Redraw the entire game window and update the display."""
    window.fill(BACKGROUND_COLOR)  # Fill the background color

    # Draw each tile in the game
    for tile in tiles.values():
        tile.draw(window)

    # Draw the grid lines
    draw_grid(window)

    # Update the window display
    pygame.display.update()


def get_random_pos(tiles):
    """Generate a random, empty position on the grid."""
    row, col = None, None
    while True:
        row = random.randrange(0, ROWS)
        col = random.randrange(0, COLS)

        # Ensure the position is not already occupied
        if f"{row}{col}" not in tiles:
            break

    return row, col


def move_tiles(window, tiles, clock, direction):
    """Move and merge tiles based on the specified direction (left, right, up, down)."""
    updated = True
    blocks = set()  # Keep track of merged tiles to avoid double-merging

    # Define movement behavior based on the direction
    if direction == "left":
        sort_func = lambda x: x.col
        reverse = False
        delta = (-MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col - 1}")
        merge_check = lambda tile, next_tile: tile.x > next_tile.x + MOVE_VEL
        move_check = lambda tile, next_tile: tile.x > next_tile.x + RECT_WIDTH + MOVE_VEL
        ceil = True
    elif direction == "right":
        sort_func = lambda x: x.col
        reverse = True
        delta = (MOVE_VEL, 0)
        boundary_check = lambda tile: tile.col == COLS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row}{tile.col + 1}")
        merge_check = lambda tile, next_tile: tile.x < next_tile.x - MOVE_VEL
        move_check = lambda tile, next_tile: tile.x + RECT_WIDTH + MOVE_VEL < next_tile.x
        ceil = False
    elif direction == "up":
        sort_func = lambda x: x.row
        reverse = False
        delta = (0, -MOVE_VEL)
        boundary_check = lambda tile: tile.row == 0
        get_next_tile = lambda tile: tiles.get(f"{tile.row - 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y > next_tile.y + MOVE_VEL
        move_check = lambda tile, next_tile: tile.y > next_tile.y + RECT_HEIGHT + MOVE_VEL
        ceil = True
    elif direction == "down":
        sort_func = lambda x: x.row
        reverse = True
        delta = (0, MOVE_VEL)
        boundary_check = lambda tile: tile.row == ROWS - 1
        get_next_tile = lambda tile: tiles.get(f"{tile.row + 1}{tile.col}")
        merge_check = lambda tile, next_tile: tile.y < next_tile.y - MOVE_VEL
        move_check = lambda tile, next_tile: tile.y + RECT_HEIGHT + MOVE_VEL < next_tile.y
        ceil = False

    # Keep moving tiles while changes occur in the grid
    while updated:
        clock.tick(FPS)
        updated = False
        sorted_tiles = sorted(tiles.values(), key=sort_func, reverse=reverse)

        for i, tile in enumerate(sorted_tiles):
            if boundary_check(tile):
                continue

            next_tile = get_next_tile(tile)
            if not next_tile:
                tile.move(delta)
            elif (
                tile.value == next_tile.value
                and tile not in blocks
                and next_tile not in blocks
            ):
                if merge_check(tile, next_tile):
                    tile.move(delta)
                else:
                    next_tile.value *= 2
                    sorted_tiles.pop(i)
                    blocks.add(next_tile)
            elif move_check(tile, next_tile):
                tile.move(delta)
            else:
                continue

            tile.set_pos(ceil)
            updated = True

        update_tiles(window, tiles, sorted_tiles)

    return end_move(tiles)


def end_move(tiles):
    """Check if the game is lost or add a new tile to the grid after a move."""
    if len(tiles) == 16:  # If the grid is full
        return "lost"

    # Add a new tile to a random, empty position on the grid
    row, col = get_random_pos(tiles)
    tiles[f"{row}{col}"] = Tile(random.choice([2, 4]), row, col)
    return "continue"


def update_tiles(window, tiles, sorted_tiles):
    """Update the tiles dictionary and redraw the updated grid."""
    tiles.clear()  # Clear the tile dictionary
    for tile in sorted_tiles:
        tiles[f"{tile.row}{tile.col}"] = tile

    draw(window, tiles)  # Redraw the game grid with updated tile positions


def generate_tiles():
    """Generate the initial two tiles on the grid."""
    tiles = {}
    for _ in range(2):
        row, col = get_random_pos(tiles)
        tiles[f"{row}{col}"] = Tile(2, row, col)

    return tiles


def main(window):
    """Main game loop."""
    clock = pygame.time.Clock()
    run = True

    # Generate the initial tiles
    tiles = generate_tiles()

    while run:
        clock.tick(FPS)

        # Event loop to process input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_tiles(window, tiles, clock, "left")
                elif event.key == pygame.K_RIGHT:
                    move_tiles(window, tiles, clock, "right")
                elif event.key == pygame.K_UP:
                    move_tiles(window, tiles, clock, "up")
                elif event.key == pygame.K_DOWN:
                    move_tiles(window, tiles, clock, "down")

        draw(window, tiles)  # Redraw the window on each frame

    pygame.quit()


if __name__ == "__main__":
    main(WINDOW)
