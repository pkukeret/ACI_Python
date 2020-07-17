import sys
import re
import json
import csv
from acitoolkit import Credentials, Session

# Take login credentials from the command line if provided
# Otherwise, take them from your environment variables file ~/.profile
description = 'Application that logs on to the APIC, and extracts the L3outs paths along with their vlan encap and IP addresses'

creds = Credentials('apic', description)
creds.add_argument('--tenant', help='The name of Tenant')
args = creds.get()

# Login to APIC
session = Session(args.url, args.login, args.password)
resp = session.login()
if not resp.ok:
    print('%% Could not login to APIC')
    sys.exit(0)

resp = session.get('/api/class/l3extRsPathL3OutAtt.json?rsp-subtree=full&rsp-prop-include=config-only&order-by=l3extRsPathL3OutAtt.dn')
data = json.loads(resp.text)['imdata']
datacount = int(json.loads(resp.text)['totalCount'])

#with open("./tt1l3outpaths.json") as file:
#	data = json.load(file)['imdata']

fname = "L3out_paths_IP.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Tenant","L3OUT Name","Logical Node Profile","Logical Interface Profile","If inst type","Node ID","Port ID","vlan encap","IP address","VIP","SIDE A IP address","SIDE B IP ADDRESS"])

	numrow = 0
	for i in data:
		itemone = (((i['l3extRsPathL3OutAtt'])['attributes']))
		dnstr = itemone['dn']
		Tenant = ((dnstr.split('/'))[1])[3:]
		l3out = ((dnstr.split('/'))[2])[4:]
		nodepro = ((dnstr.split('/'))[3])[7:]
		intfpro = ((dnstr.split('/'))[4])[5:]
		insttype = itemone['ifInstT']
		nodeid = re.split(r's-',((dnstr.split('/'))[7]))[1]
		path = re.split(r'\[|\]', dnstr)[2]
		vlan = itemone['encap'][5:]
		ip = itemone['addr']

		if 'children' in i['l3extRsPathL3OutAtt']:
			itemtwo = (((i['l3extRsPathL3OutAtt'])['children']))
			if 'l3extIp' in itemtwo[0]:
				item3 = itemtwo[0]['l3extIp']['attributes']
				csv_file.writerow([Tenant, l3out, nodepro, intfpro, insttype, nodeid, path, vlan, ip, item3['addr'], "", ""])

			# For L3out Paths those are vPC	
			elif 'l3extMember' in itemtwo[0]:

				# To loop over side A and Side B details
				for j in itemtwo:

					# To check only L3extMember elements and skip the other elements
					if 'l3extMember' in j:

						if j['l3extMember']['attributes']['side'] == 'A':
							sideaip = j['l3extMember']['attributes']['addr']

							# To consider cases where VIP is not  defined for vPC
							if 'children' in j['l3extMember']:
								vip = j['l3extMember']['children'][0]['l3extIp']['attributes']['addr']
							else:
								vip = ""

						elif j['l3extMember']['attributes']['side'] == 'B':
							sidebip = j['l3extMember']['attributes']['addr']

							if 'children' in j['l3extMember']:
								vip = j['l3extMember']['children'][0]['l3extIp']['attributes']['addr']
							else:
								vip = ""

					else:
						continue			

				csv_file.writerow([Tenant, l3out, nodepro, intfpro, insttype, nodeid, path, vlan, ip, vip, sideaip, sidebip])

			# For L3out Paths which have children attributes like BGP config, but do not have external IP (VIP)	
			else:
				csv_file.writerow([Tenant, l3out, nodepro, intfpro, insttype, nodeid, path, vlan, ip, "", "", ""])

		# This would be required for L3out paths which do not have children, like L3out paths with no VIP and with Static routing 		
		else:
			csv_file.writerow([Tenant, l3out, nodepro, intfpro, insttype, nodeid, path, vlan, ip, "", "", ""])

		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")