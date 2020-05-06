import requests
from bs4 import BeautifulSoup

URL = 'https://referensi.data.kemdikbud.go.id/index11.php?kode=010101&level=3'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='example')

print(result.prettify())
