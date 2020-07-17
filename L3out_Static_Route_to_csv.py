import sys
import re
import json
import csv
from acitoolkit import Credentials, Session


# Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Simple application that logs on to the APIC and Extracts the L3out Static Routes information.'
creds = Credentials('apic', description)
creds.add_argument('--tenant', help='The name of Tenant')
args = creds.get()

# Login to APIC
session = Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

resp = session.get('/api/class/ipRouteP.json?rsp-subtree=full&rsp-prop-include=config-only&order-by=ipRouteP.dn')
data = json.loads(resp.text)['imdata']
datacount = int(json.loads(resp.text)['totalCount'])

fname = "Static_Route.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Tenant","L3OUT","Logical Node Profile","Node ID","IP Prefix","Route Pref","Next Hop","NH Pref","Route Control"])

	numrow = 0
	for i in data:
		itemone = (((i['ipRouteP'])['attributes']))
		itemtwo = ((((((i['ipRouteP'])['children']))[0])['ipNexthopP'])['attributes'])
		dnstr = itemone['dn']
		Tenant = ((dnstr.split('/'))[1])[3:]
		L3OUT = ((dnstr.split('/'))[2])[4:]
		nodepro = ((dnstr.split('/'))[3])[7:]
		nodeid = ((dnstr.split('/'))[6])[5:-1]
		csv_file.writerow([Tenant, L3OUT, nodepro, nodeid, itemone['ip'],itemone['pref'],itemtwo['nhAddr'],itemtwo['pref'],itemone['rtCtrl']])
		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")		
		