import sqlite3
import tkinter as tk
from PIL import ImageTk, Image

conn = sqlite3.connect('player.db')
c = conn.cursor()

def create_table():

    conn.execute("""CREATE TABLE IF NOT EXISTS playerData(
                username text,
                gamesPlayed text,
                wins integer,
                losses integer,
                ties integer,
                icon text)
                """)

def check_player():
    pass




def update_score(usernames, winner):  #dictionary

    if(winner == 'None'):

        for name in usernames:
            c.execute('''UPDATE playerData SET ties = ties+1, gamesPlayed = gamesPlayed+1 WHERE username = ?''', (name,))
    else:

        c.execute('''UPDATE playerData SET gamesPlayed = gamesPlayed+1, wins = wins+1 WHERE username = ?''', (winner,))

        for name in usernames:
            if(name != winner):
                c.execute('''UPDATE playerData SET gamesPlayed = gamesPlayed+1, losses = losses+1 WHERE username = ?''',
                          (name,))

    conn.commit()


def add_player(username):


    if(not check_player_exists(username)):
        c.execute("INSERT INTO playerData (username, gamesPlayed, wins, losses, ties, icon) VALUES (?, ?, ?, ?, ?, ?)",
                           (username, 0, 0, 0, 0, 'images/default.png'))
        conn.commit()
        return True
    else:
        return False

def delete_player(username):
    c.execute('''DELETE FROM playerData WHERE username = ?''', (username,))
    conn.commit()

def check_player_exists(username):
    c.execute("SELECT username FROM playerData WHERE username=:username", {'username': username}) #cursor is populated

    name = c.fetchone()

    if name:
        return True
    else:
        return False

def update_icon(username, filename):
    c.execute('''UPDATE playerData SET icon = ? WHERE username = ?''', (filename, username,))
    conn.commit()


def get_player(username):
    c.execute("SELECT username FROM playerData WHERE username=:username", {'username': username})
    conn.commit()

def get_data():
    c.execute("SELECT * FROM playerData ORDER BY username DESC")
    return c.fetchall()


def remove_player(username):
    c.execute("DELETE FROM playerData WHERE username=:username", {'username': username})
    conn.commit()





#add_players(["gamerMan"])
#print(check_player_exists("gamerMan"))

create_table()

#print(app.check_player_exists("Bill"))

list = ['Tommy', 'Nook', 'Timmy', 'Tom']





#update_score(list, 0)




#app.print_table()



