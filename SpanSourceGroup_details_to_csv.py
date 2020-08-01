import sys
import re
import json
import csv
from acitoolkit import Credentials, Session
'''
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
'''
with open("./spanSrcGrp.json") as file:
	data = json.load(file)['imdata']

fname = "SpanSourceGroups.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Source Group Name","Admin State","Source name","Direction","Node ID","PATH","Source L3OUT IP","Source L3OUT encap","Tenant Name","L3OUT Name","App Profile","EPG Name","Span Dest Grp"])
#	numrow = 0
	for i in data:
		itemone = (((i['spanSrcGrp'])['attributes']))
		SGNAME = itemone['name']
		SGSTATE = itemone['adminSt']

		if 'children' in i['spanSrcGrp']:
			itemtwo = (((i['spanSrcGrp'])['children']))

			DSTGRP = itemtwo[-1]['spanSpanLbl']['attributes']['name']

			for j in itemtwo:

				if 'spanSrc' in j:
					spanSrcatt = j['spanSrc']['attributes']
					SRCNAME = spanSrcatt['name']
					SRCDIR = spanSrcatt['dir']

					spanSrcchld = j['spanSrc']['children']

					if 'spanRsSrcToL3extOut' in spanSrcchld[-1]:

						SRCPATH = spanSrcchld[0]['spanRsSrcToPathEp']['attributes']['tDn']
						NODEid = re.split(r's-',((SRCPATH.split('/'))[2]))[1]
						PATH = re.split(r'\[|\]',SRCPATH)[1]

						SRCL3OUTIP = spanSrcchld[1]['spanRsSrcToL3extOut']['attributes']['addr']
						SRCL3OUTENCAP = spanSrcchld[1]['spanRsSrcToL3extOut']['attributes']['encap'][5:]
						SRCL3OUTtDn = spanSrcchld[1]['spanRsSrcToL3extOut']['attributes']['tDn']
						TENANT = SRCL3OUTtDn.split('/')[1][3:]
						L3OUTname = SRCL3OUTtDn.split('/')[2][4:] 
						APP = ""
						EPG = ""
						csv_file.writerow([SGNAME, SGSTATE, SRCNAME, SRCDIR, NODEid, PATH, SRCL3OUTIP, SRCL3OUTENCAP, TENANT, L3OUTname,APP,EPG,DSTGRP])
					
					else:
						
						if 'spanRsSrcToEpg' in spanSrcchld[-1]:
							EPGtDn = spanSrcchld[-1]['spanRsSrcToEpg']['attributes']['tDn']
							TENANT = EPGtDn.split('/')[1][3:]
							APP = EPGtDn.split('/')[2][3:]
							EPG = EPGtDn.split('/')[3][4:]

						else:
							APP = ""
							EPG = ""

						for k in spanSrcchld:

							if 'spanRsSrcToPathEp' in k:

								SRCPATH = k['spanRsSrcToPathEp']['attributes']['tDn']
								NODEid = re.split(r's-',((SRCPATH.split('/'))[2]))[1]
								PATH = re.split(r'\[|\]',SRCPATH)[1]								
								SRCL3OUTIP = ""
								SRCL3OUTENCAP = ""
								L3OUTname = ""


							else:
								continue
							
							csv_file.writerow([SGNAME, SGSTATE, SRCNAME, SRCDIR, NODEid, PATH, SRCL3OUTIP, SRCL3OUTENCAP, TENANT, L3OUTname,APP,EPG,DSTGRP])

				else:
					continue


#		numrow += 1

#if numrow == datacount:
#	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
#else:
#	print ("Script Executed Successfully, but Count does not match !")