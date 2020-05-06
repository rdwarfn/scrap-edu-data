import requests
import csv
import re
from bs4 import BeautifulSoup

base = 'https://referensi.data.kemdikbud.go.id/'
URL = f'{base}index11.php?kode=010000&level=1'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='box-table-a').tbody


for tr in result.find_all('tr'):

    for a in tr.find_all('a'):
        URL2  = f"{base}{a.get('href')}"
        page2 = requests.get(URL2)
        soup2 = BeautifulSoup(page2.content, 'html.parser')
        result2 = soup2.find(id='box-table-a').tbody
        
        for a2 in result2.find_all('a'):
            flag = re.sub(r'\s', '-', a2.text)
            URL3 = f"{base}{a2.get('href')}"
            page3= requests.get(URL3) 
            soup3 = BeautifulSoup(page3.content, 'html.parser')
            result3 = soup3.find(id='example')

            output_rows = []
            for row in result3.find_all('tr'):
                output_row = []
                for col in row.find_all('td'):
                    output_row.append(col.text.strip())
                output_rows.append(output_row)

            with open(f'{flag}.csv', 'w', newline='') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerows(output_rows)