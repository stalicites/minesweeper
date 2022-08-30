# Python Class 3251
# Lesson 9 Problem 1
# Author: cdm (472521)

# from logging import root
from tkinter import *
import random


'''
Specifically, write a function $\verb#play_minesweeper(width,height,numBombs)#$ that launches a tkinter window to play the game Minesweeper on a $width \times height$ board of squares, with $numBombs$ of the squares randomly selected to contain bombs.

The goal in Minesweeper is to expose all the squares that do not contain bombs. The player exposes a square by left-clicking on it.

-- If the square contains a bomb, KABOOM! -- the game is over and the player loses. The game should display all of the remaining unexposed, unflagged bombs. (See below about "flagging".)

-- If the square does not contain a bomb, it displays a number that indicates the number of adjacent squares (including diagonally-adjacent) that contain a bomb. (If none of the adjacent squares contain a bomb, the exposed square is blank -- you can optionally have the game auto-expose all of the adjacent squares, because since you know that none of them are bombs, it's safe to do so.) If the player successfully exposes all the non-bomb squares, the player wins.

The player may also flag squares that he/she believes to contain a bomb, by right-clicking on them. Flagged squares should display as asterisks, and cannot be exposed unless they are unflagged by again right-clicking on them (which also removes the asterisk). The game should also display the number of bombs minus the number of placed flags.

'''


class Tile():

    # display a minesweeper tile in tkinter

    def __init__(self, master, x, y, state, bomb):
        self.master = master
        self.x = x
        self.y = y
        self.state = state
        self.bomb = bomb
        self.button = Button(master, command = self.expose, bg="red")
        self.button.grid(row = x, column = y)
        self.button.config(width=4, height=2)
        self.button.bind("<Button-2>", self.flag)


    def expose(self):
        # expose tile
        print("Clicked on: ", self.x, self.y)
        if self.bomb == False and self.state != 1 and self.master.gameState == 1:
            self.state = 1
            adjacentTiles = self.getAdjacent()

            print("Adjacente Tiles: ", adjacentTiles)

            adjacentBombTiles = []
            
            for tile in adjacentTiles:
                if self.master.board[tile].bomb == True:
                    print("Bomb tile: ", tile)
                    adjacentBombTiles.append(tile)
            
            self.button.config(text = str(len(adjacentBombTiles)))

            print("Tile (" + str(self.x) + ", " + str(self.y) + ") has ", adjacentBombTiles)

            if len(adjacentBombTiles) == 0:
                self.button.config(text = ".")
                self.master.checkWin()
                print("Adjacent tiles is: ", adjacentTiles)
                for tile in adjacentTiles:
                    if self.master.board[tile].state != 1 and self.master.board[tile].bomb == False:
                        self.master.board[tile].expose()
            self.master.checkWin()
        else:
            if self.bomb == True:
                self.button.config(text = "X", fg = "red")
                self.state = 1
                self.master.gameState = 0
                self.master.flagsLabel.config(text="Kaboom! You lose!")
                for tile in self.master.board:
                    if self.master.board[tile].bomb == True and self.master.board[tile].state != 1:
                        self.master.board[tile].expose()
    
    def flag(self, event):
        # flag tile
        print("Flag ran! Flags left: ", self.master.flagsLeft)
        if self.state == 0 and self.master.flagsLeft > 0 and self.master.gameState == 1:
            self.button.config(text = "*", fg="black")
            self.state = 2 
            self.master.flagsLeft -= 1
            self.master.flagsLabel.config(text="Flags left: " + str(self.master.flagsLeft)) 
            self.master.checkWin()
        elif self.state == 2:
            self.button.config(text = "")
            self.state = 0
            self.master.flagsLeft += 1
            self.master.flagsLabel.config(text="Flags left: " + str(self.master.flagsLeft)) 
            self.master.checkWin()
        else:
            pass

    def getAdjacent(self):
        # get adjacent tiles
        adjacent = []

        coords = [
            {"x": self.x-2,  "y": self.y-1},  #top right
            {"x": self.x-2,  "y": self.y},    #top middle
            {"x": self.x-2,  "y": self.y+1},  #top left
            {"x": self.x-1, "y": self.y-1},  #left
            {"x": self.x-1, "y": self.y+1},  #right
            {"x": self.x, "y": self.y-1},  #bottom right
            {"x": self.x,  "y": self.y},    #bottom middle
            {"x": self.x,  "y": self.y+1},  #bottom left
        ]

        for c in coords:
            if (c["x"], c["y"]) in self.master.board:
                adjacent.append((c["x"], c["y"]))
        return adjacent

class Minesweeper(Frame):

    def __init__(self, width, height, bombCount, root):
        Frame.__init__(self, root)
        # tkinter.messagebox.showinfo("Welcome!", "This game assumes you know how to play Minesweeper.\n\nIf you don't, head over to thier Wikipedia page.\nhttps://en.wikipedia.org/wiki/Minesweeper_(video_game)")
        self.grid()
        self.width = width
        self.height = height
        self.bombCount = bombCount
        self.gameState = 1 # 1 = playing, 0 = game over
        self.board = {}
        self.flagsLeft = self.bombCount

        self.flagsLabel = Label(self, text = "Flags left: " + str(self.flagsLeft)) 
        self.flagsLabel.grid(row = 0, column = 0, columnspan = 10, sticky=W)

        for i in range(0, self.height):
            for j in range(1, self.width):
                self.board[(i, j)] = Tile(self, i + 1, j, 0, False)

        self.placeBombs()


    def placeBombs(self):
        availableSquares = []
        for i in self.board:
            if self.board[i].state == 0 and self.board[i].bomb != True:
                availableSquares.append(i)
        
        random.shuffle(availableSquares)

        for i in range(self.bombCount):
            self.board[availableSquares[i]].bomb = True
            self.board[availableSquares[i]].button.config(fg="red")
    
    def checkWin(self):
        for i in self.board:
            if self.board[i].bomb == False and self.board[i].state == 0:
                return False
        self.flagsLabel.config(text="You win! Congrats!")
        self.gameState = 2
        for tile in self.board:
            if self.board[tile].bomb == True:
                self.board[tile].button.config(text="X", fg = "blue")
        return True
        

root = Tk()
root.title("Minesweeper")
game = Minesweeper(12, 10, 20, root)
game.mainloop()