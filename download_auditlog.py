import requests
from bs4 import BeautifulSoup
import csv
from .secret import *

session = requests.Session()
session.headers.update({
    'User-Agent' : 'Footloose ICT Audit Log Scraper'
})
login = session.get(SITE_URL + 'wp-login.php')
cookies = {"wordpress_test_cookie":"WP Cookie check"}
data = {
    "log" : SITE_USERNAME,
    "pwd" : SITE_PASSWORD,
    "redirect_to": SITE_URL + "wp-admin/",
    "testcookie":1,
    "wp-submit":"Log In"
}
login = session.post(SITE_URL + "wp-login.php", cookies=cookies, data=data)
r = session.get(SITE_URL + "wp-admin/admin.php?page=wsal-auditlog&paged=1")
soup = BeautifulSoup(r.text, 'lxml')

rows = []
pages = int(soup.find('span', class_='total-pages').text)
for i in range(1, pages+1):
    r = session.get(SITE_URL + "wp-admin/admin.php?page=wsal-auditlog&paged={}".format(i))
    soup = BeautifulSoup(r.text, 'lxml')
    rowssoup = soup.find('tbody', id='the-list').findAll('tr')
    for rs in rowssoup:
        cellssoup = rs.findAll('td')
        try:
            user = "{}|{}".format(cellssoup[3].find('a').text, cellssoup[3].contents[-1])
        except:
            user = cellssoup[3].text

        rows.append([
            cellssoup[0].find('span')['data-tooltip'].split('-')[-1].strip("'"),
            cellssoup[2].text,
            user,
            cellssoup[4].text,
            cellssoup[5].text,
        ])
    print("page [{}/{}]".format(i, pages))

with open('data/auditlog.csv', 'w') as stream:
    writer = csv.writer(stream)
    writer.writerows(rows)