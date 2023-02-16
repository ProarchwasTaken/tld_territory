import pygame
import time
from grid import colors, loadGrid
from tiles import tileList, wallList, territoryList, Blue, Red

# =====================================================================================================================
# Territory - Made by Tyler "Proarch" @2023
#
# To be honest, this is the most complicated program I ever made with python, so it's pretty hard for me to leave
# clear comments. There may be performance issues depending on what computer you use. You can increase the
# grid size, but from what I discovered, anything higher than the values I preset will eventrually cause the game to
# slow to a near crawl.
#
# CONTROLS: Left click to place and remove a wall.
#           E to place a Blue Tile, Q to place a Red Tile. These special tiles will slowly spread to any empty tile.
#
# Thank you for trying out this program!
# =====================================================================================================================

running = True

# Sets up window.
pygame.init()
screenWidth, screenHeight = 600, 600
screen = pygame.display.set_mode((screenWidth, screenHeight))
pygame.display.set_caption("Territory")

# Sets up the clock and FPS
clock = pygame.time.Clock()
prevTime = time.time()
fps = 60

# Prepares the grid
loadGrid(tileList, prevTime)

# Main game loop.
while running:
    # Stuff that deals with the clock.
    clock.tick(fps)
    # Stores current time each cycle
    now = time.time()
    # Sets prevtime to now each cycle
    prevTime = now
    # Sets up FPS, Blue, and Red counter as window caption.
    pygame.display.set_caption(
        f"Territory | FPS: {int(clock.get_fps())} | Blue: {len(Blue.list)} | Red: {len(Red.list)}"
    )

    # Stores position of mouse.
    mousePos = pygame.mouse.get_pos()

    # Checks for game events
    for event in pygame.event.get():

        # This was originally going to be a match statement because I heard its much faster.
        # However, on further investigation I found out this wasn't the case, so I when back to how I usually do it.
        if event.type == pygame.QUIT:
            running = False

        # Checks for key inputs
        if event.type == pygame.KEYDOWN:

            # Checks if the E and Q keys are pressed while the cursor is hovering over a tile
            for tile in tileList:
                tile.spawnTerritory(mousePos, event.key, prevTime)

    # Refreshes the screen.
    screen.fill(colors["darkGrey"])

    # Updates class instances
    # (surface, mouse position, color, current time)
    for tile in tileList:
        tile.update(screen, mousePos, colors["white"], now)

    for wall in wallList:
        wall.update(screen, mousePos, colors["black"], now)

    # Updates all territory instances.
    for terri in territoryList:
        terri.update(screen, now)

    # Updates the screen.
    pygame.display.flip()
