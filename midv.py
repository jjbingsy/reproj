import sqlite3
from icecream import ic
import bs4
import re


IDOLSDB_PATH = "/home/bing/dat2/filmSources.db" #Original filmsources
# Connect to an in-memory SQLite database
conn2 = sqlite3.connect(':memory:')
conn = sqlite3.connect(IDOLSDB_PATH)

# Create a cursor object
cur = conn.cursor()
# cur2 = conn2.cursor()

i = cur.execute("SELECT NAME, URL, content FROM filmsources where name like 'MIDV%' AND URL LIKE '%database%' order by name;").fetchall()

for name, url, content in i:
    print(name, url)
    soup = bs4.BeautifulSoup(content, "lxml")
    # idols = soup.find_all('a', {'href': re.compile(f"/actresses/")}, class_="text-nord13 font-medium")

    # for idol in idols:
    #     idol_name = None
    #     idol_link = None
    #     idol_name = idol.string
    #     idol_link = idol["href"]
    #     if idol_name:
    #         print(idol_name, idol_link)


    idols =  soup.find_all('div', class_='idol-thumb')
    for idol in idols:
        idolsp = idol.previous_sibling
        idol_name = idolsp.find('a').text
        idol_link = idol.find('a')['href']        
        if idol_name:
            print(idol_name, idol_link)
            # Insert the data into the film_idol table
            # cur.execute("INSERT or ignore INTO film_idol (i, idol_link, u, idol_name) VALUES (?, ?, ?, ?)",
            #              (str(name), str(idol_link), str(url), str(idol_name)))