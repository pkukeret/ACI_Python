import sys
import re
import json
import csv
import re
from acitoolkit import Credentials, Session

# Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Application that logs on to the APIC, and extracts the L3OUT BGP peer configuration details'
creds = Credentials('apic', description)
creds.add_argument('--tenant', help='The name of Tenant')
args = creds.get()

# Login to APIC
session = Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

resp = session.get('/api/class/bgpPeerP.json?rsp-subtree=full&rsp-prop-include=config-only&order-by=bgpPeerP.dn')
#resp = session.get('/api/class/bgpPeerP.json?rsp-subtree=full&query-target-filter=wcard(bgpPeerP.dn,"MBH_L3out")&rsp-prop-include=config-only')
data = json.loads(resp.text)['imdata']
datacount = int(json.loads(resp.text)['totalCount'])

#with open("./bgppeer.json") as file:
#	data = json.load(file)['imdata']

fname = "BGP_Peer_Details.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Tenant","L3OUT Name","Node Profile Name","Interface Profile","Node ID","Path","Peer IP","Peer AS","Peer Cntrl","TTL","Peer Description","Allowed_Self_AS","ctrl","privateASCTRL","weight"])

	numrow = 0
	for i in data:
		itemone = (((i['bgpPeerP'])['attributes']))
		dnstr = itemone['dn']
		dnlen = len(dnstr.split('/'))
		Tenant = ((dnstr.split('/'))[1])[3:]
		l3out = ((dnstr.split('/'))[2])[4:]
		nodepro = ((dnstr.split('/'))[3])[7:]

		itemtwo = (((i['bgpPeerP'])['children']))
		
		AS = itemtwo[1]['bgpAsP']['attributes']['asn']

		if dnlen == 5:

			intfpro =""
			nodeid = ""
			path = ""
			csv_file.writerow([Tenant, l3out, nodepro, intfpro, nodeid, path, itemone['addr'], AS, itemone['peerCtrl'], itemone['ttl'],itemone['descr'],itemone['allowedSelfAsCnt'],itemone['ctrl'],itemone['privateASctrl'],itemone['weight']])

		else:
			intfpro = ((dnstr.split('/'))[4])[5:]
			nodeid = re.split(r's-',((dnstr.split('/'))[7]))[1]
			path = re.split(r'\[|\]', dnstr)[2]
			csv_file.writerow([Tenant, l3out, nodepro, intfpro, nodeid, path, itemone['addr'], AS, itemone['peerCtrl'], itemone['ttl'],itemone['descr'],itemone['allowedSelfAsCnt'],itemone['ctrl'],itemone['privateASctrl'],itemone['weight']])

		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")		