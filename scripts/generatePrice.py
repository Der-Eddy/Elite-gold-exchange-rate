import re
import json
import datetime
from statistics import median
import psycopg2 as pg
from config import __version__, databaseCred, cookieJar, userAgent, jsonSavePath

jsonData = {}

con = pg.connect(
    host=databaseCred['host'], 
    dbname=databaseCred['dbname'],
    user=databaseCred['dbuser'], 
    password=databaseCred['dbpassword'])
cur = con.cursor()

cur.execute("SELECT * FROM treasures WHERE (title LIKE '%PSC%' OR title LIKE '%psc%' OR title LIKE '%Psc%' OR title LIKE '%Paysafecard%' OR title LIKE '%paysafecard%') AND timestamp > NOW() - INTERVAL '30 days'")
priceList = []
soldPriceList = []
parsedList = []
queryResult = cur.fetchall()
jsonData['treasureCount'] = len(queryResult)
for entry in queryResult:
    id = int(entry[0])
    sellerid = int(entry[1])
    seller = bytes(entry[2]).decode('ISO-8859-1')
    cost = int(entry[3])
    timestamp = entry[4].timestamp()
    title = bytes(entry[5]).decode('ISO-8859-1')
    try:
        buyer = bytes(entry[7]).decode('ISO-8859-1')
        buyerid = int(entry[8])
    except TypeError:
        buyer = None 
        buyerid = None
    regex = r'(10|20|25|50|100)'
    if 'junior' in title.lower():
        continue
        # Junior Paysafecard are often sold for a lower price and will skew with the price rate
    titleMatch = re.search(regex, title)
    try:
        euro = int(titleMatch.group(1))
    except AttributeError:
        continue
    exchangePrice = cost / euro
    priceList.append(exchangePrice)
    if buyer != None:
        soldPriceList.append(exchangePrice)
    parsedList.append({'id': id, 'sellerid': sellerid, 'sellername': seller, 'cost': cost, 'timestamp': timestamp, 'title': title, 'buyerid': buyerid, 'buyername': buyer, 'ratio': exchangePrice})
    #print(f'{id} - {title} - {cost} - {euro}')
    #print(exchangePrice)

jsonData['median'] = median(priceList)
jsonData['medianSold'] = median(soldPriceList)
jsonData['treasureList'] = parsedList
cur.execute("SELECT COUNT(id) FROM treasures")
jsonData['rows'] = int(cur.fetchone()[0])
jsonData['lastUpdated'] = datetime.datetime.now().timestamp()

with open(jsonSavePath, 'w') as file:
    json.dump(jsonData, file)

cur.close()
con.close()