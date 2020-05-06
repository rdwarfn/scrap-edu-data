import requests
import csv
import re
from bs4 import BeautifulSoup
import os

base = 'https://referensi.data.kemdikbud.go.id/'
URL = f'{base}index11.php?'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='box-table-a').tbody


for a in result.find_all('a'):

    print('[*] ' + a.text)
    URL2 = f"{base}{a.get('href')}"
    page2 = requests.get(URL2)
    soup2 = BeautifulSoup(page2.content, 'html.parser')
    result2 = soup2.find(id='box-table-a').tbody
    direc = a.text
    os.mkdir(direc)

    for tr in result2.find_all('tr'):

        for a2 in tr.find_all('a'):
            URL3  = f"{base}{a2.get('href')}"
            page3 = requests.get(URL3)
            soup3 = BeautifulSoup(page3.content, 'html.parser')
            result3 = soup3.find(id='box-table-a').tbody
            
            for a3 in result3.find_all('a'):
                flag = re.sub(r'[./\s]', '-', a3.text)
                URL4 = f"{base}{a3.get('href')}"
                page4= requests.get(URL4) 
                soup4 = BeautifulSoup(page4.content, 'html.parser')
                result4 = soup4.find(id='example')

                output_rows = []
                for row in result4.find_all('tr'):
                    output_row = []
                    for col in row.find_all('td'):
                        output_row.append(col.text.strip())
                    output_rows.append(output_row)

                with open(f'{direc}/{flag}.csv', 'w', newline='') as csvfile:
                    writer = csv.writer(csvfile)
                    writer.writerows(output_rows)
    print('[*] clear')
    print()