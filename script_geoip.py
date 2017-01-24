#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
import argparse
import os
import json
from geoip import geolite2
def copy_csv(geoip_result,csv,domain):

	domain_result=domain
	country=str(geoip_result.country)
	continent=str(geoip_result.continent)
	timezone=str(geoip_result.timezone)
	location=str(geoip_result.location)
		
	csv.write(domain_result+';'+country+';'+continent+';'+timezone+';'+location+';\n')


def find_csv(geoip_result,domain):
	
	if os.path.exists('geoip_csv.csv') is False:
		csv = open('geoip_csv.csv','a+')
		csv.write('Domain;Country;Continent;Timezone;Location\n')
		copy_csv(geoip_result,csv,domain)
		csv.close()
	else:
		csv = open('geoip_csv.csv','a+')
		copy_csv(geoip_result,csv,domain)
		csv.close()
	
def search_geoip(domain):
	print domain

	ip = socket.gethostbyname(domain)
	geoip_result = geolite2.lookup(ip)
	print geoip_result
	find_csv(geoip_result,domain)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-d","--domain", help="insert domain")
	args = parser.parse_args()
	if not args.domain:
		print "Introduce domain with -d or --domain"
	else:
		
		search_geoip(args.domain)