import csv

with open('data/auditlog.csv', 'r') as stream:
    reader = csv.reader(stream)
    rows = list(reader)


logclean = []
filterwords = [
    'phpmyadmin',
    'automatically'
]

for row in rows:
    if any(word in ''.join(row).lower() for word in filterwords):
        continue
    if len(row) == 0:
        continue
    row[-1] = row[-1].strip('\n')
    logclean.append(row)

with open('data/auditlog_clean.csv', 'w', newline='') as stream:
    writer = csv.writer(stream)
    writer.writerows(logclean)