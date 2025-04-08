from urllib.request import urlopen
import json
from collections import defaultdict
import mysql.connector
from tqdm import tqdm
import json
from time import time
import ipinfo
import matplotlib.pyplot as plt


# Enter ipinfo access token
IPINFO_ACCESS_TOKEN = "<ACCESSTOKEN>"
# Enter data to production database
HOST = "<HOST>"
USER = "<USER>"
PASSWORD = "<PASSWORD>"
DATABASE = "<DATABASE>"

def get_mysql_connection():
    return mysql.connector.connect(
        host=HOST,
        user=USER,
        password=PASSWORD,
        database=DATABASE
    )

def fetch_all(query: str, params = None, dictionary=True) -> dict:
    conn = get_mysql_connection()
    cursor = conn.cursor(dictionary=dictionary)
    cursor.execute(query, params)
    result = cursor.fetchall()
    conn.commit()
    cursor.close()
    conn.close()
    return result

def count_country(addr, countries):
    url = 'https://ipinfo.io/' + addr + '/json'
    res = urlopen(url)
    data = json.load(res)
    countries[data["country"]] += 1


handler = ipinfo.getHandler(IPINFO_ACCESS_TOKEN)

countries = defaultdict(int)
ips = fetch_all("""SELECT DISTINCT(`userId`), ip FROM sessions WHERE starttime <= '2025-03-14 13:30:00'""", dictionary=False)

for address in tqdm(ips, desc="Counting countries"):
    details = handler.getDetails(address[1])
    countries[details.country] += 1

with open("data/counted_countries_distinct_by_user_id.json", "w+") as json_file:
    json.dump(countries, json_file)

