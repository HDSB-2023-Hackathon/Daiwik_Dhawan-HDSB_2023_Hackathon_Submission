'''
Alright guys this gonna be main like program
 '''

# This is main shit right here to start stuff.

# Importing pygame library, so we can have a window and easily load images in.
import pygame

# Start it up, and set our display to variable "screen" and size of whatever.
pygame.init()
screen = pygame.display.set_mode((2240, 1280))

# Title of window/game
pygame.display.set_caption("Down to Earth")

# Sets our fps to 60, ex. our game loop runs 60 times every second. Very important to so our animations and timings
# are consistent.
FPS = 60
fpsClock = pygame.time.Clock()

# Example on how to load an image. An image is basically just a variable, which you then load with .blit.
# ExamplePNG = pygame.image.load('Graphics_Folder/Example.png')


# MAIN GAME LOOP. Running variable is what decides if loop is active.
running = True

while running:

    # This line here is essentially if it detects anything from player. Ex. a click, key down (i think), etc.
    for event in pygame.event.get():

        # checks if one of the events that occurred was the QUIT action (pressing the top right red x button)
        if event.type == pygame.QUIT:

            # If it was the quit button, the game loop turns off by turning running variable to false.
            running = False

    # These 2 lines are very important.

    # pygame.display.update() updates our display. It makes sure images gets loaded and essentially keeps everything on.
    pygame.display.update()

    # This ticks our fps clock with our FPS variable (set to 60). This makes sure our loop runs consistently.
    fpsClock.tick(FPS)