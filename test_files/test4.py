import sqlite3

conn = sqlite3.connect('players.db')

c = conn.cursor()

#c.execute(""" CREATE TABLE playerData (
#            id integer,
#            username text,
#            wins integer)
#        """)

c.execute("INSERT INTO playerData VALUES('1', 'Bill', '3')")

#c.execute("SELECT * FROM employees WHERE wins = '3'")

#c.fetchall()
print(c.fetchone())


conn.commit()

conn.close