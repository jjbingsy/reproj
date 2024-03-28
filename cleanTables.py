import sqlite3
import bs4
import re
from env.env_001 import FILMSOURCES_PATH

conn = sqlite3.connect(FILMSOURCES_PATH)
cr = conn.cursor()
cr.execute('drop table film_idols')
cr.execute('''CREATE TABLE  film_idols (
                    film_name TEXT,
                    idol_link TEXT,
                    url_source TEXT,
                    idol_name TEXT,
                    PRIMARY KEY (film_name, idol_link)
                )''')

# cr.execute ('select * from idols')
# idols = cr.fetchall()
# for idol in idols:
#     print(idol)
