import requests
import csv
from bs4 import BeautifulSoup

URL = 'https://referensi.data.kemdikbud.go.id/index11.php?kode=010101&level=3'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='example')

output_rows = []
for row in result.find_all('tr'):
    output_row = []
    for col in row.find_all('td'):
        output_row.append(col.text.strip())
    output_rows.append(output_row)

print(output_rows)
with open('output.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(output_rows)
    