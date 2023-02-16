import pygame
from engine import Territory

print("tiles.py has been imported")

# Stores every Tile and Wall instance
tileList = []
wallList = []

# Stores every Blue and Red Instance
territoryList = []

# Colors used for Territory Children
terriColors = {
    "blue": (0, 0, 255),
    "red": (255, 0, 0)
}


# Used for the grid, treated as the ground
class Tile:
    
    def __init__(self, x, y, tilesize, color, prev_time):
        
        self.rect = pygame.Rect(x, y, tilesize-1, tilesize-1)
        
        # How much time must pass at it's creation before it can be clicked on
        self.clickDelay = 0.5
        self.prevtime = prev_time
        
        # Stores the position of instance
        self.x, self.y = x, y
        # Gets the size of the instance
        self.size = tilesize
        # Stores the color of instance
        self.color = color
        
    def update(self, surface, mousePos, swapcolor, now):

        # This code handles swapping the instance when it is clicked on.
        if now - self.prevtime >= self.clickDelay:
            if self.clickCheck(mousePos):
                self.prevtime = now
                self.swapTile(swapcolor)
        
        # Draws the instance
        self.draw(surface)
    
    # When called, It will check if the mouse is hovering over it, and if the mouse is left clicked.
    # Returns True if conditions are met
    def clickCheck(self, mousePos):
        if self.rect.collidepoint(mousePos):
            if pygame.mouse.get_pressed()[0] == 1:
                return True

    # Used for checking if territory is inside tile, the tile deletes itself if it's true.
    def terriCheck(self):
        if self.rect.collideobjects(territoryList):
            tileList.remove(self)

    def spawnTerritory(self, mousePos, key, prevtime):
        # First it checks if the mouse is hovering over tile.
        if self.rect.collidepoint(mousePos):
            # Then uses a match case to determine with key was pressed.
            match key:
                case pygame.K_e:  # Creates blue territory if E was pressed
                    territoryList.append(Blue(self.x, self.y, self.size, terriColors["blue"], prevtime))
                    
                    tileList.remove(self)  # In the end, the instance will delete itself
                
                case pygame.K_q:  # Creates red territory if E was pressed
                    territoryList.append(Red(self.x, self.y, self.size, terriColors["red"], prevtime))
                    
                    tileList.remove(self)  # In the end, the instance will delete itself
    
    # When called, it creates a Wall object at the Tile instance's position then the Tile instance deletes itself
    def swapTile(self, color):
        print("Swapping Tile with: Wall")
        wallList.append(Wall(self.x, self.y, self.size, color, self.prevtime))
            
        tileList.remove(self)
    
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self)


# This class inherits from Tile
# I learned that If you add a method in the child class with the same name as a function in the parent class,
# the inheritance of the parent method will be overridden. That's something that's very useful to know.
class Wall(Tile):
    # Used for checking if territory is inside wall, the wall deletes itself if it's true.
    def terriCheck(self):
        if self.rect.collideobjects(territoryList):
            wallList.remove(self)

    # When called, it creates a Tile object at the Wall instance's position then the Wall instance deletes itself
    def swapTile(self, color):
        print("Swapping Wall with: Tile")
        tileList.append(Tile(self.x, self.y, self.size, color, self.prevtime))
            
        wallList.remove(self)


# Child class of Territory, there will be some statments that allow it to act differently
class Blue(Territory):
    # A private class list of all Blue instances
    list = []
    
    def __init__(self, x, y, tilesize, color, prevtime):
        super().__init__(x, y, tilesize, color, prevtime)
        # Assigns the team class of the instance
        self.team = Blue
        # Assigns the enemy class to the instance.
        self.enemy = Red

        # Adds self to class list
        Blue.list.append(self)


# Child class of Territory, there will be some statments that allow it to act differently
class Red(Territory):
    # A private class list of all Red instances
    list = []
    
    def __init__(self, x, y, tilesize, color, prevtime):
        super().__init__(x, y, tilesize, color, prevtime)
        # Assigns the team class of the instance
        self.team = Red
        # Assigns the enemy class to the instance.
        self.enemy = Blue

        # Adds self to class list
        Red.list.append(self)

# If you want to see the full extent of what the last two class do, then refer to engine.py
