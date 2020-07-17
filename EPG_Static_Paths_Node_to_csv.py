import sys
import re
import json
import csv
import re
from acitoolkit import Credentials, Session

#Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Application that logs on to the APIC, and extracts the EPG Static Paths for the user provided input Node ID'
creds = Credentials('apic', description)
creds.add_argument('--tenant', help='The name of Tenant')
args = creds.get()

# Login to APIC
session = Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

while True:
	try:
		inputnode = input("Enter the Node ID: ")
		if (len(inputnode) == 4):
			nodeidint = int(inputnode)
			break
		else:
			print("Node ID is INVALID ! try again")
			continue
	except ValueError:
		print("INVALID IP address ! Enter Numeric values only")

resp = session.get("/api/class/fvRsPathAtt.json?query-target-filter=wcard(fvRsPathAtt.tDn,\""+inputnode+"\")")
data = json.loads(resp.text)['imdata']
datacount = int(json.loads(resp.text)['totalCount'])

fname = "EPG_Static_Ports_"+inputnode+".csv"
#fname = "EPGpathsdetailsapinode.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Tenant","APP_Profile","EPG_Name","Node","port","encap","Mode"])

	numrow = 0
	for i in data:
		itemone = (((i['fvRsPathAtt'])['attributes']))
		dnstr = itemone['dn']
		tenant = dnstr.split("/")[1][3:]
		apppro = dnstr.split("/")[2][3:]
		epg = dnstr.split("/")[3][4:]
		nodeid = re.split(r's-',((dnstr.split('/'))[6]))[1]
		path = re.split(r'\[|\]', dnstr)[2]
		csv_file.writerow([tenant, apppro, epg, nodeid,path,itemone['encap'],itemone['mode']])
		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")