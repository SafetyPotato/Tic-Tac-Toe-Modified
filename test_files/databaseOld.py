import sqlite3
import time
import datetime
import random


class Database:

    def __init__(self):

        self.conn = sqlite3.connect('player.db')
        self.c = self.conn.cursor()


        self.create_table()






    def create_table(self):

        self.conn.execute("""CREATE TABLE IF NOT EXISTS playerData(
                    username text,
                    gamesPlayed text,
                    wins integer,
                    losses integer,
                    ties integer)
                    """)


    def check_player(self):
        pass
    def update_score(self, players):  #dictionary
        pass


    def add_players(self, usernames):

        for name in usernames:

            if(not self.check_player_exists(name)):
                self.c.execute("INSERT INTO playerData (username, gamesPlayed, wins, losses, ties) VALUES (?, ?, ?, ?, ?)",
                               (name, 0, 0, 0, 0))
            else:
                return False

        self.conn.commit()


    def check_player_exists(self, username):
        self.c.execute("SELECT username FROM playerData WHERE username=:username", {'username': username}) #cursor is populated

        name = self.c.fetchone()

        if name:
            return True
        else:
            return False

    def print_table(self):
        self.c.execute("SELECT * FROM playerData")
        print(self.c.fetchall())


    def remove_player(self, username):
        self.c.execute("DELETE FROM playerData WHERE username=:username", {'username': username})
        self.conn.commit()



app = Database()

app.add_players(["Tom"])

app.remove_player("James")

#print(app.check_player_exists("Bill"))




#app.print_table()



