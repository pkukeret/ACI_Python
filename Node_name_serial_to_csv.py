import sys
import re
import json
import csv
from acitoolkit import Credentials, Session


# Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Simple application that logs on to the APIC and extracts Node IDs, Node names and their serial numbers.'
creds = Credentials('apic', description)
creds.add_argument('--tenant', help='The name of Tenant')
args = creds.get()

# Login to APIC
session = Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

resp = session.get('/api/class/fabricNodeIdentP.json?rsp-subtree=full&rsp-prop-include=config-only')
data = json.loads(resp.text)['imdata']
datacount = int(json.loads(resp.text)['totalCount'])


fname = "NodeReginfo.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Node ID","Node Name","Serial Number"])

	numrow = 0
	for i in data:
		itemone = (((i['fabricNodeIdentP'])['attributes']))
		dnstr = itemone['dn']
		nodename = itemone['name']
		nodeid = itemone['nodeId']
		serial = itemone['serial']
		csv_file.writerow([nodeid,nodename, serial])
		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")