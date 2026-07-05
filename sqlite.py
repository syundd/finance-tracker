import sqlite3

db=sqlite3.connect("finance.db")
#Create cursor
c = db.cursor()
#Can do commands
#c.execute("""CREATE TABLE finance (
#   title text,
#   price integer,
#   total integer,
#   remain integer
#)""")

c.execute("INSERT INTO finance VAlUES()")
#Update db
db.commit()

db.close()