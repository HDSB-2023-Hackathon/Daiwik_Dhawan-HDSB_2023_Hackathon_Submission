# Importing pygame library, so we can have a window and easily load images in.
import pygame

# Importing random library, used so we can randomly generate numbers/papers.
import random

# Start it up, and set our display to variable "screen" and size of whatever.
pygame.init()
screen = pygame.display.set_mode((1000, 1250))

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

# Gamestate is just a number to index the proper game function out of the gamestatelist. Starts at 0, goes up to 2.
gamestate = 0

# Below is a small matrix to organise our player statistics. The reason we don't have every stat as it's own variable
# is because it becomes annoying to deal with when our impactcode for papers uses just a single number to address
# each stat. While we could put the string to each variable in the impactcode and utilize the eval() command, it's
# a meh solution. So, we instead have a 2 row matrix, with each column being a stat. The first row is just a label,
# so we know what is what and the second row is the actual value from 0-100.
playerStats = [['Biodiversity', 'Happiness', 'Pollution', 'ClimateChange', 'Corruption', 'Budget', 'PoliticalSupport'],
               [50, 50, 50, 50, 0, 50, 50]]

# Choice papers (Will always just be list of 3 paper instances, refreshed after a paper has been chosen)
choicePapers = []

# Relating to list above, this variable is used to remember the paper the player is choosing to look at.
# This variable is always just a number used to index in the choicePapers list.
viewingPaper = 0

# Coords of mouse position. Starts at 0,0 before any initial clicks. Remember, the click position will be saved from
# last click if there hasn't been a recent one. If click statements might also use the presented clicking boolean
# value, which is False by default. We also have justClicked bool variable, which is very helpful if we ever want to
# turn the player holding down click to just check for the initial down click.
mousex, mousey = 0, 0
clicking = False
justClicked = False

# This is the total number of turns in the game. If the game has not already ended by this amount of turns/contracts
# signed via some alternate ending, it ends directly upon reaching this level.
TotalTurns = 20

# This is the variable that keeps track of how many turns have been played. If TurnsPlayed == TotalTurns, game ends.
TurnsPlayed = 0


# Main class for any paper object.
class Paper:
    # Potential paper variable, used for selecting the new choice papers.
    potentialPaper = 0

    # This is a list of all the papers that can be chosen at a point in time.
    # If a paper is suddenly enabled, it is put in here. If it is used, it is removed.
    activePapers = []

    # Number used to compare rarity of a paper and see if it is rare/common enough.
    paperRandNum = 0

    # These next lists are the different stages for papers. While some papers aren't part of a stage, and can be drawn
    # at any time, some papers can only be drawn if a certain paper has been passed before it.
    # Ex. CHAINGlobalDomination = [GlobalDomination1, GlobalDomination2, GlobalDomination3]
    # Each GlobalDomination list element would be a paper class instance.

    # This function returns a random paper in the activePapers list, based on each paper's rarity.
    def getPaper(self):
        # First shuffles the list of papers, so when it goes through them, it goes through them randomly.
        random.shuffle(self.__class__.activePapers)
        # Here we choose a random number from 1 to 100. Explained why on next line.
        self.__class__.paperRandNum = random.randint(1, 100)
        # Essentially, when we randomly go through the papers, we check their rarity. If their rarity is above the
        # random number we chose, we choose that paper. This means that if a paper's rarity value is a high number, it
        # is more likely to be chosen on average compared to a paper with a low rarity value.
        for paper in self.__class__.activePapers:
            if paper.rarity >= self.__class__.paperRandNum:
                return paper

    # Any paper has several points of info. These are defined when you create the instance of the paper.
    def __init__(self, enabled, rarity, contents, chained, chosenchain, impactcode):

        self.enabled = enabled  # Most paper are enabled by default. Only later stage papers of chained papers aren't.

        self.rarity = rarity  # When choosing a paper, it needs to be above a random number between 1-100.
        # Essentially, higher number = more common, low number = more rare.

        self.contents = contents  # This is just the text of the paper. Haven't really figured out this part yet.

        self.chained = chained  # This is a bool value, if a paper is chained this should be put to true.

        self.chosenchain = chosenchain  # If a paper is chained, put chain. Otherwise, just put 0 or something.
        # Make sure chain is in Paper.chainlistname format! Otherwise, probably won't work in paperUsed function.

        self.impactcode = impactcode  # This essentially stores all the information on how the paper signing will impact
        # the player statistics. Format is num of statistic, operation and then value. Different impacts are split by
        # the pipe symbol -> |  (Ex of an impactcode: 0x1.2|2+30|5-10)

        if self.enabled:  # Any paper (public or first stage chain type) gets added to the active paper list.
            self.__class__.activePapers.append(self)

    # This function occurs to only the paper that got chosen/signed by the player.
    def paperUsed(self):
        # Removes the chosen paper from the activePapers list, ensuring it can never be presented or selected again.
        self.__class__.activePapers.remove(self)

        # If this paper is part of a chain list, it adds the next paper in that chain list.
        if self.chained:

            # Here it tries to go to next paper by indexing the chosen paper in the chain list, adding 1 and then
            # indexing it again.
            try:
                self.__class__.activePapers.append(self.chosenchain[self.chosenchain.index(self) + 1])

            # If we get an error, which should only code failing to index in the list when the number exceeds the list,
            # we know we've done all the papers in that chain. This might lead to some specific function, but right now
            # it just prints an alert.
            except:
                print("A paper chain has run out/done its last paper!")

        # This applies the impactcode for the chosen paper. First it splits up the string via the pipes (|) and then
        # applies the math to each designated playerStat. This is kinda complicated so a typo/error might be present.
        for statImpact in self.impactcode.split('|'):
            playerStats[1][eval(statImpact[0])] = eval(
                f'{playerStats[1][eval(statImpact[0])]}{statImpact[1]}{statImpact[2:]}')

    # This function shuffles the 3 choice papers by basically called the getPaper function 3 times over.
    def shuffleChoicePaper(self):
        global choicePapers
        for i in range(3):
            self.__class__.potentialPaper = self.getPaper()
            while self.__class__.potentialPaper in choicePapers:
                self.__class__.potentialPaper = self.getPaper()
            choicePapers[i] = self.__class__.potentialPaper


# This gamestate just waits until the player clicks on the start button.
def startState():
    global gamestate

    # Remember to input correct location of start button, currently just from 0, 0 to 100, 100.
    if justClicked and 0 < mousex < 100 and 0 < mousey < 100:
        # We change the gamestate to 1, so we activate the main game sequence.
        gamestate += 1
        Paper.shuffleChoicePaper()


# This gamestate is the main state. It goes through a few phases:
# 1. Chooses 3 papers to be signed. Displays current player stats.
# 2. Waits until the player chooses one. Plays animation signing it and calculates the new player stats.

# Function for zoomed in view:
def mainZoomedIn():
    global viewingPaper
    global TurnsPlayed
    # WHEN GRAPHICS ADDED ADD IMAGE LOADING HERE, ALSO TEXT FOR THE CONTRACT UR LOOKING AT

    # Main check if there was a click. A click is the main way anything activates, so it's our main trigger for ifs.
    if justClicked:

        # If we're on the left or middle paper, check if they click on the right button. If they did, increase the
        # viewingPaper variable by 1, so we move one to the right.
        if viewingPaper < 2:
            if 0 < mousex < 100 and 0 < mousey < 100:
                viewingPaper += 1

        # If we're on the right or middle paper, check if they click on the left button. If they did, decrease the
        # viewingPaper variable by 1, so we move one to the left.
        if viewingPaper > 0:
            if 0 < mousex < 100 and 0 < mousey < 100:
                viewingPaper -= 1

        # Check if they clicked the check (sign/approve) button.
        if 0 < mousex < 100 and 0 < mousey < 100:
            # Play animation maybe?
            choicePapers[viewingPaper].paperUsed()
            TurnsPlayed += 1


# Function for zoomed out view:
def mainZoomedOut():
    global viewingPaper
    global mainZoomMode
    global mainZoomedIn
    # WHEN GRAPHICS ADDED, ADD IMAGE LOADING HERE
    # ALSO ADD TEXT RENDERING FOR STATS
    # Main check if the player clicked on one of the contracts (3 of them)
    if justClicked:
        # Check if click touched first contract.
        if 0 < mousex < 100 and 0 < mousey < 100:
            viewingPaper = 0
            mainZoomMode = mainZoomedIn()


# The main part of the game also has 2 views: Zoomed in and zoomed out. Both had different things to render and
# check. So, we have one variable that is either the zoomed in function mode or the zoomed out function mode. We just
# run the variable.
mainZoomMode = mainZoomedOut


def mainchooseState():
    mainZoomMode()


# This gamestate is basically just a display of what you've complished. You can't really do anything, you simply
# get to see your score and see what ending you accomplished.
def endscreenState():
    pass


# Our game has 3 main parts: 1. the start screen, 2. the actual game, and finally 3. the end screen.
# To easily designated function for each one, we put each of our different states (which are just functions that run
# every game loop) in a list, and index the one we want to run by just having a simple gamestate number (from 0-2).
gamestatelist = [startState, mainchooseState, endscreenState]


while running:

    # This line here is essentially if it detects anything from player. Ex. a click, key down (i think), etc.
    for event in pygame.event.get():

        # Checks if one of the events that occurred was the QUIT action (pressing the top right red x button)
        if event.type == pygame.QUIT:
            # If it was the quit button, the game loop turns off by turning running variable to false.
            running = False

        # Checks if one of the events that occurred was a mouse down action.
        if event.type == pygame.MOUSEBUTTONDOWN:
            # NOTE TO SELF: THIS IS ANY TYPE OF MOUSE CLICK. LEFT RIGHT WHATEVA. Here are states for dif button actions.
            # Check if event.button is equal to one of the following:
            # 1 - left click
            # 2 - middle click
            # 3 - right click
            # 4 - scroll up
            # 5 - scroll down

            # If we're not already clicking, meaning this is the first click, we turn the justClicked variable on. If
            # not, and we're already clicking, we turn it off again so justClicked is only on for that one frame/loop.
            if not clicking:
                justClicked = True
            else:
                justClicked = False

            # Here we turn the clicking value to True, since we just detected a click.
            clicking = True

            # Here we grab our mouseposition as a list with 2 elements, which we then save to our mousex and moousey.
            mouseposition = pygame.mouse.get_pos()
            mousex, mousey = mouseposition[0], mouseposition[1]

            # Print system that's useful to check if the mouse is working and if we need to troubleshoot positions.
            print(mousex, mousey)

        # Checks if one of the events that occurred was a mouse up action.
        if event.type == pygame.MOUSEBUTTONUP:
            # If the mouse is up, it's obviously not clicking, so we turn the value false.
            clicking = False
        # If you're wondering why we do an if statement here and not just an else or an elif, it's because we are also
        # checking other events, like pygame.QUIT. If we click, then next frame do another action like quit, our
        # clicking variable is wrong for a frame. While obviously this doesn't matter right now, if we ever add more
        # event checks, it's just a small source of error that we don't need.

    # Runs main game state function via indexing it out of our gamestatelist with our gamestate number.
    gamestatelist[gamestate]()

    # These 2 lines are very important.

    # pygame.display.update() updates our display. It makes sure images gets loaded and essentially keeps everything on.
    pygame.display.update()

    # This ticks our fps clock with our FPS variable (set to 60). This makes sure our loop runs consistently.
    fpsClock.tick(FPS)
