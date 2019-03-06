import csv
import geoip2.database
from datetime import datetime

georeader = geoip2.database.Reader('./GeoLite2-City.mmdb')

with open('data/auditlog_clean.csv', 'r') as stream:
    reader = csv.reader(stream)
    rows = list(reader)

foreign_logins = []

for row in rows:
    if 'logged in' in row[0].lower():
        if row[3] != 'unknown':
            georesponse = georeader.city(row[3])
            if georesponse.country.iso_code in ['NL', 'BE', 'DE']:
                continue
        else:
            continue
        date = datetime.strptime(row[1].split('.')[0], "%d-%m-%Y%H:%M%S")
        data = [
            date,
            row[2].split('|')[0],
            row[3],
            georesponse.city.name,
            georesponse.country.iso_code
        ]
        foreign_logins.append(data)

foreign_logins = sorted(foreign_logins, key = lambda x: (x[1], x[0]))

foreign_logins = [[
        'date',
        'user',
        'ip',
        'city',
        'country'
    ]] + foreign_logins

with open('data/foreign_logins.csv', 'w') as stream:
    writer = csv.writer(stream)
    writer.writerows(foreign_logins)