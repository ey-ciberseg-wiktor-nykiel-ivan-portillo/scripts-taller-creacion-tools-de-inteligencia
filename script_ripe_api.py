#!/usr/bin/python
# -*- coding: utf-8 -*-
from urllib2 import Request, urlopen
import json

def copy_csv(final_result):
	csv = open('ripe_csv.csv','a+')
	print final_result

	csv.write('inetnum;netname;descr;descr2;descr3\n')
	
	for dict1 in final_result:
		for dict2 in dict1:
			for key,value in dict2.items():
				csv.write(value+';')
		csv.write('\n')

	csv.close()
	
def search_ripe():
	inetnum=[]
	request = Request("http://rest.db.ripe.net/search.json?query-string=EY")
	response_body = urlopen(request).read()
	tmp = json.loads(response_body)
	ripe=tmp['objects']['object']
	final_result=[]
	for i in ripe:
		if 'inetnum' in i['type']:
			total=i
			line_result=[]
			for line in total['attributes']['attribute']:
				
				if "inetnum" in line['name'] or "netname" in line['name'] or "descr" in line['name']:
					
					file={str(line['name']):str(line['value'])}
					line_result.append(file)
					 
			final_result.append(line_result)

	copy_csv(final_result)

if __name__ == '__main__':
  search_ripe()