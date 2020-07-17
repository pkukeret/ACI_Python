import json
import csv

with open("./bgpstate.json") as file:
	data = json.load(file)['imdata']
	datacount = int(json.loads(resp.text)['totalCount'])
	#print(data[0])
	#itemone = (((data[0]['bgpPeerEntry'])['attributes']))

fname = "outputbgp.csv"

with open(fname, "w") as file:
	csv_file = csv.writer(file)
	csv_file.writerow(["Peer IP","Local IP","Domain Name","State","Remote Router ID","BGP Type"])

	numrow = 0
	for i in data:
		itemone = (((i['bgpPeerEntry'])['attributes']))
		csv_file.writerow([itemone['addr'],itemone['localIp'],itemone['dn'],itemone['operSt'],itemone['rtrId'],itemone['type']])
		numrow += 1

if numrow == datacount:
	print ("Script Executed Successfully, CSV rows count matches Response data total count !")
else:
	print ("Script Executed Successfully, but Count does not match !")		