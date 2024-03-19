import sqlite3
import bs4
import re
from env.env_001 import FILMSOURCES_PATH, IDOLSDB_PATH

#check original fim_sources
# FILMSOURCES_PATH = "/home/bing/dat2/filmSources.db" #Original filmsources
# IDOLSDB_PATH = "/home/bing/dat2/idolsdb.db" # 2nd film_sources
'''
SELECT column_name
FROM (
    SELECT column_name FROM table1
    UNION ALL
    SELECT column_name FROM table2
    UNION ALL
    SELECT column_name FROM table3
) AS combined
GROUP BY column_name
HAVING COUNT(*) = 1
'''
conn_orig = sqlite3.connect(FILMSOURCES_PATH)
conn2 = sqlite3.connect(IDOLSDB_PATH)

cur_orig = conn_orig.cursor()
query_guru = "select name, url, content from filmsources where url not like '%/actress%' and url not like '%/series/%' and url not like '%jav.guru/?%' "
#query_guru = "select name, url, content from filmsources where url like '%missav.com%'"
#query_guru = "select name, url, content from filmsources where url not like '%jav.guru/?%' and url like '%jav.guru%'"
cur_orig.execute(query_guru)
guru = cur_orig.fetchall()

# Create the film_idol table
cur2 = conn_orig.cursor()
cur2.execute('drop table film_idol')
cur2.execute('''CREATE TABLE  film_idol (
                    i TEXT,
                    idol_link TEXT,
                    u TEXT,
                    idol_name TEXT,
                    PRIMARY KEY (i, idol_link)
                )''')

for i, u, c in guru:
    print(i, u)
    soup = bs4.BeautifulSoup(c, "lxml")

    if "database" in u:
        idols = soup.find_all('div', class_='idol-thumb')
        for idol in idols:
            idol_name = None
            idol_link = None

            idolsp = idol.previous_sibling
            idol_name = idolsp.find('a').text
            idol_link = idol.find('a')['href']
            if idol_name:
                print(idol_name, idol_link)
                # Insert the data into the film_idol table
                cur2.execute("INSERT or ignore INTO film_idol (i, idol_link, u, idol_name) VALUES (?, ?, ?, ?)",
                             (str(i), str(idol_link), str(u), str(idol_name)))
    elif "missav" in u:
        idols = soup.find_all('a', {'href': re.compile(f"/actresses/")}, class_="text-nord13 font-medium")
        for idol in idols:
            idol_name = None
            idol_link = None
            idol_name = idol.string
            idol_link = idol["href"]
            if idol_name:
                print(idol_name, idol_link)
                # Insert the data into the film_idol table
                cur2.execute("INSERT or ignore INTO film_idol (i, idol_link, u, idol_name) VALUES (?, ?, ?, ?)",
                             (str(i), str(idol_link), str(u), str(idol_name)))
    else:
        idols = soup.find("div", class_="infoleft").select('a[href*="jav.guru/actress/"]')
        for idol in idols:
            idol_name = None
            idol_link = None
            idol_link = idol['href']
            idol_name = idol.string.strip()
            if idol_name:

                if i and idol_link and idol_name and  u:
                    # Insert the data into the film_idol table
                    print(i, idol_link, idol_name, u)
                    cur2.execute("INSERT or ignore INTO film_idol (i, idol_link, u, idol_name) VALUES (?, ?, ?, ?)",
                             (str(i), str(idol_link), str(u), str(idol_name)))

conn_orig.commit()
conn_orig.close()
# Commit the changes and close the connections
conn2.commit()

conn2.close()
