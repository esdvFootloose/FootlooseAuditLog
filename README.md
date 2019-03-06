# Footloose Audit Log Analyser

Source code to download and analyze our audit log. This is a set of scripts to download the log
for the wordpress audit log plugin.

## Usage
First put SITE_USER SITE_PASSWORD and SITE_URL in secret.py.
Then run the scripts in the following order, each will create a new file in data to view and the next step uses that file as input.

1. download_auditlog.py
1. clean_auditlog.py
1. failed_login_check_auditlog.py
1. getbadhosts.py

This will result in a baddies_per_host.yaml which gives list of hosts with belonging ips that tried to bruteforce logins.