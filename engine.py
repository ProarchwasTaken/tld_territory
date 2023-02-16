import pygame
import random

# This file contains the code for the Territory to work.
# The code was moved to a new file because it was taking up too many lines.

print("engine.py has been imported")


# Parent Class.
# Contains most of the code for how basic Territory is going to function
class Territory:
    def __init__(self, x, y, tilesize, color, prevtime):
        # Sets up basic factors of object
        self.rect = pygame.Rect(x, y, tilesize - 1, tilesize - 1)
        self.size = tilesize
        self.color = color

        # These two variables are very important.
        # They store data on who is friend or foe
        # The child classes of this class will be able to change these values for them to work.
        self.team = None
        self.enemy = None

        # These two lines are used for timing.
        self.prevtime = prevtime
        self.spreadDelay = 0.5  # How much time will pass before the instance attempts to spread.

        # Determine whether the instance's spread attempt is successful or not.
        self.spreadChance = 2  # Can go from 0-10

        # Sets up Rects for the tiles above, below, left, and right of the main rect.
        # This will be used for a new pygame feature I found out about.
        self.adjacentRects = [
            # Right
            pygame.Rect(x + tilesize, y, tilesize, tilesize),
            # Left
            pygame.Rect(x - tilesize, y, tilesize, tilesize),
            # Down
            pygame.Rect(x, y + tilesize, tilesize, tilesize),
            # Up
            pygame.Rect(x, y - tilesize, tilesize, tilesize)
        ]

        # Stores the positions of each tile adjecent to the instance.
        # Will be used later for creating tiles
        self.adjacent = [
            # Right
            None,
            # Left
            None,
            # Down
            None,
            # Up
            None
        ]

    def update(self, surface, now):
        # Handles the territory spreading.
        # First, it checks is the instances delay is over.
        if self.delayCheck(now):
            # Then it checks if the instance is not surrounded by tiles it can't spread to.
            if self.surroundedCheck() is False:
                # And finally, the instance will roll a die. If it succeeds then the instance will finally spread.
                if self.spreadAttempt():
                    self.spread()

        # Draws the instance on screen.
        self.draw(surface)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)

    def surroundedCheck(self):
        from tiles import tileList

        # First sets local variable to 0
        adjacentTiles = 0

        # For each item in adjecentRects
        for adj in self.adjacentRects:
            # Runs if item's rect does not collide with any floor or enemy tiles
            if not adj.collideobjects(tileList) or adj.collideobjects(self.enemy.list):
                adjacentTiles += 1

        # If this value is 4, return True
        if adjacentTiles == 4:
            return True
        else:
            return False

    # Checks if spread delay is over, return True if it is.
    def delayCheck(self, now):
        if now - self.prevtime >= self.spreadDelay:
            self.prevtime = now  # Set prevtime to the current time.
            return True

    # When called, generates a random integer between 0 though 10
    def spreadAttempt(self):
        ranNum = random.randint(0, 10)

        # Then it checks of spread chance is greater than random number.
        if self.spreadChance >= ranNum:
            return True  # If conditions are met.

    def spread(self):
        from tiles import territoryList, tileList
        # Sets up Adjacent Positions
        self.setAdjacent()

        # Runs for each value in list
        for adj in self.adjacent:
            # Will not run if list item is None
            if adj is not None:
                # Splits the list item's tuple into x and y values
                x, y = (adj)
                # Create a new instance at x, and y position
                territoryList.append(self.team(x, y, self.size, self.color, self.prevtime))

                for tile in tileList:
                    tile.terriCheck()

    def setAdjacent(self):
        from tiles import tileList, Tile

        # Runs for each item in adjacentRects also grabs the index of each item
        for adj_index, adj in enumerate(self.adjacentRects):
            # Checks if abj rect has collided with tile or enemy
            if adj.collideobjects(
                    tileList).__class__ is Tile or adj.collideobjects(self.enemy.list).__class__ is self.enemy:
                # Set adjacent value to abj x and y
                self.adjacent[adj_index] = adj.topleft
            else:
                # Sets abjacent value to None
                self.adjacent[adj_index] = None
