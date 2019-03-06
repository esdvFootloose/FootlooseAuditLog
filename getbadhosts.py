import yaml

with open('data/baddies.yaml', 'r') as stream:
    data = yaml.load(stream)

hosts = {}

for ip, v in data.items():
    if "|" in v['reversedns']:
        domain = ".".join(v['reversedns'].split('|')[0].split('.')[-2:])
    else:
        domain = ".".join(v['reversedns'].split('.')[-2:])
    if domain not in hosts:
        hosts[domain] = [
            [ip, v['offenses']]
        ]
    else:
        hosts[domain].append([
            [ip, v['offenses']]
        ])

with open('data/baddies_per_host.yaml', 'w') as stream:
    yaml.dump(hosts, stream)