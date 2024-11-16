#importing pygame module for window and controls for the game
import pygame
pygame.init()
#importing random function to get a number when rolling the dice
import random
#importing all the constants in pygame
from pygame.locals import *
#importing sys module for information about functions and constants
import sys
#importing font and time from the pygame module 
from pygame import font
import time

#creating a class for each gride that will decide the colour at a certain coordinate
class gridObj:
    #initialising the object's attributes 
    def __init__(self, bgColour, player_s, safezone, coordinates):
        self.bgColour = bgColour
        self.player_s = player_s
        #if that location is safe for players to land
        self.safezone = safezone
        #holding the player's the location
        self.coordinates = coordinates


#creating a token for each of the four players
class Token:
    #holding information for each token
    def __init__(self, I_d, colour, state, coordinates, rsize):
        #token's Id
        self.I_d = I_d
        #token's colour
        self.colour = colour
        #token's radius state
        self.state = state
        #token's coordinates
        self.coordinates = coordinates
        #token's size
        self.rsize=rsize
        #token's location
        self.original_coordinates = coordinates

#creating the global variables that will be used while creating and running the game
#holds the center locations of the grid for red, blue, green and red
cList = [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (7, 0), (8, 0), (8, 1),
          (8, 2), (8, 3), (8, 4), (8, 5), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (14, 7),(14, 8), (13, 8),
          (12, 8), (11, 8), (10, 8), (9, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (7, 14),(6, 14), (6, 13),
          (6, 12), (6, 11), (6, 10), (6, 9), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7),(0, 6)]
#holds the initial positions of the tokens
initialPos=[[[1,1],[1,4],[4,1],[4,4]],[[10,1],[13,1],[10,4],[13,4]],[[1,10],[4,10],[1,13],[4,13]],[[10,10],[10,13],[13,10],[13,13]]]
#holds the names of the tokens
names=['Red','Green','Blue','Yellow']
#height of the game 
height = 1000
#size for the game
width = 1000
#initial x coordinates
initx = 0
#initial y coordinates
inity = 0
#holds the name of the player playing the game
currentPlayer = 'Red'
#holds the locations of the four tokens in case the game mode is with Computer
compTokensLoc=[[1,1],[1,4],[4,1],[4,4]]
#holds the number of players being played depending on the user's decision
n=2
#True when the game is being played with the computer
withComputer=True
#False if being played with other users
dice_rolled = False
move_list = []
#setting dice value to 6
diceValue = 6
#game window
Game_grid = [[-1 for _ in range(15)] for _ in range(15)]
colours=['white','red','green','yellow','blue','black']
#setting the color to the locations on the grid based on the colors in the colors list
colourMatrix = [[-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 2, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 2, 2, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
                [0, 1, 1, 1, 1, 1, 0, 5, 0, 4, 4, 4, 4, 4, 0],
                [0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0],
                [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 3, 3, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 3, 3, 0, -1, -1, -1, -1, -1, -1],
                [-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1]]
coordinateMatrix = [[[initx + i * 50, inity + j * 50] for i in range(0, 15)] for j in range(0, 15)]
#making the locations where multiple tokens can stay
safezoneLocs=[[6,2],[8,1],[12,6],[13,8],[8,12],[6,13],[2,8],[1,6]]
safezoneMatrix = [[0 for i in range(15)] for j in range(15)]

#if the location is safe then these locations are set 1 in the safeMatrix
for i in safezoneLocs:
    safezoneMatrix[i[0]][i[1]] = 1

#creating the dice values on the screen
FacesofDice = {1: [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
           2: [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
           3: [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
           4: [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
           5: [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
           6: [[1, 0, 1], [1, 0, 1], [1, 0, 1]],
               }
#creating the 15×15 grid objects for the window
for i in range(15):
    for j in range(15):
        #assigning its attributes
        object = gridObj(colours[colourMatrix[i][j]], [], safezoneMatrix[i][j], coordinateMatrix[i][j])
        Game_grid[i][j] = object
#creating the 4 tokens for each color
for j in range(4):
    for i in range(1,5):
        t=initialPos[j][i-1]
        #adding the colour, size and additional properties
        Red= Token(names[j]+str(i), colours[j+1], 0, (50 *t[0] , 50 * t[1]), 20)
        Game_grid[t[0]][t[1]].player_s.append(Red)
#creating a function to draw the grid and execute in the main while loop to show the updates on the screen
def drawingGrid():
    #creating a global variable
    global Game_grid
    #creating the surface of the height and width
    newSurface = pygame.display.set_mode((height, width))
    newSurface.fill('#00AADA')
    #setting grid coordinates
    for i in range(15):
        for j in range(15):
            pygame.draw.rect(newSurface, Game_grid[i][j].bgColour, tuple(Game_grid[i][j].coordinates + [50, 50]))
            pygame.draw.rect(newSurface, (0, 0, 0), tuple(Game_grid[i][j].coordinates + [50, 50]), 1)

    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[1], (initx, inity, 300, 300))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[0], (initx + 50, inity + 50, 200, 200))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[2], (initx + 450, inity, 300, 300))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[0], (initx + 500, inity + 50, 200, 200))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[3], (initx, inity + 450, 300, 300))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[0], (initx + 50, inity + 500, 200, 200))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[4], (initx + 450, inity + 450, 300, 300))
    #creating the surface of the height and width which will remain constant.
    pygame.draw.rect(newSurface, colours[0], (initx + 500, inity + 500, 200, 200))
    
    #drawing the boxes that holds the four tokens on the four corners
    for i in range(15):
        #for loop iterates through the columns in the game grid
        for j in range(15):
            #function call calculates the relative position of the tokens for the current cell
            relativeToken(Game_grid[i][j].player_s, i * 50, j * 50)
            #for loop iterates through the players in the current cell
            for m in Game_grid[i][j].player_s:
                #gets the coordinates of the current player's token
                d = m.coordinates
                #draws the player's token on the surface
                pygame.draw.circle(newSurface, m.colour, (d[0] + 25, d[1] + 25), m.rsize)
                #draws the outline of the player's token on the surface
                pygame.draw.circle(newSurface, colours[-1], (d[0] + 25, d[1] + 25), m.rsize, 1)
                #checks if the player is the current player and if so, draws a highlight around their token
                if m.I_d[0] == currentPlayer:
                    pygame.draw.circle(newSurface, colours[0], (d[0] + 25, d[1] + 25), m.rsize - 2, 2)
    #sets the face of the dice to be displayed
    faces = FacesofDice[diceValue]
    #iterates through the rows in the dice face
    for i in range(3):
        #iterates through the columns in the dice face
        for j in range(3):
            #draws a black square at the current position
            pygame.draw.rect(newSurface, 'black', ((0 + 800) + (50 * j), (0 + 300) + (50 * i), 50, 50))
            #checks if the current position in the dice face should have a token and if so, draws it
            if faces[i][j] == 1:
                #gets the index of the current player and adds one to it to get the color index
                cIndex=names.index(currentPlayer)+1
                #draws the token for the current player at the current position in the dice face
                pygame.draw.circle(newSurface, colours[cIndex], ((0 + 800) + (50 * j) + 25, (0 + 300) + (50 * i) + 25),
                                   10)
    #draws the dice with its attributes and the current player's token
    pygame.draw.rect(newSurface, colours[names.index(currentPlayer)+1], ((0 + 798), (0 + 298), 150, 150), 4)
    #returns the surface with all the elements drawn on it
    return newSurface

#creating a function to be able to control the movement based on the value of the dice
def token_moves(initialPos, value, current):
    #initialise i to 0
    i = 0
    #initialise j to -1
    j = -1
    #initialise flag to 0
    flag = 0
    #start an infinite loop
    while True:
        #position for tokens
        #if the current position matches the initial position or j is greater than or equal to 0
        if cList[i] == initialPos or j >= 0:
            #position for red
            #if the current player is red and the index i is equal to 50
            if current == 'Red' and i == 50:
                #set flag to 1
                flag = 1
            #position for green
            #if the current player is green and the index i is equal to 11
            if current == 'Green' and i == 11:
                #set flag to 2
                flag = 2
            #position for blue
            #if the current player is blue and the index i is equal to 37
            if current == 'Blue' and i == 37:
                #set flag to 3
                flag = 3
            #position for yellow
            #if the current player is yellow and the index i is equal to 24
            if current == 'Yellow' and i == 24:
                #set flag to 4
                flag = 4
            #increment j by 1
            j += 1
            if j == value:
                #exit the loop
                break
        #increment i by 1 and get the remainder of i divided by the length of cList
        i = (i + 1) % len(cList)
    #making the rules for the flag
    if flag == 1:
        #return a tuple with the first element as the x-coordinate incremented by 1 
        #and the second element as the y-coordinate incremented by 1
        return (cList[i][0] + 1, cList[i][1] + 1)
    #mkaing the rules for the flag
    elif flag == 2:
        #return a tuple with the first element as the x-coordinate incremented by 1 
        #and the second element as the y-coordinate incremented by 1
        return (cList[i][0] + 1, cList[i][1] + 1)
    #mkaing the rules for the flag
    elif flag == 3:
        #return a tuple with the first element as the x-coordinate incremented by 1 
        #and the second element as the y-coordinate incremented by 1
        return (cList[i][0] + 1, cList[i][1] - 1)
    #mkaing the rules for the flag
    elif flag == 4:
        #return a tuple with the first element as the x-coordinate incremented by 1
        #and the second element as the y-coordinate incremented by 1
        return (cList[i][0] - 1, cList[i][1] - 1)
    else:
        #return a tuple with the current x
        return (cList[i][0], cList[i][1])

#creating a function for the tokens based of their coordinates
def relativeToken(tList, x, y):
    #alculate the length of the player list
    l = len(tList)
    #calculate the relative radius of each token
    relRad = int((2 / (l + 1)) * 20)
    #create an empty list to store the relative positions of the tokens
    relpt = []
    #initialise a counter variable
    j = 0
    #calculate the relative positions of the tokens based on whether the length of the list is even or odd
    if l % 2 == 0:
        l1 = [i + 1 for i in range((l // 2))]
        l2 = [i - 1 for i in range((l // 2))]
        relpt = l2[::-1] + l1
    #calculate the relative positions of the tokens based on whether the length of the list is even or odd
    else:
        l1 = [i + 1 for i in range((l // 2))]
        l2 = [i - 1 for i in range((l // 2))]
        relpt = l2[::-1] + [0] + l1
    #set the size and coordinates of each player token based on its position in the list and the relative radius
    for t in tList:
        #set the size of the token
        t.rsize = relRad
        #set the coordinates of the token based on its position in the list and the relative radius
        t.coordinates = ((x) + (relpt[j] * (relRad // 2)), (y))
        #increment the counter variable
        j += 1

#function that returns if the position of the token is in the cList
def check(pos):
    if pos in cList:
        return True
    else:
        return False
#returns the corresponding position in the grid for the given token position  
def grid_location(pos):
    x = pos[0]
    y = pos[1]
    #position is calculated by dividing the x and y values of the token position by 50 
    #and returning the result as a tuple
    return (x // 50, y // 50)
#function to check if two tokens are in the same location     
def check_collision(tList):
    #global variables
    global currentPlayer
    global Game_grid
    new_list=[]
    #checking tokens in the player list
    for t in tList:
        #adding the current player's token to the new list
        if t.I_d[0] == currentPlayer:
            new_list.append(t)
        #moving the other tokens to their original positions and updating the Game_grid accordingly
        else:
            t.coordinates=t.original_coordinates
            i=t.coordinates[0]//50
            j=t.coordinates[1]//50
            Game_grid[i][j].player_s.append(t)
    return new_list
#checking which token has been moved
def checkI_d(tList):
    global currentPlayer
    for i in tList:
        #returns True if the token belongs to the current player
        if i.I_d[0] == currentPlayer:
            return True
    return False

#checking the number of tokens
def compLoc(diceValue):
    #global variable
    global compTokensLoc
    #saving tokens positions
    saveLocs=[(1, 7),(2, 7),(3, 7),(4, 7),(5, 7),(6, 7),(7, 7)]
    #list to save tokens at initial position
    initial=[]
    #saving other tokens of players
    players=[]
    #checking the initial position of each token and adding them to appropriate list
    if(compTokensLoc[0]==[1,1]):
        initial.append(0)
    #checking the initial position of each token and adding them to appropriate list
    else:
        players.append(0)
    #checking the initial position of each token and adding them to appropriate list
    if(compTokensLoc[1]==[1,4]):
        initial.append(1)
    #checking the initial position of each token and adding them to appropriate list
    else:
        players.append(1)
    #checking the initial position of each token and adding them to appropriate list
    if(compTokensLoc[2]==[4,1]):
        initial.append(2)
    #checking the initial position of each token and adding them to appropriate list
    else:
        players.append(2)
    #checking the initial position of each token and adding them to appropriate list
    if(compTokensLoc[3]==[4,4]):
        initial.append(3)
    else:
        players.append(3)
    #checking if the dice value is 6 and there are tokens at initial position to move
    #then move a random token to the first position on the board
    if(diceValue==6 and len(initial)>0):
        tkn=random.randint(1,len(initial))
        compTokensLoc[tkn-1]=cList[0]
        return compTokensLoc[tkn-1]
    #if all tokens are already on board, then select a random token to move
    count=len(compTokensLoc)-len(initial)
    print(initial)
    if(count<=0):
        return (1,1)
    if(count>0):
        #get the index of the token to be moved in the list of other players' tokens
        tkn=random.randint(1,count)
        tkn=players[tkn-1]
        print(tkn)
        ind=cList.index(compTokensLoc[tkn])
        #check if the token is at a location to be saved
        if(compTokensLoc[tkn] in saveLocs):
            ind=saveLocs.index(compTokensLoc[tkn])
            #check if the token can be moved ahead by the dice value without going out of range
            if((ind+diceValue) <=(len(saveLocs-1))):
                compTokensLoc[tkn]=saveLocs[ind+diceValue]
                return compTokensLoc[tkn]
            #if token can't be moved ahead without going out of range, call the function again
            else:
                compLoc(diceValue)
        #if token is not at a saved location, move it ahead by the dice value
        elif(ind+diceValue<len(cList)-1):
            compTokensLoc[tkn]=cList[ind+diceValue]
        #if moving the token ahead by the dice value takes it out of range, move it to a saved location
        else:
            stepsLeft= diceValue-(len(cList)-1)
            compTokensLoc[tkn]=saveLocs[stepsLeft-1]
        return compTokensLoc[tkn] 
#function to change to the next player
def Player_next():
    #access global variables 'n' and 'currentPlayer'
    global n,currentPlayer
    #if the number of players is 2
    if(n==2):
        #if the current player is red
        if currentPlayer == 'Red':
            #set the current player to blue
            currentPlayer = 'Blue'
        #if the current player is blue
        elif currentPlayer == 'Blue':
            #set the current player to red
            currentPlayer = 'Red'
    #if the number of players is 3
    elif(n==3):
        #if the current player is red
        if currentPlayer == 'Red':
            #set the current player to green
            currentPlayer = 'Green'
        #if the current player is green
        elif currentPlayer == 'Green':
            #set the current player to yellow
            currentPlayer = 'Yellow'
        #if the current player is yellow
        elif currentPlayer == 'Yellow':
            #set the current player to red
            currentPlayer = 'Red'
    #if the number of players is 4
    elif(n==4):
        #if the current player is red
        if currentPlayer == 'Red':
            #set the current player to green
            currentPlayer = 'Green'
        #if the current player is green
        elif currentPlayer == 'Green':
            #set the current player to yellow
            currentPlayer = 'Yellow'
        #if the current player is yellow
        elif currentPlayer == 'Yellow':
            #set the current player to red
            currentPlayer = 'Red'
        #if the current player is blue
        elif currentPlayer == 'Blue':
            #set the current player to red
            currentPlayer = 'Red'
#access global variable 'DISPLAY'
global DISPLAY

def mainGame():
    #Define the size of the display window
    height = 1000
    width = 800
    #Initialise Pygame library
    pygame.init()
    #Creating a Pygame display surface with the specified dimensions
    DISPLAY = pygame.display.set_mode((height, width))
    #Setting the caption of the Pygame window
    pygame.display.set_caption('LuCraze')
    #Declaring global variables that are used throughout the game
    global cList, initialPos,names,initx,inity,currentPlayer,n,dice_rolled,move_list,diceValue,Game_grid,colours,colourMatrix, coordinateMatrix,safezoneMatrix,safezoneLocs,FacesofDice
    #Creating a font object
    font = pygame.font.SysFont("Arial", 40,'bold')
    #Creating a label to display the name of the game
    label = font.render("LuCraze", 1, 'White')
    #starting the game loop
    while (True):
        #Check for Pygame events
        for event in pygame.event.get():
            #If the game is being played against the computer and it is the computer's turn, or if the user clicks the mouse
            if(withComputer and currentPlayer=='Red') or event.type == MOUSEBUTTONDOWN:
                #If the game is being played against the computer and it is the computer's turn
                if(withComputer and currentPlayer=='Red'):
                    #Computer generates a random location to move
                    loc=compLoc(random.randint(1, 6))
                    #The dice has been clicked
                    dice_rolled == True
                #If the user clicks the mouse
                elif event.type == MOUSEBUTTONDOWN:
                    #Get the location of the mouse click on the game grid
                    loc = grid_location(event.pos)
                #If the user clicks the dice button
                if (loc[0] >= 16 and loc[0] <= 18 and loc[1] >= 6 and loc[1] <= 8 and dice_rolled == False):
                    #Generate a random dice value between 1 and 6
                    diceValue = random.randint(1, 6)
                    #Display the dice value
                    print("dice rolled", currentPlayer)
                    #The dice has been clicked
                    dice_rolled = True
                #If the dice value is not 6 and the dice has been clicked
                if diceValue != 6 and dice_rolled == True:
                    print(1)
                    #Initialize the flag variable to 0
                    flag = 0
                    #Iterate over all cells on the game grid
                    for i in cList:
                        #Iterate over all players in the current cell
                        for p in Game_grid[i[0]][i[1]].player_s:
                            #If the current player's ID is found in the cell's player list, set the flag variable to 1
                            if p.I_d[0] == currentPlayer:
                                flag = 1
                    #If the current player has no more moves, move to the next player and reset the dice click status
                    if flag == 0:
                        Player_next()
                        dice_rolled = False
                #If it is the red player's turn and the dice value is 6 and the location of the click is in the red home column
                if currentPlayer == 'Red' and diceValue == 6 and (loc in [(1, 1), (4, 1), (4, 4), (1, 4)]) and dice_rolled == True:
                    #Print the number 2
                    print(2)
                    #Print the list of players in the current position on the game grid
                    print(Game_grid[1][6].player_s)
                    #Move the player from the start position to the first safe position
                    Game_grid[1][6].player_s.append(Game_grid[loc[0]][loc[1]].player_s[0])
                    #Update the player's coordinates to the new position
                    Game_grid[1][6].player_s[-1].coordinates = (50 * 1, 50 * 6)
                    #Print the coordinates of all players in the new position
                    for t in Game_grid[1][6].player_s:
                        print(t.coordinates)
                    #Remove the player from the start position
                    Game_grid[loc[0]][loc[1]].player_s = []
                    #Reset the dice click flag
                    dice_rolled = False
                #If the current player is green, the dice value is 6, and the click is on one of the start positions
                elif currentPlayer == 'Green' and diceValue == 6 and (loc in [(10, 1), (13, 1), (13, 4), (10, 4)]) and dice_rolled == True:
                    #Print the number 3
                    print(3)
                    #Print the list of players in the current position on the game grid
                    print(Game_grid[8][1].player_s)
                    #Move the player from the start position to the first safe position
                    Game_grid[8][1].player_s.append(Game_grid[loc[0]][loc[1]].player_s[0])
                    #Update the player's coordinates to the new position
                    Game_grid[8][1].player_s[-1].coordinates = (50 * 8, 50 * 1)
                    #Remove the player from the start position
                    Game_grid[loc[0]][loc[1]].player_s = []
                    print(Game_grid[8][1].player_s[0].I_d)
                    #Reset the dice click flag
                    dice_rolled = False
                #If the current player is blue, the dice value is 6, and the click is on one of the start positions
                elif currentPlayer == 'Blue' and diceValue == 6 and (loc in [(1, 10), (4, 10), (4, 13), (1, 13)]) and dice_rolled == True:
                    #Print the number 5
                    print(5)
                    #Print the list of players in the current position on the game grid
                    print(Game_grid[6][13].player_s)
                    #Move the player from the start position to the first safe position
                    Game_grid[6][13].player_s.append(Game_grid[loc[0]][loc[1]].player_s[0])
                    #Update the player's coordinates to the new position
                    Game_grid[6][13].player_s[-1].coordinates = (50 * 6, 50 * 13)
                    #Remove the player from the start position
                    Game_grid[loc[0]][loc[1]].player_s = []
                    #Reset the dice click flag
                    dice_rolled = False
                #If the current player is yellow, the dice value is 6, and the click is on one of the start positions
                elif currentPlayer == 'Yellow' and diceValue == 6 and (loc in [(10, 10), (13, 10), (13, 13), (10, 13)]) and dice_rolled == True:
                    #Print the number 4
                    print(4)
                    #Print the list of players in the current position on the game grid
                    print(Game_grid[13][8].player_s)
                    #Move the player from the start position to the first safe position
                    Game_grid[13][8].player_s.append(Game_grid[loc[0]][loc[1]].player_s[0])
                    #Update the player's coordinates to the new position
                    Game_grid[13][8].player_s[-1].coordinates = (50 * 13, 50 * 8)
                    #Remove the player from the start position
                    Game_grid[loc[0]][loc[1]].player_s = []
                    #Reset the dice click flag
                    dice_rolled = False
                #Checks the current player, the player's location is one of the middle positions
                elif currentPlayer == 'Red' and (loc in [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7)]) and len(
                        #there is at least one player in the current position on the game grid, and the dice has been clicked
                        Game_grid[loc[0]][loc[1]].player_s) > 0 and dice_rolled == True:
                    #Check if the player can move within the boundaries of the game grid
                    if loc[0] + diceValue <= 6:
                        #Move the player to the new position
                        Game_grid[loc[0] + diceValue][loc[1]].player_s.append(Game_grid[loc[0]][loc[1]].player_s[-1])
                        #Update the player's coordinates to the new position
                        Game_grid[loc[0] + diceValue][loc[1]].player_s[-1].coordinates = (
                        50 * (loc[0] + diceValue), 50 * (loc[1]))
                        #Remove the player from the previous position
                        Game_grid[loc[0]][loc[1]].player_s = Game_grid[loc[0]][loc[1]].player_s[:-1]
                    #Reset the dice click flag
                    dice_rolled = False
                #Checks the current player, the player's location is one of the middle positions
                elif currentPlayer == 'Green' and (loc in [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)]) and len(
                        #there is at least one player in the current position on the game grid, and the dice has been clicked
                        Game_grid[loc[0]][loc[1]].player_s) > 0 and dice_rolled == True:
                    #Check if the player can move within the boundaries of the game grid
                    if loc[1] + diceValue <= 6:
                        #Move the player to the new position
                        Game_grid[loc[0]][loc[1] + diceValue].player_s.append(Game_grid[loc[0]][loc[1]].player_s[-1])
                        #Update the player's coordinates to the new position
                        Game_grid[loc[0]][loc[1] + diceValue].player_s[-1].coordinates = (
                            50 * (loc[0]), 50 * (loc[1] + diceValue))
                        #Remove the player from the previous position
                        Game_grid[loc[0]][loc[1]].player_s = Game_grid[loc[0]][loc[1]].player_s[:-1]
                    #Reset the dice click flag
                    dice_rolled = False
                #Checks the current player, the player's location is one of the middle positions
                elif currentPlayer == 'Blue' and (loc in [(7, 9), (7, 10), (7, 11), (7, 12), (7, 13)]) and len(
                        #there is at least one player in the current position on the game grid, and the dice has been clicked
                        Game_grid[loc[0]][loc[1]].player_s) > 0 and dice_rolled == True:
                    #Check if the player can move within the boundaries of the game grid
                    if loc[1] + diceValue >= 8:
                        #Move the player to the new position
                        Game_grid[loc[0]][loc[1] + diceValue].player_s.append(Game_grid[loc[0]][loc[1]].player_s[-1])
                        #Update the player's coordinates to the new position
                        Game_grid[loc[0]][loc[1] + diceValue].player_s[-1].coordinates = (
                            50 * (loc[0]), 50 * (loc[1] + diceValue))
                        #Remove the player from the previous position
                        Game_grid[loc[0]][loc[1]].player_s = Game_grid[loc[0]][loc[1]].player_s[:-1]
                    #Reset the dice click flag
                    dice_rolled = False
                #Checks the current player, the player's location is one of the middle positions
                elif currentPlayer == 'Yellow' and (loc in [(9, 7), (10, 7), (11, 7), (12, 7), (13, 7)]) and len(
                        #there is at least one player in the current position on the game grid, and the dice has been clicked
                        Game_grid[loc[0]][loc[1]].player_s) > 0 and dice_rolled == True:
                    #Check if the player can move within the boundaries of the game grid
                    if loc[0] - diceValue >=8:
                        #Move the player to the new position
                        Game_grid[loc[0] - diceValue][loc[1]].player_s.append(Game_grid[loc[0]][loc[1]].player_s[-1])
                        #Update the player's coordinates to the new position
                        Game_grid[loc[0] - diceValue][loc[1]].player_s[-1].coordinates = (
                            50 * (loc[0] - diceValue), 50 * (loc[1]))
                        #Remove the player from the previous position
                        Game_grid[loc[0]][loc[1]].player_s = Game_grid[loc[0]][loc[1]].player_s[:-1]
                    #Reset the dice click flag
                    dice_rolled = False
                #Check if the player can move to the new position, the current position has a player with the current player's ID, 
                #and the dice has been clicked
                elif (check(loc)) and checkI_d(Game_grid[loc[0]][loc[1]].player_s) and dice_rolled == True:
                    print(6)
                    #Get the new position based on the dice roll and the current position
                    newpos = token_moves(loc, diceValue, currentPlayer)
                    new_list = []
                    flg = 0
                    #Iterate over the list of players in the current position
                    for i in Game_grid[loc[0]][loc[1]].player_s:
                        #Check if the player has the current player's ID and the flag is not set
                        if i.Id[0] == currentPlayer and flg == 0:
                            #Move the player to the new position
                            Game_grid[newpos[0]][newpos[1]].player_s.append(i)
                            #Update the player's coordinates to the new position
                            Game_grid[newpos[0]][newpos[1]].player_s[-1].coordinates = (50 * newpos[0], 50 * newpos[1])
                            #Check if the player can eat other pieces
                            Game_grid[newpos[0]][newpos[1]].player_s=check_collision(Game_grid[newpos[0]][newpos[1]].player_s)
                            #Set the flag to indicate that the player has been moved
                            flg = 1
                        else:
                            #Add the player to the new list of players in the current position
                            new_list.append(i)
                    #Update the list of players in the current position with the new list
                    Game_grid[loc[0]][loc[1]].player_s = new_list
                    #Reset the dice click flag
                    dice_rolled = False
                    #If the dice roll is not 6, switch to the next player
                    if diceValue != 6:
                        Player_next()
            #Draw the game grid and the dice roll label on the game screen
            font1 = pygame.font.SysFont("Arial", 50)
            label1 = font1.render(str(diceValue), 1, 'black')

            DISPLAY.blit(drawingGrid(), (0, 0))
            DISPLAY.blit(label, (800, 10))
            DISPLAY.blit(label1, (850, 500))
            pygame.display.update()

            #Check if the user has clicked the close button on the game window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

pygame.init()
#crearing screen
screen = pygame.display.set_mode((1000, 800))
#Title of screen
pygame.display.set_caption('LuCraze')
#setting clock/time
clock = pygame.time.Clock()
#font for the writing
font = pygame.font.SysFont("Arial", 20)
 #creating a button class
class Button:
    #initalising the button with its text, players, font size, bg and feedback
    def __init__(self, text,num,comp,pos, font, bg="blue", feedback=""):
        #position
        self.x, self.y = pos
        #font
        self.font = pygame.font.SysFont("Arial", font)
        #number of players
        self.no=num
        #text
        self.text=text
        #text colour
        self.text = self.font.render(self.text, 1, pygame.Color("White"))
        #playing with computer
        self.cmp=comp
        #background colour
        self.change_text(bg)
    #updating button's colour
    def change_text(self, bg="blue"):
        #size of button text
        self.size = self.text.get_size()
        #size
        self.surface = pygame.Surface(self.size)
        #background colour
        self.surface.fill(bg)
        self.surface.blit(self.text, (0, 0))
        #updating
        self.rect = pygame.Rect(self.x, self.y, self.size[0], self.size[1])
    #blits the button's text on the screen at its position
    def show(self):
        screen.blit(self.text , (self.x, self.y))
    #checking mouse movement
    def click(self, event):
        #mouse position
        x, y = pygame.mouse.get_pos()
        #font
        f1 = pygame.font.SysFont("Arial", 50)
        #text on first screen
        l1 = f1.render("LuCraze", 1, '#00AADA')
        #position
        screen.blit(l1, (410, 30))
        #checks if the left mouse button is clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                #checking if mouse is hovering over the button's rectangular area
                if self.rect.collidepoint(x, y):
                    # sets the global variables n and with computer
                    global n,withComputer
                    n=self.no
                    withComputer=self.cmp
                    print(n,",",withComputer)
                    #exits the game
                    pygame.quit()
                    mainGame()
 
#infinite loop that handles pygame events
def mainloop():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            #checks for button clicks
            b1.click(event)
            #checks for button clicks
            b2.click(event)
            #checks for button clicks
            b3.click(event)
            #checks for button clicks
            b4.click(event)
        #displays the buttons
        b1.show()
        #displays the buttons
        b2.show()
        #displays the buttons
        b3.show()
        #displays the buttons
        b4.show()
        #updates the screen,
        clock.tick(30)
        pygame.display.update()
 
#setting each button with its text, font size and colour
b1 = Button(
    "Play with Computer",2,True,
    (400, 150),
    font=30,
    bg="white")
#setting each button with its text, font size and colour
b2 = Button(
    "2 Players",2,False,
    (400, 250),
    font=30,
    bg="white")
#setting each button with its text, font size and colour
b3 = Button(
    "3 Players",3,False,
    (400, 350),
    font=30,
    bg="white",)
#setting each button with its text, font size and colour
b4 = Button(
    "4 Players",4,False,
    (400, 450),
    font=30,
    bg="white",)
#running event loop
mainloop()
