from random import randint
from os import system, path
from time import sleep
from playsound import playsound #requires playsound 1.2.2

boardsize = 5       #default board size
round = 0
lost = False
numberGuess = boardsize**2
player = ""
playAgain = True
turn = 0
playerScore = 0
computerScore = 0
cannonSoundPath = path.dirname(__file__) + '\\Cannon.mp3'
explosionSoundPath = path.dirname(__file__) + '\\Explosion.mp3'

class Brd:
    def __init__(self, name, size, score, listofcoordinates=[]):
        self.name = name
        self.size = size
        self.score = score
        self.listofcoordinates = listofcoordinates
        self.listofcoordinates.append([" "," ","1","2","3","4","5"," <--col"])
        self.listofcoordinates.append([" "]+[" "]+(["_"] * 5))
        for x in range(5):
            self.listofcoordinates.append([f"{x+1}"]+["|"]+(["O"] * 5))
        self.listofcoordinates.append(["^"])
        self.listofcoordinates.append(["|"])
        self.listofcoordinates.append(["row"])

    def print(self, value):
        print(f"{self.name}'s field      Score: {value}")
        print("===================")
        for row in self.listofcoordinates:
            print(" ".join(row))
        print("===================")

def randomNumber(size):
    return randint(3, size + 2)

#error handling
def validateInput(input):
    if input == "" :
        return 1
    if input.isalpha():
        return "Invalid input. Enter a number"
    elif int(input) < 1 or int(input) > boardsize :
            return f"Invalid input. Enter a number from 1 to {boardsize}"
    else :
        return 0

#get value of axis and handle invalid inputs
def axisInput(axis):
    returnValue = None
    while True :
        errorHandle = 0
        if axis == "Row" :
            returnValue = input("Row: (leave blank to randomize): ")
        elif axis == "Col" :
            returnValue = input("Col: (leave blank to randomize): ")
        errorHandle = validateInput(returnValue)
        if errorHandle == 1 :
            returnValue = randomNumber(myBrd.size)
            break
        elif errorHandle == 0 :
            returnValue = int(returnValue) + 2
            break
        else :
            print(f"{errorHandle}")
            sleep(1)
            continue
    return returnValue
#display welcome screen    
system("cls")
print("=" * 50)
print("- !!!Battleship!!!")
print(f"- Try to hit your opponent's Battleship by taking a guess between 1 and {boardsize} for row & column")
print(f"- You have {numberGuess} turns to try to hit your oppponent's battleship")
print("=" * 50 + "\n")
player = input(f"what is your name:")
system("cls")

while True :
    round += 1
    
    #initialize Boards
    enemyBrd = Brd("Computer", boardsize, computerScore, [])
    myBrd = Brd(player, boardsize, playerScore, [])
    myBrd.print(playerScore) 

    #initialize ship positions
    print(f"Place your ship:")
    myShipRow = int(axisInput("Row"))
    myShipCol = int(axisInput("Col"))
    enemyShipRow = randomNumber(enemyBrd.size)
    enemyShipCol = randomNumber(enemyBrd.size)
    #place your ship on the map coordinates
    myBrd.listofcoordinates[myShipRow-1][myShipCol-1] = "∆"    
    #Print empty boards
    system("cls")
    print(f"Round: {round}")
    enemyBrd.print(computerScore)
    myBrd.print(playerScore) 
    #for troubleshooting
    #print(f"actual enemy position at {enemyShipRow},{enemyShipCol}")
    #print(f"adjusted enemy position at {enemyShipRow-2},{enemyShipCol-2}")
    #print(f"actual position of my ship at {myShipRow},{myShipCol}")
    #print(f"adjusted position of my ship at {myShipRow-2},{myShipCol-2}")
    # Player's turn
    for attempt in range(1,numberGuess+1,1):
        print("\n")
        #guess_row = int(input("Guess Row:"))+2
        #guess_col = int(input("Guess Col:"))+2
        guess_row = int(axisInput("Row"))
        guess_col = int(axisInput("Col"))
        if guess_row == enemyShipRow and guess_col == enemyShipCol:
            system("cls")
            playerScore += 1
            print(f"Round: {round}")
            enemyBrd.print(computerScore)
            myBrd.print(playerScore)
            print("You guessed row: %d column: %d" % (guess_row-2,guess_col-2))
            playsound(cannonSoundPath)
            enemyBrd.listofcoordinates[guess_row-1][guess_col-1] = "⨻"
            system("cls")
            print(f"Round: {round}")
            enemyBrd.print(computerScore)
            myBrd.print(playerScore)
            print("Congratulations! You sunk my battleship!")
            playsound(explosionSoundPath)
            break
        else:
            #if (guess_row <= 2 or guess_row > boardsize +2) or (guess_col <= 2 or guess_col > boardsize + 2):
            #    print("Out of bounds.")
            #    sleep(1)
            if(enemyBrd.listofcoordinates[guess_row-1][guess_col-1] == "X"):
                print("You guessed that one already!!!")
                sleep(1)
            else:
                enemyBrd.listofcoordinates[guess_row-1][guess_col-1] = "X"
                system("cls")
                print(f"Round: {round}")
                enemyBrd.print(computerScore)
                myBrd.print(playerScore)
                print("You guessed row: %d column: %d" % (guess_row-2,guess_col-2))
                playsound(cannonSoundPath)
                print("You missed computer's battleship!")
                sleep(1)
        print ("Turn %d \n" % (turn + 1) )
        system("cls")
        print(f"Round: {round}")
        enemyBrd.print(computerScore)
        myBrd.print(playerScore)
        # Enemy's Turn
        print("Enemy is thinking!")
        sleep(2)
        while True :
            enemy_guess_row = randomNumber(myBrd.size)
            enemy_guess_col = randomNumber(myBrd.size)
            if enemy_guess_row == myShipRow and enemy_guess_col == myShipCol:
                lost = True 
                computerScore += 1
                break
            else:
                if(myBrd.listofcoordinates[enemy_guess_row-1][enemy_guess_col-1] == "X"):
                    continue
                else:
                    myBrd.listofcoordinates[enemy_guess_row-1][enemy_guess_col-1] = "X"
                    break                
        system("cls")
        print(f"Round: {round}")
        enemyBrd.print(computerScore)
        myBrd.print(playerScore)
        print("Computer guessed row: %d column: %d" % (enemy_guess_row-2,enemy_guess_col-2))
        playsound(cannonSoundPath)
        if lost :
            myBrd.listofcoordinates[enemy_guess_row-1][enemy_guess_col-1] = "⨻"
            system("cls")
            print(f"Round: {round}")
            enemyBrd.print(computerScore)
            myBrd.print(playerScore)
            print("You Lose!!!!")
            playsound(explosionSoundPath)
            break
        else :            
            print("Computer missed your battleship!")
            sleep(1)
    playagainanswer = input("Do you want to play again? press (y) to play again? ")
    if playagainanswer.lower() != "y" :
        print(f"FINAL SCORE: {player}: {playerScore} Computer: {computerScore} ")
        print("Thank you for playing")
        break
    
                 

    
        