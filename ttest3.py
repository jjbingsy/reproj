import sqlite3
from icecream import ic
IDOLSDB_PATH = r"C:\Users\Security\Documents\jsy\dat2\idolsdb.db"
# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
conn2 = sqlite3.connect(IDOLSDB_PATH)

# Create a cursor object
cur = conn.cursor()
cur2 = conn2.cursor()

rest = cur2.execute("SELECT * FROM film_idols where film_name = 'JUTA-139'").fetchall()

for r in rest:
    print (r)   