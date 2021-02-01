import mysql.connector
from datetime import datetime


db = mysql.connector.connect(
    host = "localhost",
    user = "Tom",
    passwd = "gamer",
    database = "testdatabase"
)

mycursor = db.cursor()

#mycursor.execute("CREATE TABLE Person (name VARCHAR(50), age smallint UNSIGNED, personID int PRIMARY KEY AUTO_INCREMENT)")

#mycursor.execute("DESCRIBE Person")
#mycursor.execute("INSERT INTO Person (name, age) VALUES (%s, %s)", ("Joe", 22))
#db.commit()

#mycursor.execute("SELECT * FROM Person")

#mycursor.execute("CREATE TABLE Test(name varchar(50), created datetime NOT NULL, "
                # "gender ENUM('M', 'F', 'O') NOT NULL, id int PRIMARY KEY NOT NULL AUTO_INCREMENT)")

#mycursor.execute("INSERT INTO Test(name, created, gender) VALUES (%s,%s,%s)", ("Sally", datetime.now(), "F"))
#db.commit()

#mycursor.execute("SELECT name FROM Test WHERE gender = 'F' ORDER BY id DESC")

#mycursor.execute("ALTER TABLE Test ADD COLUMN food VARCHAR(50) NOT NULL")
#mycursor.execute("DESCRIBE Test")


#print(mycursor.fetchone())

#mycursor.execute("ALTER TABLE Test DROP food")
#mycursor.execute("ALTER TABLE Test CHANGE name first_name VARCHAR(50)")

for x in mycursor:
    print(x)






#mycursor.execute("CREATE DATABASE testdatabase")


