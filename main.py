# Importing pygame library, so we can have a window and easily load images in.
import pygame

# Importing random library, used so we can randomly generate numbers/papers.
import random
from pygame import mixer

#Instantiate mixer
mixer.init()

PaperSlideSOUND = pygame.mixer.Sound('Sound_Folder/SlidingPaper.wav')
BasicButtonSOUND = pygame.mixer.Sound('Sound_Folder/BasicButton.wav')
SpecialButtonSOUND = pygame.mixer.Sound('Sound_Folder/SpecialButton.wav')


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

ZoomedOutPNG = pygame.image.load('Graphics_Folder/ZoomedOut.png')
ZoomedInPNG = pygame.image.load('Graphics_Folder/ZoomedIn.png')
RightArrowPNG = pygame.image.load('Graphics_Folder/RightArrow.png')
LeftArrowPNG = pygame.image.load('Graphics_Folder/LeftArrow.png')
MainMenuPNG = pygame.image.load('Graphics_Folder/MainMenu.png')
BoringEndPNG = pygame.image.load('Graphics_Folder/BoringEnd.png')
EcoEndPNG = pygame.image.load('Graphics_Folder/EcoEnding.png')
MoneyEndPNG = pygame.image.load('Graphics_Folder/MoneyEnding.png')
DictatorEndPNG = pygame.image.load('Graphics_Folder/DictatorEnding.png')
GreedEndPNG = pygame.image.load('Graphics_Folder/GreedEnding.png')

# Different endings
chosenEnding = 0
difEndings = [BoringEndPNG, EcoEndPNG, MoneyEndPNG, GreedEndPNG, DictatorEndPNG]
endScorePositions = [[320, 500, 500, 631, 550],
                     [654, 170, 170, 917, 850]]
# Loading of the icon image we have.
icon = pygame.image.load('Graphics_Folder/Logo.png')
pygame.display.set_icon(icon)

# MAIN GAME LOOP. Running variable is what decides if loop is active.
running = True

# Gamestate is just a number to index the proper game function out of the gamestatelist. Starts at 0, goes up to 2.
gamestate = 0

smallfont = pygame.font.Font('freesansbold.ttf', 32)

# Below is a small matrix to organise our player statistics. The reason we don't have every stat as it's own variable
# is because it becomes annoying to deal with when our impactcode for papers uses just a single number to address
# each stat. While we could put the string to each variable in the impactcode and utilize the eval() command, it's
# a meh solution. So, we instead have a 2 row matrix, with each column being a stat. The first row is just a label,
# so we know what is what and the second row is the actual value from 0-100.
playerStats = [['Biodiversity: %', 'Happiness: %', 'Pollution: %', 'Budget: %', 'Corruption: ', 'ClimateChange: ', 'PoliticalSupport: '],
               [100, 50, 50, 50, 0, 50, 50]]

# Choice papers (Will always just be list of 3 paper instances, refreshed after a paper has been chosen)
choicePapers = [0, 0, 0]

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
TotalTurns = 10

# This is the variable that keeps track of how many turns have been played. If TurnsPlayed == TotalTurns, game ends.
TurnsPlayed = 0


# Main class for any paper object.
class Paper:
    # Variable used to check requirements for when a paper is selected
    requirementFail = False

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

    # REMEMBER TO PUT CHAIN LISTS HERE!!!!!
    CHAINEcoEnding = []
    CHAINMoneyEnding = []
    CHAINGreedEnding = []
    CHAINDictatorEnding = []

    difChains = [CHAINEcoEnding, CHAINMoneyEnding, CHAINGreedEnding, CHAINDictatorEnding]

    # This function returns a random paper in the activePapers list, based on each paper's rarity.
    @staticmethod
    def getPaper():
        while True:
            # First shuffles the list of papers, so when it goes through them, it goes through them randomly.
            random.shuffle(Paper.activePapers)
            # Here we choose a random number from 1 to 100. Explained why on next line.
            Paper.paperRandNum = random.randint(1, 100)
            # Essentially, when we randomly go through the papers, we check their rarity. If their rarity is above the
            # random number we chose, we choose that paper. This means that if a paper's rarity value is a high number,
            # it is more likely to be chosen on average compared to a paper with a low rarity value.
            for paper in Paper.activePapers:
                if paper.rarity >= Paper.paperRandNum:
                    if len(paper.requirements) < 3:
                        return paper
                    else:
                        Paper.requirementFail = False
                        # Checks each requirement
                        for requirement in paper.requirements.split('|'):
                            # If a requirement didn't pass we want to restart, so we have a fail variable.
                            if not eval(f'{playerStats[1][eval(requirement[0])]}{requirement[1]}{requirement[2:]}'):
                                Paper.requirementFail = True
                        if not Paper.requirementFail:
                            return paper

    # Any paper has several points of info. These are defined when you create the instance of the paper.
    def __init__(self, enabled, rarity, contents, chained, chosenchain, impactcode, requirements):

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

        self.requirements = requirements  # Requirements for a paper to be chosen. If a paper is chosen from the
        # shuffled activePapers and passes the rarity check, this is the final challenge for it. Format for each
        # requirement is index of stat, operator (< or >, really) and then the number to compare to. There should also
        # be a pipe symbol between each different requirement. This system is rather similar to the impactcode system.

        if self.enabled:  # Any paper (public or first stage chain type) gets added to the active paper list.
            self.__class__.activePapers.append(self)

        if self.chained:
            self.chosenchain.append(self)

    # This function occurs to only the paper that got chosen/signed by the player.
    def paperUsed(self):
        global gamestate
        global chosenEnding
        # Removes the chosen paper from the activePapers list, ensuring it can never be presented or selected again.
        print("PAPER USED!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
        print(self.__class__.activePapers)
        print(self)
        self.__class__.activePapers.remove(self)
        for paper in self.__class__.activePapers:
            print(paper.contents)

        # If this paper is part of a chain list, it adds the next paper in that chain list.
        if self.chained:

            # Here it tries to go to next paper by indexing the chosen paper in the chain list, adding 1 and then
            # indexing it again.
            try:
                self.__class__.activePapers.append(self.chosenchain[self.chosenchain.index(self) + 1])
                print(self.chosenchain[self.chosenchain.index(self) + 1].contents)

            # If we get an error, which should only code failing to index in the list when the number exceeds the list,
            # we know we've done all the papers in that chain. This might lead to some specific function, but right now
            # it just prints an alert.
            except:
                print("A paper chain has run out/done its last paper!")
                gamestate += 1
                chosenEnding = Paper.difChains.index(self.chosenchain) + 1

        # This applies the impactcode for the chosen paper. First it splits up the string via the pipes (|) and then
        # applies the math to each designated playerStat. This is kinda complicated so a typo/error might be present.
        # Also, we do use eval here (which is known as insecure) but that's only when inputs are like freely inputted.
        # This eval will only be in contact with input from when we created the program, nothing from the player.
        for statImpact in self.impactcode.split('|'):
            playerStats[1][eval(statImpact[0])] = eval(
                f'{playerStats[1][eval(statImpact[0])]}{statImpact[1]}{statImpact[2:]}')

    # This function shuffles the 3 choice papers by basically called the getPaper function 3 times over.
    @staticmethod
    def shuffleChoicePaper():
        global choicePapers
        for i in range(3):
            Paper.potentialPaper = Paper.getPaper()
            while Paper.potentialPaper in choicePapers:
                Paper.potentialPaper = Paper.getPaper()
            choicePapers[i] = Paper.potentialPaper


# Instantiate all paper instances here:

# Biodiversity 0, Happiness 1, Pollution 2, Budget 3, Corruption 4, ClimateChange 5, PoliticalSupport 6
CHAINEcoEnding1 = Paper(True, 100, "You have received a great opportunity, with a chance to decrease pollution and "
                                   "climate change. This would all be free as well, if you just tax your citizens "
                                   "enough...", True, Paper.CHAINEcoEnding, '2-10|5-10|1-15', '')
CHAINEcoEnding2 = Paper(False, 100, "Your past plan of taxing your citizen to afford environment worked great! A new "
                                    "plan to increase biodiversity has been introduced, only costing a small part of "
                                    "your budget. The major funding would come from your citizens...", True, Paper.CHAINEcoEnding, '0+20|3-5|1-25', '')
CHAINEcoEnding3 = Paper(False, 100, "Taxing the people might not have been wisest choice, as now even your political "
                                    "friends are slightly against you. But is it really time to back off? The "
                                    "environment is almost saved, and you just got the opportunity to completely "
                                    "eliminate climate change!", True, Paper.CHAINEcoEnding, '6-10|5*0|1-20', '')
CHAINEcoEnding4 = Paper(False, 100, "People are starving, and your political friends and opponenets have backed off."
                                    " You're just a sign away to completely save the environment..", True, Paper.CHAINEcoEnding, '0*2|1-40|2*0|5*0|6-20', '')
CHAINMoneyEnding1 = Paper(True, 100, "Theres an amazing opportunity for you to clear the Amazon rainforest for immense"
                                     " natural resources. This would give great money for your citizens and yourself,"
                                     " but it might just hurt the environment a little.", True, Paper.CHAINMoneyEnding, '1+15|3+15|5+10', '')
CHAINMoneyEnding2 = Paper(False, 100, "There a lot of species that are dying due to the Amazon rainforest incident, and"
                                     " you're not sure what to do. Do you want to ignore these dying species, and simply"
                                     " use them their leftovers for manufacturing products?", True, Paper.CHAINMoneyEnding, '0-30|1+20|3+10|4+15', '')
CHAINMoneyEnding3 = Paper(False, 100, "The environment is hurting, and all that manufacturing might just start mass "
                                      "pollution and climate change. Continue sacrificing the environment for your and "
                                      "the people's money?", True, Paper.CHAINMoneyEnding, '5+30|2+30|1+15|3+45', '')
CHAINMoneyEnding4 = Paper(False, 100, "The Earth is not what it once was. Your destructive campaign has let society to "
                                      "prosper, but not nature. Finish what you started?", True, Paper.CHAINMoneyEnding, '1*1.5|3*2|2+50|5+50|0-50', '')
CHAINGreedEnding1 = Paper(True, 100, "You feel the uncontrollable urge for money, and for power. How about starting some"
                                     " trouble to get just that? Nobody really cares about animals after all.", True, Paper.CHAINGreedEnding, '0-30|4+30', '')
CHAINGreedEnding2 = Paper(False, 100, "People are starting to wonder what happened to the wildlife around them, but"
                                      " what they don't know won't hurt them. Continue sacrificing nature and people for money?", True, Paper.CHAINGreedEnding, '1-10|0-10|3+10|4+20', '')
CHAINGreedEnding3 = Paper(False, 100, "People and your political friends are confused. What's going on, why is the "
                                      "environment suffering, and how are you becoming so rich? Let's put them in the "
                                      "grave, and throw away the help given to climate change.", True, Paper.CHAINGreedEnding, '1-10|4+20|6-10|5-50', '')
CHAINDictatorEnding1 = Paper(True, 100, "Finally, after all these years, you've gained true power. It's time to show "
                                        "these people and this world who controls everything. Start propaganda?", True, Paper.CHAINDictatorEnding, '1-10|4+10|6-10', '')
CHAINDictatorEnding2 = Paper(False, 100, "People are becoming scared, but just think how good they have it. "
                                         "The environment is suffering, and with your power, you can fix it. Start "
                                         "forcing random people to participate in manual labour to help?", True, Paper.CHAINDictatorEnding, '1-30|3+10|6-10|0+15|2-10', '')
CHAINDictatorEnding3 = Paper(False, 100, "Your control over your people is growing ever stronger, and you realize you"
                                         " are on top. Who cares about the people's feelings; they've already destroyed "
                                         "the environment's feelings. Save the environment, and teach these weaklings "
                                         "their final lesson?", True, Paper.CHAINDictatorEnding, '1-60|6-30|5-10|0+10|2-10', '')

# Common papers
PaperName = Paper(True, 100, "Ban strikes", False, 0, '1-2|4+1|6+1', '')
PaperName1 = Paper(True, 100, "Taxes levied based on wealth", False, 0, '1+15|3+25|4-5|6-15', '')
PaperName2 = Paper(True, 100, "Discourage Coal based power", False, 0, '1+5|6-0.1', '')
PaperName3 = Paper(True, 100, "Increase logging subsidies", False, 0, '1-5|0-5|4+5|5+2|6+1', '')
PaperName4 = Paper(True, 100, "Subsidise Electric Cars", False, 0, '1+5', '')
PaperName5 = Paper(True, 100, "Assassinate Opposition", False, 0, '4+2|6+1', '')
PaperName6 = Paper(True, 100, "Increase racism towards minorities", False, 0, '1-20|4+10|6+25', '')
PaperName7 = Paper(True, 100, "Officially switch to Nuclear Power as majority of energy source", False, 0, '1+1|2-1|6-2', '')
PaperName8 = Paper(True, 100, "Defund the police", False, 0, '1+10|4-10', '')
PaperName9 = Paper(True, 100, "Assassinate Donald Trump", False, 0, '1+20|6-10', '')
PaperName10 = Paper(True, 100, "Initiate 4-Day work weeks", False, 0, '1+20|6-5', '')
PaperName11 = Paper(True, 100, "Regulate Oil Companies", False, 0, '1+5|2-10|5-5', '')
PaperName12 = Paper(True, 100, "Make Abortion Illegal", False, 0, '1-20|4+5|5+10', '')
# PaperName8 = Paper(True, 100, "", False, 0, '', '')


# This gamestate just waits until the player clicks on the start button.
def startState():
    global gamestate

    screen.blit(MainMenuPNG, (0, 0))

    # Remember to input correct location of start button, currently just from 0, 0 to 100, 100.
    if justClicked and 184 < mousex < 848 and 922 < mousey < 1091:
        # We change the gamestate to 1, so we activate the main game sequence.
        gamestate += 1
        Paper.shuffleChoicePaper()
        pygame.mixer.Sound.play(SpecialButtonSOUND)


# This gamestate is the main state. It goes through a few phases:
# 1. Chooses 3 papers to be signed. Displays current player stats.
# 2. Waits until the player chooses one. Plays animation signing it and calculates the new player stats.

# Function for zoomed in view:
def mainZoomedIn():
    global viewingPaper
    global TurnsPlayed
    global mainZoomMode
    global gamestate
    # WHEN GRAPHICS ADDED, ADD IMAGE LOADING HERE, ALSO TEXT FOR THE CONTRACT UR LOOKING AT
    screen.blit(ZoomedInPNG, (0, 0))

    LawTextYAdjust = 274
    numOfCharacters = 0
    curLine = ''
    print(choicePapers[viewingPaper].contents)

    for character in choicePapers[viewingPaper].contents:
        numOfCharacters += 1
        curLine = f'{curLine}{character}'
        if numOfCharacters > 25 and character == ' ':
            screen.blit(smallfont.render(f'{curLine}', True, (0, 0, 0)), (267, LawTextYAdjust))
            LawTextYAdjust += 45
            curLine = ''
            numOfCharacters = 0
    screen.blit(smallfont.render(f'{curLine}', True, (0, 0, 0)), (267, LawTextYAdjust))

    # Check to see if we need to load the right button (If we're on the left or middle paper)
    if viewingPaper < 2:
        screen.blit(RightArrowPNG, (0, 0))

    # Check to see if we need to load the left button (If we're on the right or middle paper)
    if viewingPaper > 0:
        screen.blit(LeftArrowPNG, (-15, 0))

    # Main check if there was a click. A click is the main way anything activates, so it's our main trigger for ifs.
    if justClicked:

        # If we're on the left or middle paper, check if they click on the right button. If they did, increase the
        # viewingPaper variable by 1, so we move one to the right.
        if viewingPaper < 2:
            if 789 < mousex < 980 and 481 < mousey < 671:
                viewingPaper += 1
                pygame.mixer.Sound.play(PaperSlideSOUND)

        # If we're on the right or middle paper, check if they click on the left button. If they did, decrease the
        # viewingPaper variable by 1, so we move one to the left.
        if viewingPaper > 0:
            if 11 < mousex < 213 and 477 < mousey < 678:
                viewingPaper -= 1
                pygame.mixer.Sound.play(PaperSlideSOUND)

        # Check if they clicked the check (sign/approve) button.
        if 489 < mousex < 742 and 869 < mousey < 961:
            # Play animation maybe?
            choicePapers[viewingPaper].paperUsed()
            Paper.shuffleChoicePaper()
            mainZoomMode = mainZoomedOut
            print(playerStats[1][1])
            TurnsPlayed += 1
            pygame.mixer.Sound.play(SpecialButtonSOUND)
            if TurnsPlayed == TotalTurns:
                gamestate += 1

        # Check if they clicked the back (to view states) button.
        if 313 < mousex < 691 and 1073 < mousey < 1194:
            mainZoomMode = mainZoomedOut
            pygame.mixer.Sound.play(BasicButtonSOUND)


# Function for zoomed out view:
def mainZoomedOut():
    global viewingPaper
    global mainZoomMode
    global mainZoomedIn
    # WHEN GRAPHICS ADDED, ADD IMAGE LOADING HERE
    # ALSO ADD TEXT RENDERING FOR STATS
    screen.blit(ZoomedOutPNG, (0, 0))
    screen.blit(smallfont.render(f'{playerStats[0][0]}{playerStats[1][0]}', True, (0, 0, 0)), (394, 188))
    screen.blit(smallfont.render(f'{playerStats[0][1]}{playerStats[1][1]}', True, (0, 0, 0)), (394, 258))
    screen.blit(smallfont.render(f'{playerStats[0][2]}{playerStats[1][2]}', True, (0, 0, 0)), (394, 338))
    screen.blit(smallfont.render(f'{playerStats[0][3]}{playerStats[1][3]}', True, (0, 0, 0)), (394, 408))
    # print('mainzoomedout')

    # Main check if the player clicked on one of the contracts (3 of them)
    if justClicked:

        # Check if click touched first contract.
        if 302 < mousex < 377 and 877 < mousey < 989:
            viewingPaper = 0
            mainZoomMode = mainZoomedIn
            pygame.mixer.Sound.play(PaperSlideSOUND)

        # Check if click touched second contract.
        elif 479 < mousex < 556 and 879 < mousey < 991:
            viewingPaper = 1
            mainZoomMode = mainZoomedIn
            pygame.mixer.Sound.play(PaperSlideSOUND)

        # Check if click touched third contract.
        elif 666 < mousex < 744 and 877 < mousey < 989:
            viewingPaper = 2
            mainZoomMode = mainZoomedIn
            pygame.mixer.Sound.play(PaperSlideSOUND)


# The main part of the game also has 2 views: Zoomed in and zoomed out. Both had different things to render and
# check. So, we have one variable that is either the zoomed in function mode or the zoomed out function mode. We just
# run the variable.
mainZoomMode = mainZoomedOut


def mainchooseState():
    mainZoomMode()


# This gamestate is basically just a display of what you've complished. You can't really do anything, you simply
# get to see your score and see what ending you accomplished.
def endscreenState():
    # LOAD BACKGROUND
    # Biodiversity [0], Happiness [1], Pollution [2], Budget [3], Corruption [4], ClimateChange [5], PoliticalSupport[6]
    screen.blit(difEndings[chosenEnding], (0, 0))
    FinalScore = (playerStats[1][0] + playerStats[1][1] - playerStats[1][2] + playerStats[1][3] - playerStats[1][5]) / playerStats[1][4] * playerStats[1][6]
    screen.blit(smallfont.render(f'{FinalScore}', True, (0, 0, 0)), (endScorePositions[0][chosenEnding], endScorePositions[1][chosenEnding]))


# Our game has 3 main parts: 1. the start screen, 2. the actual game, and finally 3. the end screen.
# To easily designated function for each one, we put each of our different states (which are just functions that run
# every game loop) in a list, and index the one we want to run by just having a simple gamestate number (from 0-2).
gamestatelist = [startState, mainchooseState, endscreenState]

while running:
    justClicked = False

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

            # This event only occurs on the initial click, so we turn on justClicked. If you look a few lines above, you
            # will see justClicked is turned off in the beginning/by default.
            justClicked = True

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
