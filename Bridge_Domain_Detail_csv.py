import sys
import re
import json
import csv
from acitoolkit import Credentials, Session

# Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Application that logs on to the APIC, and extracts the BD information to a csv file. Only first 3 IP Subnets for a BD will be shown'
creds = Credentials('apic', description)
creds.add_argument('--tenant', help='The name of Tenant')
args = creds.get()

# Login to APIC
session = Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

resp = session.get('/api/class/fvBD.json?rsp-subtree=full&rsp-prop-include=config-only&order-by=fvBD.name')
data = json.loads(resp.text)['imdata']
datacount = int(json.loads(resp.text)['totalCount'])

#with open("./BDinfo.json") as file:
#	data = json.load(file)['imdata']

fname = "Bridge_Domain_Details.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Tenant","BD Name","Description","ARP Flooding","IP Learning","LimitIPLearnToSubnets","Unicast Routing","UnknownMacUnicastAct","IP_Subnet-1","Subnet-1_Scope","IP_Subnet-2","Subnet-2_Scope","IP_Subnet-3","Subnet-3_Scope"])

	numrow = 0
	for i in data:
		itemone = (((i['fvBD'])['attributes']))
		dnstr = itemone['dn']
		Tenant = ((dnstr.split('/'))[1])[3:]
		bd = ((dnstr.split('/'))[2])[3:]
		itemtwo = (((i['fvBD'])['children']))
		subdic = {'subnet0':"",'scope0':"",'subnet1':"",'scope1':"",'subnet2':"",'scope2':""}
		no = 0
		for j in itemtwo:
			if 'fvSubnet' in j:
				subdic['subnet{}'.format(no)]=j['fvSubnet']['attributes']['ip']
				subdic['scope{}'.format(no)]=j['fvSubnet']['attributes']['scope']	
				no = no + 1

			else:
				continue				

		csv_file.writerow([Tenant, bd, itemone['descr'], itemone['arpFlood'], itemone['ipLearning'],itemone['limitIpLearnToSubnets'],itemone['unicastRoute'],itemone['unkMacUcastAct'],subdic['subnet0'],subdic['scope0'],subdic['subnet1'],subdic['scope1'],subdic['subnet2'],subdic['scope2']])

		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")		