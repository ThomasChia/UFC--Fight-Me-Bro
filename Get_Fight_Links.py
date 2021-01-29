from bs4 import BeautifulSoup
import csv
import pandas as pd
import numpy as np
import requests

url = 'http://ufcstats.com/statistics/events/completed?page=all'

source = requests.get(url)

links = []

soup = BeautifulSoup(source.content, 'lxml')
body = soup.find('body')
table = body.find('table')
table_body = table.find('tbody')
table_rows = table_body.find_all('tr')

for row in table_rows[2:]:
    for a in row.find_all('a', href = True):
        print(a['href'])
        links.append([a['href']])

print(links)

with open('fight_links.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerows(links)

