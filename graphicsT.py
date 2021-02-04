from engine import Engine
import database as db
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as ft
from tkinter import filedialog
from typing import Dict
from PIL import ImageTk, Image
import os
import copy


class OptionWindow(tk.Tk):


    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        self.playerData = {}
        self.playerWindow = None
        self.playerWindowOpened = False
        self.playerNamesEntered = False

        self.geometry("650x500+600+275")
        self.resizable(height = False, width = False)

        self.mainFrame = tk.Frame(self,)
        self.mainFrame.pack(expand = True, fill = "both")
        self.myFont = ft.Font(size=10, weight="bold")

        self.create_frames()
        self.create_labels()
        self.create_entryBoxes()
        self.create_buttons()
        self.create_radioButtons()


    def create_frames(self):
        self.frame0_0 = tk.Frame(self.mainFrame)
        self.frame1_0 = tk.Frame(self.mainFrame)
        self.frame2_0 = tk.Frame(self.mainFrame)
        self.frame3_1 = tk.Frame(self.mainFrame)

        self.frame0_0.grid(row=0, column=0, sticky="NW", columnspan=1)
        self.frame1_0.grid(row=1, column=0, sticky="NW", columnspan=1)
        self.frame2_0.grid(row=2, column=0, sticky="NW", columnspan=1)
        self.frame3_1.grid(row=3, column=1, sticky="S", columnspan=1)


    def create_labels(self):
        label_entry = tk.Label(self.frame1_0, text="Board Size", font=ft.Font(size=10, weight="bold"))
        label_multiply = tk.Label(self.frame1_0, text="x", font= self.myFont)
        label_tallies = tk.Label(self.frame1_0, text="Tallies to Win", font= self.myFont)
        label_playerCount = tk.Label(self.frame2_0, text="Player Count", font= self.myFont)

        label_entry.grid(row=0, column=0, sticky="NW", padx=(16, 0), pady=(20, 0), columnspan=10)
        label_multiply.grid(row=1, column=1, sticky="NW", columnspan=1)
        label_tallies.grid(row=2, column=0, sticky="NW", padx=(16, 0), pady=(15, 0), columnspan=10)
        label_playerCount.grid(row=0, column=0, sticky="NW", padx=(16, 0), pady=(20, 0), columnspan=4)


    def create_entryBoxes(self):
        self.entry_xSize = tk.Entry(self.frame1_0, width=2, font=ft.Font(size=10))
        self.entry_ySize = tk.Entry(self.frame1_0, width=2, font=ft.Font(size=10))
        self.entry_tally2win = tk.Entry(self.frame1_0, width=5, font=ft.Font(size=10))

        self.entry_xSize.grid(row=1, column=0, sticky="NW", padx=(20, 0), columnspan=1)
        self.entry_ySize.grid(row=1, column=2, sticky="NW", columnspan=1)
        self.entry_tally2win.grid(row=3, column=0, sticky="NW", columnspan=15, padx = 20)


    def create_buttons(self):
        #Radio buttons need to be turned off when hitting default game in the event that custom game is chosen after
        button_defaultGame = tk.Button(self.frame0_0, text="Default Game", font=self.myFont,
                                       command=lambda: [self.set_default_data(2), self.start_game("3", "3", 2, 3), self.r.set("0")])

        self.button_setPlayer = tk.Button(self.frame2_0, text="Set Player Names/Icons", font= self.myFont,
                                     command = lambda: self.open_player_window(self.r.get()))
        self.button_startGame = tk.Button(self.frame3_1, text="Start Game", font= self.myFont, bg="green",
                                     command=lambda: self.start_game(self.entry_xSize.get(), self.entry_ySize.get(),
                                                                     self.r.get(), self.entry_tally2win.get()))

        button_defaultGame.grid(row=0, column=0, sticky="NW", ipadx=10, ipady=5, padx=(20, 0), pady=(20, 0),
                                columnspan=4)

        self.button_setPlayer.grid(row=2, column=0, sticky="NW", columnspan=4, padx=(16, 0), pady=(20, 0), ipadx=10, ipady=5)
        self.button_startGame.grid(row=0, column=0, ipadx=70, ipady=20, padx=(20, 0), pady=50)


    def create_radioButtons(self):
        self.r = tk.IntVar()
        self.r.set("0")

        self.radio_2player = tk.Radiobutton(self.frame2_0, text='2', variable=self.r, value=2, command = lambda: self.ask_user(2))
        self.radio_3player = tk.Radiobutton(self.frame2_0, text='3', variable=self.r, value=3, command = lambda: self.ask_user(3))
        self.radio_4player = tk.Radiobutton(self.frame2_0, text='4', variable=self.r, value=4, command = lambda: self.ask_user(4))
        self.radio_5player = tk.Radiobutton(self.frame2_0, text='5 ', variable=self.r, value=5, command = lambda: self.ask_user(5))

        self.radio_2player.grid(row=1, column=0, sticky="NW", columnspan=1, padx=(15, 0))
        self.radio_3player.grid(row=1, column=1, sticky="NW", columnspan=1)
        self.radio_4player.grid(row=1, column=2, sticky="NW", columnspan=1)
        self.radio_5player.grid(row=1, column=3, sticky="NW", columnspan=1)


    def start_game(self, x, y, numPlayers, tally2win):
        #Check if all data is filled out
        if (len(x) == 0 or len(y) == 0 or numPlayers == 0 or tally2win == None):
            self.print_error("Start Game")
            return

        x = int(x)
        y = int(y)
        tally2win = int(tally2win)

        self.withdraw()
        game = BoardWindow(self, x, y, numPlayers, tally2win, self.playerData)


    def ask_user(self, num):

        if(self.playerNamesEntered):
            result = tk.messagebox.askquestion(message = "Are you sure you want to change player count? Selected players will be unselected.")
            if(result == 'yes'):
                self.player_window.destroy()
                self.playerNamesEntered = False
            else:
                self.r.set(self.lastRadioPressed)
                return

        self.lastRadioPressed = num
        self.set_default_data(num)


    def open_player_window(self, numPlayers):
        if(numPlayers == 0):
            self.print_error("Player Names")
            return

        self.button_setPlayer['state'] = tk.DISABLED
        self.button_startGame['state'] = tk.DISABLED

        #Prevents another player window from being opened. Makes it so data can be saved
        if(self.playerNamesEntered):
            self.player_window.deiconify()
        else:
            self.player_window = PlayerWindow(self, numPlayers)


    def print_error(self, errorType):

        top = tk.Toplevel()
        top.geometry("+700+425")
        top.resizable(height = False, width = False)

        if(errorType == "Start Game"):
            message_error = tk.Label(top, text="Please enter all required boxes if you wish to play a custom game", padx=20,
                                     pady=20)
        elif(errorType == "Player Names"):
            message_error = tk.Label(top, text = "Please enter number of players before attempting to submit player names", padx=20,
                                     pady=20)

        button_ok = tk.Button(top, text="OK", padx=20, pady=5, command=lambda: top.destroy())
        message_error.grid(row=0, column=0)
        button_ok.grid(row=1, column=0, pady=(0, 20))


    def set_default_data(self, numPlayers):

        self.playerData = {}
        imgNames = ['images/X.png', 'images/O.jpg', 'images/spade.jpg', 'images/diamond.png', 'images/club.png']

        for i in range(numPlayers):
            self.playerData["Player " + str(i + 1)] = imgNames[i]




class PlayerWindow(tk.Toplevel):

    def __init__(self, parent, numPlayers):
        tk.Toplevel.__init__(self)

        self.parent = parent
        self.numPlayers = numPlayers
        self.selectList = {}
        self.playerNamesEntered = False

        self.geometry("+650+375")
        self.resizable(height = False, width = False)
        self.protocol("WM_DELETE_WINDOW", lambda: self.close_window())

        self.frame_entry = tk.LabelFrame(self, text="Add New Player", borderwidth=4, relief='groove')
        self.frame_scoreboard = tk.Frame(self)
        self.frame_player_display = tk.LabelFrame(self, text="Selected Players", borderwidth=4, relief='groove')
        self.frame_right = tk.Frame(self)

        self.frame_scoreboard.grid(row=0, column=0, sticky='nsew', rowspan=3)
        self.frame_entry.grid(row=0, column=1, sticky='wn', padx=7, pady=(14, 0), rowspan=1, columnspan=2)
        self.frame_player_display.grid(row=1, column=1, sticky="wn", padx=7, pady=(5, 13), rowspan=1, columnspan=1)
        self.frame_right.grid(row=1, column=2, sticky="wn", rowspan=1, columnspan=1)

        self.fill_scoreboard_frame()
        self.update_records()
        self.fill_entry_frame()
        self.fill_player_frame()
        self.fill_right_frame()


    def close_window(self):

        self.parent.button_setPlayer['state'] = tk.NORMAL
        self.parent.button_startGame['state'] = tk.NORMAL

        if(self.playerNamesEntered):
            self.withdraw()
        else:
            self.destroy()


    def fill_player_frame(self):

        self.selectTree = ttk.Treeview(self.frame_player_display, height=5)
        self.selectTree.images = {}

        self.selectTree.column("#0", width=100, minwidth=20, stretch=tk.NO)
        self.selectTree.heading("#0", text="Players", anchor=tk.W)

        self.selectTree.grid(row=0, column=0, sticky='nsew')


    def fill_right_frame(self):

        self.isChecked = tk.BooleanVar()
        self.isChecked.set(False)

        self.check = tk.Checkbutton(self.frame_right, text="Use default icons", variable=self.isChecked)
        self.button_enter = tk.Button(self.frame_right, text="Enter data", padx=20, pady=15, bg='green',
                                      command=lambda: self.enter_data(copy.deepcopy(self.selectList)))

        self.check.grid(row=0, column=0, pady=(40, 20))
        self.button_enter.grid(row=1, column=0)


    def fill_scoreboard_frame(self):

        self.dbTree = ttk.Treeview(self.frame_scoreboard, selectmode='browse')
        self.dbTree["columns"] = ("one", "two", "three", "four")
        self.dbTree.column("#0", width=100, minwidth=100, stretch=tk.NO)
        self.dbTree.column("one", width=50, minwidth=10, stretch=tk.NO)
        self.dbTree.column("two", width=50, minwidth=10, stretch=tk.NO)
        self.dbTree.column("three", width=50, minwidth=10, stretch=tk.NO)
        self.dbTree.column("four", width=50, minwidth=10, stretch=tk.NO)

        self.dbTree.heading("#0", text="Username", anchor=tk.W)
        self.dbTree.heading("one", text="GP", anchor=tk.W)
        self.dbTree.heading("two", text="Wins", anchor=tk.W)
        self.dbTree.heading("three", text="Losses", anchor=tk.W)
        self.dbTree.heading("four", text="Ties", anchor=tk.W)

        self.label_message = tk.Label(self.frame_scoreboard, text="Gamer", foreground='red')
        self.button_delete = tk.Button(self.frame_scoreboard, text="Delete", padx=15,
                                       command=lambda: self.delete_player(self.dbTree.selection()))
        self.button_icon = tk.Button(self.frame_scoreboard, text="Change Icon", padx=15,
                                     command=lambda: self.change_icon(self.dbTree.selection()))
        self.button_select = tk.Button(self.frame_scoreboard, text="Select", padx=15,
                                       command=lambda: self.select_player(self.dbTree.selection()))
        self.button_remove = tk.Button(self.frame_scoreboard, text="Remove", padx=15,
                                       command=lambda: self.remove_player(self.selectTree.selection()))

        self.label_message.grid(row=0, column=0, columnspan=4, sticky='w')
        self.dbTree.grid(row=1, column=0, columnspan=4, sticky='nsew')
        self.button_delete.grid(row=2, column=0, columnspan=1, sticky='w')
        self.button_icon.grid(row=2, column=1, columnspan=1, sticky='w')
        self.button_select.grid(row=2, column=2, columnspan=1, sticky='w')
        self.button_remove.grid(row=2, column=3, columnspan=1, sticky='w')


    def fill_entry_frame(self):

        label = tk.Label(self.frame_entry, text="Username:")
        self.entry = tk.Entry(self.frame_entry)
        button_addPlayer = tk.Button(self.frame_entry, text="Add player",
                                     command=lambda: self.add_player(self.entry.get()))

        self.entry.grid(row=0, column=1)
        label.grid(row=0, column=0)
        button_addPlayer.grid(row=1, column=1)


    def delete_player(self, item):

        if (item == ()):
            self.label_message['text'] = "Please select an entry before deleting"
            return

        username = self.dbTree.item(item, "text")
        db.delete_player(username)

        self.label_message['text'] = username + " successfully deleted"
        self.update_records()


    def select_player(self, item):

        if (item == ()):
            self.label_message['text'] = "Please select an entry before hitting select"
            return

        if (len(self.selectList) == self.numPlayers):
            self.label_message['text'] = "Max amount of players selected."
            return

        username = self.dbTree.item(item, "text")
        self.dbTree.delete(item)

        self.selectList[username] = self.dbTree.imageNames[username]   #Link username and image name

        img = self.dbTree.images[username]
        self.selectTree.images[username] = img      #Store reference to image

        self.selectTree.insert('', 'end', text=username, image=img)


    def remove_player(self, item):

        if (item == ()):
            self.label_message['text'] = "Please select an entry from selected list before hitting remove"
            return

        username = self.selectTree.item(item, "text")

        self.selectList.pop(username)
        self.selectTree.delete(item)

        self.selectTree.images.pop(username)
        self.update_records()


    def add_player(self, username):

        if (len(username) == 0):
            self.label_message['text'] = "Please fill out the box before attempting to enter"
            return

        if (db.add_player(username)):
            self.label_message['text'] = username + " has been successfully added to the database"
            self.entry.delete(0, tk.END)
            self.update_records()
        else:
            self.label_message['text'] = "The name " + username + " already exists. Please enter another username"


    def enter_data(self, players):

        if (len(players) < self.numPlayers):
            self.label_message['text'] = "Please enter the correct number of players."
            return

        imgNames = ['images/X.png', 'images/O.jpg', 'images/spade.jpg', 'images/diamond.png', 'images/club.png']


        if(self.isChecked.get()):
            for i, player in enumerate(players):
                players[player] = imgNames[i]

        self.parent.playerData = players
        self.parent.playerNamesEntered = True
        self.playerNamesEntered = True

        self.parent.button_setPlayer['state'] = tk.NORMAL
        self.parent.button_startGame['state'] = tk.NORMAL

        self.withdraw()



    def change_icon(self, item):

        #Check if a user is selected
        if (item == ()):
            self.label_message['text'] = "Please select an entry before attempting to change icon"
            return

        username = self.dbTree.item(item, "text")

        cwd = os.getcwd() #Get current working directory of file

        #Open a file dialog for user to select photo
        try:
            filename = tk.filedialog.askopenfilename(initialdir= cwd + "/images",
                                                     title="Select an image",
                                                     filetypes=(("png files", "*.png"), ("jpg files", "*.jpg")))
            db.update_icon(username, filename)
            self.update_records()

            self.label_message['text'] = "Successfully changed icon"

        except(AttributeError):
            pass


    #Update player list pulled from database
    def update_records(self):

        #Delete entries from current display
        records = self.dbTree.get_children()

        for element in records:
            self.dbTree.delete(element)


        #Refill tree with updated data
        db_rows = db.get_data()
        self.dbTree.images = {}
        self.dbTree.imageNames = {}

        for row in db_rows:
            imgName = row[5]
            img = Image.open(imgName)
            img = img.resize((20, 20), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            username = row[0]

            if (not username in self.selectList):
                self.dbTree.insert('', 0, text=row[0], values=(row[1], row[2], row[3], row[4]), image=img)
                self.dbTree.images[row[0]] = img
                self.dbTree.imageNames[row[0]] = imgName




class BoardWindow(tk.Toplevel, Engine):

    def __init__(self, parent, cols, rows, numPlayers, tally2win, playerData):
        tk.Toplevel.__init__(self)

        self.scale_window()

        self.parent = parent
        self.colCount = cols
        self.rowCount = rows
        self.numPlayers = numPlayers
        self.tally2win = tally2win
        self.playerData = playerData
        self.playerList = []
        self.iconNames = []
        self.imgList = []


        items = playerData.items()
        for item in items:
            self.playerList.append(item[0])
            self.iconNames.append(item[1])

        self.buttonList = [None] * (cols*rows)
        self.engine = Engine(self, rows, cols, tally2win, numPlayers, self.playerList)

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(1, weight=12)
        self.rowconfigure(1, weight=4)

        self.boardFrame = tk.Frame(self)
        self.displayFrame = tk.Frame(self)
        self.panelList = [None] * numPlayers
        self.labelList = [None] * numPlayers
        self.buttonList = []

        self.displayFrame.grid(row=0, column=0, sticky="nsew", columnspan=1,
                              rowspan=2)  # When you create an extra column do you create an extra row?

        self.boardFrame.grid(row=0, column=1, sticky="nsew", columnspan=1, rowspan=2)

        self.load_images()
        self.create_board()
        self.create_labels()
        self.create_buttons()



    def scale_window(self):

        self.geometry("700x500+600+275")


    def load_images(self):
        for name in self.iconNames:
            img = Image.open(name)
            img = img.resize((35, 35), Image.ANTIALIAS)
            img = ImageTk.PhotoImage(img)
            self.imgList.append(img)


    def create_board(self):

        for rowIndex in range(self.rowCount):
            tk.Grid.rowconfigure(self.boardFrame, rowIndex, weight=2)
            #print("ROW INDEX", rowIndex)

            for colIndex in range(self.colCount):
                tk.Grid.columnconfigure(self.boardFrame, colIndex, weight=2)
                newButton = tk.Button(self.boardFrame)
                newButton['command'] = lambda row = rowIndex, col = colIndex, button = newButton: self.engine.updateBoard(row, col, button, self.imgList)
                newButton.grid(row=rowIndex, column=colIndex, sticky="nsew")
                self.buttonList.append(newButton)


    def create_labels(self):

        headerFont = ft.Font(size=10, weight="bold")

        label_player = tk.Label(self.displayFrame, text="Players:", font=headerFont)
        label_options = tk.Label(self.displayFrame, text="Options:", font=headerFont)

        label_player.grid(row=0, column=0, sticky="NW", pady=(0, 10), columnspan = 2)
        label_options.grid(row=(self.numPlayers + 1), column= 0, sticky="NW", pady=(20, 10), columnspan = 2)

        for i in range(self.numPlayers):
            self.panelList[i] = tk.Label(self.displayFrame, image= self.imgList[i])
            self.labelList[i] = tk.Label(self.displayFrame, text = self.playerList[i])
            self.panelList[i].grid(row=i+1, column=0, sticky="NW")
            self.labelList[i].grid(row=i+1, column=1, sticky="NW", pady = (10, 0))


    def create_buttons(self):

        button_optionWindow = tk.Button(self.displayFrame, text = "Option Window", command = lambda: self.open_input_window())
        button_restartGame = tk.Button(self.displayFrame, text = "Restart Game", command = lambda: self.restart_game())

        button_optionWindow.grid(row = (self.numPlayers + 2), column = 0, sticky = "NW", padx = 10, pady = 10, columnspan = 10)
        button_restartGame.grid(row = (self.numPlayers + 3), column = 0, sticky = "NW", padx = 10, pady = 10, columnspan = 10)


    def open_input_window(self):
        self.destroy()
        self.parent.deiconify()


    def restart_game(self):
        self.destroy()
        new_game = BoardWindow(self.parent, self.colCount, self.rowCount, self.numPlayers, self.tally2win, self.playerData)


