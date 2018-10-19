import re
from statistics import median
import psycopg2 as pg
from config import __version__, databaseCred, cookieJar, userAgent


con = pg.connect(
    host=databaseCred['host'], 
    dbname=databaseCred['dbname'],
    user=databaseCred['dbuser'], 
    password=databaseCred['dbpassword'])
cur = con.cursor()

cur.execute("SELECT * FROM treasures WHERE (title LIKE '%PSC%' OR title LIKE '%psc%' OR title LIKE '%Paysafecard%' OR title LIKE '%paysafecard%') AND timestamp > NOW() - INTERVAL '7 days'")
priceList = []
for entry in cur.fetchall():
    id = int(entry[0])
    title = bytes(entry[5])
    cost = int(entry[3])
    regex = b'(10|20|25|50|100)'
    if b'junior' in title.lower():
        continue
        # Junior Paysafecard are often sold for a lower price and will skew with the price rate
    titleMatch = re.search(regex, title)
    try:
        euro = int(titleMatch.group(1))
    except AttributeError:
        continue
    exchangePrice = cost / euro
    priceList.append(exchangePrice)
    #print(f'{id} - {title} - {cost} - {euro}')
    #print(exchangePrice)

print(median(priceList))

cur.close()
con.close()