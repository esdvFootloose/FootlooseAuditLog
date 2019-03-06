import csv
import geoip2.database
from datetime import datetime
import yaml
import socket
from ipwhois import IPWhois

georeader = geoip2.database.Reader('GeoLite2-City.mmdb')

begin = datetime.strptime("01/11/2018", "%d/%m/%Y")

with open('data/auditlog_clean.csv', 'r') as stream:
    reader = csv.reader(stream)
    rows = list(reader)

failed_logins = []
ips = {}
hosts = {}
for row in rows:
    if 'login failed' in row[0].lower() and int(row[4].split(' ')[0].strip('+')) > 3:
        date = datetime.strptime(row[1].split('.')[0], "%d-%m-%Y%H:%M%S")
        if date < begin:
            continue
        data = [
            date,
            row[2].split('|')[0],
            row[4].split(' ')[0],
            row[3],
        ]
        if row[3] != 'unknown':
            georesponse = georeader.city(row[3])
            data += [ georesponse.city.name,
                      georesponse.country.iso_code ]
        else:
            data += [ '-', '-']
        if data[3] not in ips:
            print("IP {} is new, fetching info".format(data[3]))
            reversedns = "-"
            try:
                reversedns = socket.gethostbyaddr(data[3])[0]
            except:
                r = IPWhois("62.140.137.77").lookup_whois()
                for n in r['nets']:
                    if n['emails'] is not None:
                        reversedns = "|".join(n['emails'])
                        break
            ips[row[3]] = {
                "city" : data[4],
                "country" : data[5],
                "amount" : int(data[2].strip('+')),
                "reversedns" : reversedns,
                "offenses" : [str(date)]
            }
        else:
            ips[row[3]]['amount'] += int(data[2].strip('+'))
            ips[row[3]]["offenses"].append(str(date))
        failed_logins.append(data)

failed_logins = sorted(failed_logins, key = lambda x: (x[1], x[0]))

failed_logins = [[
        'date',
        'user',
        'ammount',
        'ip',
        'city',
        'country'
    ]] + failed_logins

with open('data/failed_logins.csv', 'w', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerows(failed_logins)

with open("data/baddies.yaml", "w") as stream:
    yaml.dump(ips, stream, default_flow_style=False)