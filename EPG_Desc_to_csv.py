import json
import csv

with open("./SN2_EPG.json") as file:
	data = json.load(file)['imdata']
	datacount = int(json.loads(resp.text)['totalCount'])
	#print(data[0])
	#itemone = (((data[0]['bgpPeerEntry'])['attributes']))

fname = "EPGdetails.csv"

with open(fname, "w", newline='') as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["EPG_Name","Descr","Domain Name"])

	numrow = 0
	for i in data:
		itemone = (((i['fvAEPg'])['attributes']))
		csv_file.writerow([itemone['name'],itemone['descr'],itemone['dn']])

		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")		