from tiles import Tile

print("grid.py has been imported")

# Tile size
tilesize = 40
# How many tiles going to the x and y position.
grid_cols = 15
grid_rows = 15

colors = {
    "black": (0, 0, 0,),
    "white": (255, 255, 255),
    "darkGrey": (32, 32, 32)
}


def loadGrid(tilelist, prevtime):
    # Prepares the grid.
    for row_index in range(grid_cols):
        for col_index in range(grid_rows):
            x = col_index * tilesize
            y = row_index * tilesize

            tilelist.append(Tile(x, y, tilesize, colors["black"], prevtime))
