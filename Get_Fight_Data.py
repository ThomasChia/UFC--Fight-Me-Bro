from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import requests
import csv

with open('fight_links.csv', newline='') as f:
    reader = csv.reader(f)
    links = list(reader)

print(links[1])
print(len(links))
links = [''.join(x) for x in links]
# print(links)
columns_ = ['Date', 'Winner', 'Loser', 'KD_W', 'KD_L', 'STR_W', 'STR_L', 'TD_W', 'TD_L', 'SUB_W', 'SUB_L', 'WEIGHT CLASS', 'PERF', 'FINISH', 'METHOD', 'ROUND', 'TIME']
fight_data = pd.DataFrame(columns = columns_)

for link in links:
    source = requests.get(str(link))
    soup = BeautifulSoup(source.content, 'lxml')

    body = soup.find('body')
    date_tag = body.find('li', {'class': 'b-list__box-list-item'})
    # date = date_tag.text.strip()
    date = date_tag.get_text(strip = True)
    date = date[5:]
    print(date)

    table = soup.find('table')
    table_body = table.find('tbody')
    table_rows = table_body.find_all('tr')
    print('a')
    for row in table_rows:
        fight_list = []
        fight_list.append(date.strip('/n'))
        print('b')
        table_data = row.find_all('td')
        for data in table_data[1:]:
            # print('c')
            p_tags = data.find_all('p')
            for p_tag in p_tags:
                # print(p_tag.text.strip())
                fight_list.append(p_tag.text.strip())
                if len(fight_list) == 12:
                    perf = p_tag.find('img')
                    if perf is not None:
                        fight_list.append(1)
                    else:
                        fight_list.append(0)
        print(fight_list)

        fight_list = [fight_list]
        fight_data = fight_data.append(pd.DataFrame(fight_list, columns=columns_), ignore_index=True)


print(fight_data)
fight_data.to_csv('fight_data.csv')
# test_list_2 = test_list.strip('\n')
# print(test_list_2)


