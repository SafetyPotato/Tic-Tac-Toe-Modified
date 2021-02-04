import sys
import database as db
import tkinter as tk
from PIL import ImageTk, Image
import types
from typing import Dict
from enum import Enum

class Neighbor():

    def __init__(self, row, col, markerRelation, next):
        self.row = row
        self.col = col
        self.relation = markerRelation
        self.next = next

class Marker():

    def __init__(self, row, col, pNum):
        self.row = row  #Not necessarily needed
        self.col = col
        self.pNum = pNum
        self.neighbors = Neighbor(None, None, None, None)


#Class that handles board interactions and game states
#Board state is tracked through a 2D array that contains 'Marker'
#nodes. These nodes contain a linked list of adjacent 'Neighbor' nodes
#that are the same type of marker. When the board is updated it checks
#to see if the newly placed marker is of the same type as any of the ones 
#adjacent to it. If it is, the markers essentially become doubly linked by 
#adding the other as a neighbor
class Engine():

    def __init__(self, parent, rows, cols, tally2win, numPlayers, playerList):

        self.rows = rows
        self.cols = cols
        self.tally2win = tally2win
        self.numPlayers = numPlayers
        self.playerList = playerList
        self.parent = parent    #Parent tkinter object
        self.markerCount = 0
        self.playerTurn = 1
        self.board = [[None] * cols for _ in range(rows)]



    def reverseDirection(self, dir):
        if(dir == 'N'):
            return 'S'
        elif(dir == 'S'):
            return 'N'
        elif (dir == 'E'):
            return 'W'
        elif (dir == 'W'):
            return 'E'
        elif (dir == 'NE'):
            return 'SW'
        elif (dir == 'SW'):
            return 'NE'
        elif (dir == 'NW'):
            return 'SE'
        elif (dir == 'SE'):
            return 'NW'


    def returnCoords(self, row, col, dir):
        if (dir == 'N'):
            return row-1, col
        elif (dir == 'S'):
            return row + 1, col
        elif (dir == 'E'):
            return row, col+1
        elif (dir == 'W'):
            return row, col-1
        elif (dir == 'NE'):
            return row-1, col+1
        elif (dir == 'SW'):
            return row+1, col-1
        elif (dir == 'NW'):
            return row-1, col-1
        elif (dir == 'SE'):
            return row + 1, col + 1


    #Checks if marker contained in board position, row1, col1, can be linked with another marker
    def checkIfValid(self, row1, col1, row2, col2):

        #Check if adjacent tile exists in board
        if(row2 >= self.rows or row2 < 0 or col2 >= self.cols or col2 < 0):
            return False

        #Check if tile is empty
        if(self.board[row2][col2] == None):
            return False

        #Check if markers are of same type
        if(self.board[row1][col1].pNum != self.board[row2][col2].pNum):
            return False

        return True


    #Add adjacent markers of same type to each others neighbor list and keep track of orientation
    def linkMarkers(self, marker1, marker2, relation):

        ptr = marker1.neighbors

        while ptr.next is not None:
            ptr = ptr.next

        ptr.next = Neighbor(marker2.row, marker2.col, relation, None)

        ptr = marker2.neighbors

        while ptr.next is not None:
            ptr = ptr.next

        ptr.next = Neighbor(marker1.row, marker1.col, self.reverseDirection(relation), None)



    def disable_buttons(self):
        for button in self.parent.buttonList:
            button['state'] = tk.DISABLED


    def displayWinner(self, isTie):

        top = tk.Toplevel(self.parent)
        top.geometry("+800+500")
        label = tk.Label(top)
        button = tk.Button(top, text="OK", command=lambda: top.destroy())

        label.pack(side='top')
        button.pack(side='bottom')

        if(not isTie):
            winner = self.playerList[self.playerTurn-1]
            label['text'] = winner + " is the winner!"
        else:
            winner = 'None'
            label['text'] = "Tie. Nobody wins!"

        db.update_score(self.playerList, winner)
        self.disable_buttons()

    #Recursive method that traverses markers of a specified type
    #in a given direction and returns the count
    def countMarkers(self, marker, dir, count):

        row, col = marker.row, marker.col
        row2, col2 = self.returnCoords(row, col, dir)  #Get coordindates for given direction

        #Return if specified adjacent marker is not the same
        if (not self.checkIfValid(row, col, row2, col2)):
            return count

        ptr = marker.neighbors

        #Search for neighbor in given direction
        while ptr.relation != dir:
            ptr = ptr.next

        #Continue search on neighbor marker
        if(ptr.relation == dir):
            count += 1
            vertex = self.board[ptr.row][ptr.col]
            count = self.countMarkers(vertex, dir, count)

        return count


    #Checks the 4 directions in which a game can be won
    def checkGameState(self, marker):

        count = 1
        count = self.countMarkers(marker, 'N', count)
        count = self.countMarkers(marker, 'S', count)

        if(count == self.tally2win):
            self.displayWinner(False)

        count = 1
        count = self.countMarkers(marker, 'E', count)
        count = self.countMarkers(marker, 'W', count)

        if (count >= self.tally2win):
            self.displayWinner(False)

        count = 1
        count = self.countMarkers(marker, 'NE', count)
        count = self.countMarkers(marker, 'SW', count)

        if (count == self.tally2win):
            self.displayWinner(False)

        count = 1
        count = self.countMarkers(marker, 'NW', count)
        count = self.countMarkers(marker, 'SE', count)

        if (count == self.tally2win):
            self.displayWinner(False)
   

    def updateBoard(self, row, col, button, imgList):
        
        #Place new marker on board
        marker = Marker(row, col, self.playerTurn)
        self.markerCount+= 1
        self.board[row][col] = marker

        #Place marker image and disable button
        button['image'] = imgList[self.playerTurn-1]
        button['state'] = tk.DISABLED

        #Check if there are any adjacent markers of same type to link
        if(self.checkIfValid(row, col, row-1, col)):
            self.linkMarkers(self.board[row][col], self.board[row -1][col], 'N')
        if(self.checkIfValid(row, col, row + 1, col)):
            self.linkMarkers(self.board[row][col], self.board[row  + 1][col], 'S')
        if(self.checkIfValid(row, col, row, col+1)):
            self.linkMarkers(self.board[row][col], self.board[row][col+1], 'E')
        if(self.checkIfValid(row, col, row, col-1)):
            self.linkMarkers(self.board[row][col], self.board[row][col-1], 'W')
        if(self.checkIfValid(row, col, row-1, col+1)):
            self.linkMarkers(self.board[row][col], self.board[row-1][col+1], 'NE')
        if (self.checkIfValid(row, col, row+1, col-1)):
            self.linkMarkers(self.board[row][col], self.board[row + 1][col - 1], 'SW')
        if (self.checkIfValid(row, col, row-1, col-1)):
            self.linkMarkers(self.board[row][col], self.board[row-1][col-1], 'NW')
        if (self.checkIfValid(row, col, row + 1, col + 1)):
            self.linkMarkers(self.board[row][col], self.board[row+1][col+1], 'SE')

        self.checkGameState(marker)

        #Check if board is full. If it is full the game is a tie
        if(self.markerCount == (self.rows*self.cols)):
            self.displayWinner(True)

        #Check if it's last players turn. If it is, loop back to first player.
        #Otherwise, increment normally
        if(self.playerTurn == self.numPlayers):
            self.playerTurn = 1
        else:
            self.playerTurn += 1
