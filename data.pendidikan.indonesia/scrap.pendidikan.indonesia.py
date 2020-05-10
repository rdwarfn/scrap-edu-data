import requests
from bs4 import BeautifulSoup
import re
import csv
import os
import time

base = 'https://referensi.data.kemdikbud.go.id/'
URL = f'{base}index11.php?'
page = requests.get(URL)
soup = BeautifulSoup(page.content, 'html.parser')
result = soup.find(id='box-table-a')


def main():
    t0 = time.time()
    try:
        os.mkdir('CSV')
    except FileExistsError:
        pass

    for a in result.tbody.find_all('tr'):
        animation = "|/-\\"
        if a.td.a is not None:
            prov = a.td.a.text.strip()
            try:
                url = f"{base}{a.td.a.get('href')}"
                page2 = requests.get(url)
                soup2 = BeautifulSoup(page2.content, 'html.parser')
                res2  = soup2.find(id='box-table-a')

                rows = []
                idx = 0
                for id_kab, kab in enumerate(res2.tbody.find_all('tr')):
                    if kab.a is not None and kab.a.text:
                        kab_kot = kab.a.string
                        url3 = f"{base}{kab.a.get('href')}"
                        page3 = requests.get(url3)
                        soup3 = BeautifulSoup(page3.content, 'html.parser')
                        res3 = soup3.find(id='box-table-a')

                        for id_kec, kec in enumerate(res3.tbody.find_all('tr')):
                            if kec.a:
                                kcm = kec.a.text.strip()
                                url4 = f"{base}{kec.a['href']}"
                                page4 = requests.get(url4)
                                soup4 = BeautifulSoup(page4.content, 'html.parser')
                                res4  = soup4.find(id='example')
                                rows2 = []
                                for id_tr, tr in enumerate(res4.find_all('tr')):
                                    row = []
                                    for id_d, d in enumerate(tr.find_all('td')):
                                        if id_d:
                                            row.append(d.text.strip())

                                        print(
                                            f"[*] {prov} {animation[idx % len(animation)] } - ({time.time() - t0:0.3f} seconds): ",
                                            f" {kab_kot}: ",
                                            f" {kcm}: ",
                                            f"{d.text.strip()}",
                                            end='\r'
                                        )
                                        idx += 1
                                        time.sleep(0.001)
                                    
                                    if len(row):
                                        row.extend((kcm,kab_kot,prov))
                                    rows.append(row)

                
                sortList = list(filter(None, rows))

                flag = re.sub('[\s./]', '-', prov.lower())
                with open(f'CSV/{flag}.csv', 'w', newline='') as f:
                    writer = csv.writer(f)
                    writer.writerows(sortList)
                    f.close()

            except AttributeError:
                pass
    print(f'[*] Scrapping finished {time.time() - t0} seconds')


if __name__ == "__main__":
    main()
