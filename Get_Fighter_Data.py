from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import string

url = 'http://ufcstats.com/statistics/fighters?char={}&page=all'

### Get Headers ###

source = requests.get(url.format('a'))

soup = BeautifulSoup(source.content, 'lxml')
body = soup.find('body')
table = body.find('table')
headers = table.find_all('th')

headers_list = []

for header in headers:
    print(header.text.strip())
    headers_list.append(header.text.strip())

print(headers_list)
full_df = pd.DataFrame(columns = headers_list)
# full_df = full_df.append(headers_list)
# print(soup.prettify())

### Get Fighter Individual Info ###

letters = string.ascii_lowercase
letters = list(letters)
# print(letters)
# letters = ['a', 'b']

for letter in letters:
    source = requests.get(url.format(letter))

    soup = BeautifulSoup(source.content, 'lxml')
    body = soup.find('body')
    table = body.find('table')
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')

    for row in table_rows[1:]:
        fighter_data = []
        # print(row.prettify())
        fighter_infos = row.find_all('td')
        for info in fighter_infos:
            if info.text is None:
                fighter_data.append('')
                print('No text')
            else:
                # print(info.text)
                data = info.text
                fighter_data.append(data.strip())
                # print(fighter_data)

        # print(fighter_data)

        fighter_data = [fighter_data]
        # fighter_df = pd.DataFrame(fighter_data, columns = headers_list)
        # print(fighter_df)
        full_df = full_df.append(pd.DataFrame(fighter_data, columns = headers_list), ignore_index = True)

print(full_df)

full_df.to_csv('fighter_data.csv')
