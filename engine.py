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

class Engine():

    def __init__(self, parent, rows : int, cols : int, tally2win : int, numPlayers : int, playerList):

        self.rows = rows
        self.cols = cols
        self.tally2win = tally2win
        self.numPlayers = numPlayers
        self.playerList = playerList
        self.parent = parent
        self.markerCount = 0
        self.playerTurn : int = 1
        self.board = [[None] * cols for _ in range(rows)]

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

    def checkIfValid(self, row1, col1, row2, col2):

        if(row2 >= self.rows or row2 < 0 or col2 >= self.cols or col2 < 0):
            return False

        if(self.board[row2][col2] == None):
            return False

        if(self.board[row1][col1].pNum != self.board[row2][col2].pNum):
            return False

        return True

    def linkMarkers(self, marker1, marker2, relation):

        ptr = marker1.neighbors

        while ptr.next is not None:
            ptr = ptr.next

        ptr.next = Neighbor(marker2.row, marker2.col, relation, None)

        ptr = marker2.neighbors

        while ptr.next is not None:
            ptr = ptr.next

        ptr.next = Neighbor(marker1.row, marker1.col, self.reverseDirection(relation), None)

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

    def updateBoard(self, row, col, button, imgList):

        marker = Marker(row, col, self.playerTurn)
        self.markerCount+= 1
        self.board[row][col] = marker

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

        button['image'] = imgList[self.playerTurn-1]
        button['state'] = tk.DISABLED

        self.checkGameState(marker)

        if(self.markerCount == (self.rows*self.cols)):
            self.displayWinner(True)

        if(self.playerTurn == self.numPlayers):
            self.playerTurn = 1
        else:
            self.playerTurn += 1

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

    def dfs(self, marker, dir, count):

        row, col = marker.row, marker.col
        row2, col2 = self.returnCoords(row, col, dir)

        if (not self.checkIfValid(row, col, row2, col2)):
            return count

        ptr = marker.neighbors

        while ptr.relation != dir:
            ptr = ptr.next

        if(ptr.relation == dir):
            count+=1
            vertex = self.board[ptr.row][ptr.col]
            count = self.dfs(vertex, dir, count)

        return count

    def checkGameState(self, marker):
        count = 1

        count = self.dfs(marker, 'N', count)
        count = self.dfs(marker, 'S', count)

        if(count == self.tally2win):
            self.displayWinner(False)

        count = 1
        count = self.dfs(marker, 'E', count)
        count = self.dfs(marker, 'W', count)

        if (count >= self.tally2win):
            self.displayWinner(False)

        count = 1
        count = self.dfs(marker, 'NE', count)
        count = self.dfs(marker, 'SW', count)

        if (count == self.tally2win):
            self.displayWinner(False)


        count = 1
        count = self.dfs(marker, 'NW', count)
        count = self.dfs(marker, 'SE', count)

        if (count == self.tally2win):
            self.displayWinner(False)