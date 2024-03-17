import sqlite3
from icecream import ic
IDOLSDB_PATH = r"C:\Users\Security\Documents\jsy\dat2\idolsdb.db"
# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
conn2 = sqlite3.connect(IDOLSDB_PATH)

# Create a cursor object
cur = conn.cursor()
cur2 = conn2.cursor()

rest = cur2.execute("SELECT * FROM film_idols").fetchall()

# Execute SQL commands to create a table
cur.execute("""
    CREATE TABLE film_idols (
        film_name TEXT,
        idol_link TEXT,
        PRIMARY KEY (film_name, idol_link)
    )
""")





# Insert data into the table
for r in rest:
    cur.execute("INSERT INTO film_idols (film_name, idol_link) VALUES (?, ?)", r)


# Select film_name with count > 8
cur.execute("""
    SELECT film_name
    FROM film_idols
    GROUP BY film_name
    HAVING COUNT(*) > 7
""")
films_to_delete = cur.fetchall()
print ("first delete: ", len(films_to_delete))
# Delete the films from the table
for film in films_to_delete:
    cur.execute("""
        DELETE FROM film_idols
        WHERE film_name = ?
    """, (film[0],))

# Commit the changes
conn.commit()



# Select pairs with count > 12
cur.execute("""
    SELECT f1.idol_link, f2.idol_link, COUNT(*)
    FROM film_idols f1
    JOIN film_idols f2 ON f1.film_name = f2.film_name
    WHERE 
    (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%' and f1.idol_link != f2.idol_link) or
    (f1.idol_link not like '%jav.guru%' and f2.idol_link like '%jav.guru%' and f1.idol_link != f2.idol_link) or
    (f1.idol_link not like '%missav.com%' and f2.idol_link like '%missav.com%' and f1.idol_link != f2.idol_link) or
    (f1.idol_link like '%missav.com%' and f2.idol_link not like '%missav.com%' and f1.idol_link != f2.idol_link)
    GROUP BY f1.idol_link, f2.idol_link
    HAVING COUNT(*) > 3;
""")

pairs_to_delete = cur.fetchall()
print ("second delete: ", len(pairs_to_delete))

for pair in pairs_to_delete:
    cur.execute("""
        DELETE FROM film_idols
        WHERE  idol_link = ? or idol_link = ?
        
    """, (pair[0], pair[1]))
    

conn.commit()



# Select data from the table
cur.execute('''
              SELECT f1.idol_link, f2.idol_link, COUNT(*)
    FROM film_idols f1
    JOIN film_idols f2 ON f1.film_name = f2.film_name
    WHERE 
    (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%') or
    (f1.idol_link not like '%jav.guru%' and f2.idol_link like '%jav.guru%') or
    (f1.idol_link not like '%missav.com%' and f2.idol_link like '%missav.com%') or
    (f1.idol_link like '%missav.com%' and f2.idol_link not like '%missav.com%')
    GROUP BY f1.idol_link, f2.idol_link
    HAVING COUNT(*) > 1
    order by COUNT(*) desc;
            ''')
pairs_to_delete = cur.fetchall()
print ("third delete: ", len(pairs_to_delete))

for pair in pairs_to_delete:
    cur.execute("""
        DELETE FROM film_idols
        WHERE  idol_link = ? or idol_link = ?
        
    """, (pair[0], pair[1]))
    

conn.commit()

cur.execute(''' 
              SELECT f1.idol_link, f2.idol_link, COUNT(*)
    FROM film_idols f1
    JOIN film_idols f2 ON f1.film_name = f2.film_name
    WHERE 
    (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%') or
    (f1.idol_link not like '%jav.guru%' and f2.idol_link like '%jav.guru%') or
    (f1.idol_link not like '%missav.com%' and f2.idol_link like '%missav.com%') or
    (f1.idol_link like '%missav.com%' and f2.idol_link not like '%missav.com%')
    GROUP BY f1.idol_link, f2.idol_link
            ''')

pairs_to_delete = cur.fetchall()
for pair in pairs_to_delete:
    cur.execute("""
        DELETE FROM film_idols
        WHERE  idol_link = ? or idol_link = ?
        
    """, (pair[0], pair[1]))
    

conn.commit()

cur.execute(''' 
select * from film_idols ;
            ''')





rows = cur.fetchall()
# Print the rows

# Open the file in write mode
with open('myfile2.txt', 'w') as f:
    # Loop through the list
    for line in rows:
        # Write each line to the file
        f.write(line[0] + '\n')
        print(line)








# Close the connection
conn.close()