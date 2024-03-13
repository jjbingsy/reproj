import sqlite3
import bs4

#check original fim_sources
FILMSOURCES_PATH = "/home/bing/dat2/filmSources.db" #Original filmsources
IDOLSDB_PATH = "/home/bing/dat2/idolsdb.db" # 2nd film_sources

conn_orig = sqlite3.connect(FILMSOURCES_PATH)
conn2 = sqlite3.connect(IDOLSDB_PATH)

cur_orig = conn_orig.cursor()
'''
query_guru = "select name, url, content from filmsources where url like '%javdatabase.com%'"
query_guru = "select name, url, content from filmsources where url like '%missav.com%'"
query_guru = "select name, url, content from filmsources where url not like '%jav.guru/?%' and url like '%jav.guru%'"
cur_orig.execute(query_guru)
guru = cur_orig.fetchall()

for i, u, c in guru:
    #print (i, u)        #print(soup.prettify())
    soup = bs4.BeautifulSoup(c, "lxml")
    idols = soup.find("div", class_="infoleft").select('a[href*="jav.guru/actress/"]')
    for idol in idols:
        #print(idol['href']) 
        pass
    series = soup.find("div", class_="infoleft").select('a[href*="jav.guru/series/"]')
    for series_spec in series:
        print (i, u)
        print (series_spec.string.strip(), series_spec["href"])
        #series_link = i["href"]
    header1 = soup.find('link', rel='canonical')
    if not header1:
        raise ValueError("Corrupt data: No canonical link found.")

    film_link = header1['href']
    description = soup.title.string
    iimage = None
    img = soup.find('div', class_="large-screenimg")
    if not img or not img.img:
        raise ValueError("Corrupt data: No image source found.")
    #name = parseTitle(description)
    iimage = img.img['src']
    print (film_link, description, iimage)

'''
query_guru = "select name, url, content from filmsources where url like '%javdatabase.com%'"
query_guru = "select name, url, content from filmsources where url like '%missav.com%' "
query_guru = "select name, url, content from filmsources where url like '%missav.com%' "
query_guru = "select name, url, content from filmsources where url like '%missav.com%' and url not like '%/actress%' and url not like '%/series/%' ;"
cur_orig.execute(query_guru)
guru = cur_orig.fetchall()
for i, u, c in guru:
    print (i, u)        #print(soup.prettify())
    soup = bs4.BeautifulSoup(c, "lxml")
