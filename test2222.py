import sqlite3
from icecream import ic
from env.env_001 import FILMSOURCES_PATH, IDOLSDB_PATH
IDOL_ID = 0

def get_idol_id():
    global IDOL_ID
    IDOL_ID += 1
    return IDOL_ID



# Connect to an in-memory SQLite database
conn = sqlite3.connect(':memory:')
conn2 = sqlite3.connect(FILMSOURCES_PATH)

# Create a cursor object
cur = conn.cursor()
cur2 = conn2.cursor()

rest = cur2.execute("SELECT film_name, idol_link, idol_name FROM film_idols").fetchall()

# Execute SQL commands to create a table
cur.execute("""
    CREATE TABLE film_idols (
        film_name TEXT,
        idol_link TEXT,
        idol_name TEXT,
        PRIMARY KEY (film_name, idol_link)
    )
""")

cur.execute("""
    CREATE TABLE idols (
        idol_ID INTEGER,
        idol_link TEXT,
        PRIMARY KEY (idol_ID, idol_link)
    )
""")




# Insert data into the table
cur.executemany("INSERT INTO film_idols VALUES (?, ?, ?)", rest)
# Commit the changes
conn.commit()

cur.execute ('select count(*) from film_idols')
print ("initial film_idols count:", cur.fetchone()[0])






# Select film_name with count > 8
cur.execute("""
    delete from film_idols where film_name in
            (SELECT film_name
    FROM film_idols
    GROUP BY film_name
    HAVING COUNT(*) > 9)
            
""")

conn.commit()

cur.execute ('''
            select f1.idol_link, f2.idol_link, f3.idol_link
            from film_idols f1 
                join film_idols f2 on f1.film_name = f2.film_name
                join film_idols f3 on f1.film_name = f3.film_name
            where f1.idol_link like '%jav.guru%' and f2.idol_link like '%missav.com%' and f3.idol_link like '%javdatabase.com%'
            group by f1.idol_link, f2.idol_link, f3.idol_link
            having count(*) > 3

             
             ''')

for idol_1, idol_2, idol_3 in cur.fetchall():
    cur.execute('select idol_ID from idols where idol_link = ? or idol_link = ? or idol_link = ?', (idol_1, idol_2, idol_3))
    #print ('must be null', cur.fetchone())
    old_idol_id = cur.fetchone()
    OO = -1
    if old_idol_id:
        oo = old_idol_id[0]
        cur.execute('insert or replace into idols values (?, ?)', (oo, idol_1))
        cur.execute('insert or replace into idols values (?, ?)', (oo, idol_2))
        cur.execute('insert or replace into idols values (?, ?)', (oo, idol_3))
    else:
        new_idol_id = get_idol_id()
        oo = new_idol_id
        cur.execute('insert into idols values (?, ?)', (new_idol_id, idol_1))
        cur.execute('insert into idols values (?, ?)', (new_idol_id, idol_2))
        cur.execute('insert into idols values (?, ?)', (new_idol_id, idol_3))
    conn.commit()

    # cur.execute ('''
    #         select f1.film_name
    #         from film_idols f1 
    #             join film_idols f2 on f1.film_name = f2.film_name
    #             join film_idols f3 on f1.film_name = f3.film_name
    #         where f1.idol_link = ? and f2.idol_link = ? and  f3.idol_link = ?
    #         group by f1.film_name
    #          ''', (idol_1, idol_2, idol_3))
    # r = cur.fetchall()

    cur.execute ('''
            select f1.film_name
            from film_idols f1 
                join film_idols f2 on f1.film_name = f2.film_name
                join film_idols f3 on f1.film_name = f3.film_name
            where (f1.idol_link = ? and f2.idol_link = ? and  f3.idol_link = ?) or
            (f1.idol_link = ? and f2.idol_link = ?) or
            (f1.idol_link = ? and f3.idol_link = ?) or
            (f2.idol_link = ? and f3.idol_link = ?)
            group by f1.film_name
             ''', (idol_1, idol_2, idol_3, idol_1, idol_2, idol_1, idol_3, idol_2, idol_3))
    r2 = cur.fetchall()
    #print (idol_1, len(r), len(r2))
    for film in r2:
        ############################################
        #TO DO: CREATE A TABLE THAT ASSOCIATES FILM WITH IDOL_ID
        ############################################
        cur.execute('delete from film_idols where film_name = ? and idol_link = ?', (film[0],idol_1))
        cur.execute('delete from film_idols where film_name = ? and idol_link = ?', (film[0],idol_2))
        cur.execute('delete from film_idols where film_name = ? and idol_link = ?', (film[0],idol_3))
conn.commit()
cur.execute ('select count(*) from film_idols')
print ("after film_idols count:", cur.fetchone()[0])

cur.execute ('select film_name, idol_link from film_idols where idol_link in (select idol_link from idols) order by film_name')
s = cur.fetchall()
print (len(s))
for fn, il in s:
    cur.execute('delete from film_idols where film_name = ? and idol_link = ?', (fn,il))
conn.commit()

# cur.execute ('select count(*) from film_idols')
# print ("final film_idols count:", cur.fetchone()[0])
# fi = cur.execute ('select * from film_idols')

cur.execute ('''
            select f1.idol_link, f2.idol_link, f3.idol_link, count(*)
            from film_idols f1 
                join film_idols f2 on f1.film_name = f2.film_name
                join film_idols f3 on f1.film_name = f3.film_name
            where f1.idol_link like '%jav.guru%' and f2.idol_link like '%missav.com%' and f3.idol_link like '%javdatabase.com%'
            group by f1.idol_link, f2.idol_link, f3.idol_link

             
             ''')
with (open('myfile1121.txt', 'w')) as f:
    for idol_1, idol_2, idol_3, ii in cur.fetchall():
        cur.execute('select count(*) from film_idols where idol_link = ?', (idol_1,))
        c1 = cur.fetchone()[0]
        cur.execute('select count(*) from film_idols where idol_link = ?', (idol_2,))
        c2 = cur.fetchone()[0]
        cur.execute('select count(*) from film_idols where idol_link = ?', (idol_3,))
        c3 = cur.fetchone()[0]
        if ii == c1 and ii == c2 and ii == c3:
            print (idol_1, idol_2, idol_3, ii, c1, c2, c3)
            f.write(idol_1 +" " + idol_2 +" "+ idol_3 +" "+ str(ii) + '\n')
        else:
            pass #print (idol_1, idol_2, idol_3, ii, c1, c2, c3)
# cur.execute ('select * from idols order by idol_ID')
# for row in cur.fetchall():
#     print (row)


# films_to_delete = cur.fetchall()
# print ("first delete: ", len(films_to_delete))
# # Delete the films from the table
# for film in films_to_delete:
#     cur.execute("""
#         DELETE FROM film_idols
#         WHERE film_name = ?
#     """, (film[0],))

# # Commit the changes
# conn.commit()



# # Select pairs with count > 12
# cur.execute("""
# select f1.idol_link, f2.idol_link , count(*) from film_idols f1 join film_idols f2 on f1.film_name = f2.film_name
#    where (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%') or
#    (f1.idol_link like '%missav%' and f2.idol_link like '%database%')
#    group by f1.idol_link, f2.idol_link having count(*) > 3 order by count(*);
# """)
# '''
# select  distinct f1.idol_link, f2.idol_link , count(*) from film_idols f1 join film_idols f2 on f1.film_name = f2.film_name
#    where (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%') or
#    (f1.idol_link like '%missav%' and f2.idol_link like '%database%')
#    group by f1.idol_link, f2.idol_link having count(*) > 3 order by count(*);
# '''




# pairs_to_delete = cur.fetchall()
# print ("second delete: ", len(pairs_to_delete))


# with open('myfile44.txt', 'w') as f:
#     # Loop through the list
#       # Write each line to the file
#     for pair in pairs_to_delete:
#         print (pair[0], pair[1], pair[2])
#         f.write(pair[0] + pair[1] + str(pair[2]) + '\n')

#         cur.execute("""
#             DELETE FROM film_idols
#             WHERE  idol_link = ? or idol_link = ?
        
#     """, (pair[0], pair[1]))
    

# conn.commit()



# # Select data from the table
# cur.execute('''
#               SELECT f1.idol_link, f2.idol_link, COUNT(*)
#     FROM film_idols f1
#     JOIN film_idols f2 ON f1.film_name = f2.film_name
#     WHERE 
#     (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%') or
#     (f1.idol_link not like '%jav.guru%' and f2.idol_link like '%jav.guru%') or
#     (f1.idol_link not like '%missav.com%' and f2.idol_link like '%missav.com%') or
#     (f1.idol_link like '%missav.com%' and f2.idol_link not like '%missav.com%')
#     GROUP BY f1.idol_link, f2.idol_link
#     HAVING COUNT(*) > 1
#     order by COUNT(*) desc;
#             ''')
# pairs_to_delete = cur.fetchall()
# print ("third delete: ", len(pairs_to_delete))

# for pair in pairs_to_delete:
#     cur.execute("""
#         DELETE FROM film_idols
#         WHERE  idol_link = ? or idol_link = ?
        
#     """, (pair[0], pair[1]))
    

# conn.commit()

# cur.execute(''' 
#               SELECT f1.idol_link, f2.idol_link, COUNT(*)
#     FROM film_idols f1
#     JOIN film_idols f2 ON f1.film_name = f2.film_name
#     WHERE 
#     (f1.idol_link like '%jav.guru%' and f2.idol_link not like '%jav.guru%') or
#     (f1.idol_link not like '%jav.guru%' and f2.idol_link like '%jav.guru%') or
#     (f1.idol_link not like '%missav.com%' and f2.idol_link like '%missav.com%') or
#     (f1.idol_link like '%missav.com%' and f2.idol_link not like '%missav.com%')
#     GROUP BY f1.idol_link, f2.idol_link
#             ''')

# pairs_to_delete = cur.fetchall()
# for pair in pairs_to_delete:
#     cur.execute("""
#         DELETE FROM film_idols
#         WHERE  idol_link = ? or idol_link = ?
        
#     """, (pair[0], pair[1]))
    

# conn.commit()

# cur.execute(''' 
# select * from film_idols ;
#             ''')





# rows = cur.fetchall()
# # Print the rows

# # Open the file in write mode
# with open('myfile11.txt', 'w') as f:
#     # Loop through the list
#     for line in rows:
#         # Write each line to the file
#         f.write(line[0] + line[1] + '\n')
#         #print(line)








# # Close the connection
# conn.close()