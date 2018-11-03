import re
import datetime
import requests
import psycopg2 as pg
from config import __version__, databaseCred, cookieJar, userAgent

url = 'https://www.elitepvpers.com/theblackmarket/treasure/'

con = pg.connect(
    host=databaseCred['host'], 
    dbname=databaseCred['dbname'],
    user=databaseCred['dbuser'], 
    password=databaseCred['dbpassword'])
cur = con.cursor()

class TreasureNotFound(Exception):
    def __init__(self, code):
        self.code = code
    def __str__(self):
        return repr(f'Treasure deleted/not found - Error {self.code}')

def parseTreasure(id):
    r = requests.get(url + str(id), cookies = cookieJar, headers = userAgent)

    reTitle = b"<td>Title:</td>\n<td>(.*?)</td>"
    titleMatch = re.search(reTitle, r.content, re.MULTILINE)
    try:
        title = titleMatch.group(1)
    except AttributeError:
        raise TreasureNotFound(1)

    reCost = b"<td>Cost:</td>\n<td>(\d+) eg</td>"
    costMatch = re.search(reCost, r.content, re.MULTILINE)
    try:
        cost = costMatch.group(1).decode('ISO-8859-1')
    except AttributeError:
        raise TreasureNotFound(2)

    reAuthor = b"<td>Seller:</td>\n<td><a href=\"https://www\.elitepvpers\.com/theblackmarket/profile/(\d+)\">(.*?)</a></td>\n</tr>"
    authorMatch = re.search(reAuthor, r.content, re.MULTILINE)
    try:
        seller = authorMatch.group(2)
        sellerid = authorMatch.group(1).decode('ISO-8859-1')
    except AttributeError:
        raise TreasureNotFound(3)

    reBuyer = b"<td>Buyer:</td>\n<td><a href=\"https://www\.elitepvpers\.com/theblackmarket/profile/(\d+)\">(.*?)</a></td>\n</tr>"
    buyerMatch = re.search(reBuyer, r.content, re.MULTILINE)
    try:
        buyer = buyerMatch.group(2)
        buyerid = int(buyerMatch.group(1).decode('ISO-8859-1'))
    except AttributeError:
        buyer = None
        buyerid = None

    reDate = b"<td>Creation date:</td>\n<td>\n(.*?)\n</td>"
    dateMatch = re.search(reDate, r.content, re.MULTILINE)
    try:
        date = datetime.datetime.strptime(dateMatch.group(1).decode('ISO-8859-1'), '%b %d, %Y - %H:%M')
    except AttributeError:
        raise TreasureNotFound(5)

    # reEuro = b"(\d+)\s*\x80"
    # euro = re.search(reEuro, matches.group(1))
    # print(euro.group(1))

    return (title, int(cost), seller, int(sellerid), buyer, buyerid, date)

if __name__ == '__main__':
    try:
        # Getting latest valid treasure id
        cur.execute('SELECT id FROM treasures WHERE cost IS NOT NULL ORDER BY id DESC LIMIT 1;')
        firstTreasure = cur.fetchone()[0] - 100 # Check the latest 100 treasures for updates
        lastTreasure = firstTreasure + 200 # To up to 100 possible new treasures
    except TypeError:
        # In case the database is empty, run at init scraping mode
        firstTreasure = 1
        lastTreasure = 351909 # Latest treasure as of 16.10.2018


    for id in range(firstTreasure, lastTreasure):
        try:
            title, cost, seller, sellerid, buyer, buyerid, date = parseTreasure(id)
            print(f'----- Treasure #{id} -----')
            print(f'{title} - {cost} e*g - {seller}')
            cur.execute('INSERT INTO treasures (id, sellerid, seller, buyerid, buyer, cost, timestamp, title, last_updated) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ON CONFLICT (id) DO UPDATE SET (buyerid, buyer, last_updated) = (excluded.buyerid, excluded.buyer, excluded.last_updated);',
                        (id, sellerid, seller, buyerid, buyer, cost, date, title, datetime.datetime.now()))
        except TreasureNotFound:
            print(f'!!!!! Deleted Treasure #{id} !!!!!')
            cur.execute('INSERT INTO treasures (id, title, last_updated) VALUES (%s, %s, %s) ON CONFLICT (id) DO UPDATE SET last_updated = excluded.last_updated;',
                        (id, 'Deleted' , datetime.datetime.now()))
        finally:
            con.commit()

    # Cleanup non-valid treasures after the last valid one
    cur.execute('SELECT id FROM treasures WHERE cost IS NOT NULL ORDER BY id DESC LIMIT 1;')
    lastTreasure = cur.fetchone()[0]
    cur.execute('DELETE FROM treasures WHERE id > %s;', (lastTreasure,))
    con.commit()

    cur.close()
    con.close()
