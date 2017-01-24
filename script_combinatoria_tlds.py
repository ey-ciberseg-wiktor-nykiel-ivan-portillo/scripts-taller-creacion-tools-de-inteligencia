#!/usr/bin/python
# -*- coding: utf-8 -*-
import pythonwhois
import argparse
import os.path
from script_tlds_mx_ns import search_domains

	
def search_tld(domain,file):
	final_result=[]
	domain_all=[]
	domain_sintld=domain.split('.')

	tlds=open(file,'r')
	for tld in tlds.read().split('\r\n'):
		domain_all.append(domain_sintld[0]+tld)
	
	for domain in domain_all:
		
		print domain
		search_domains(domain)
	


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-d","--domain", help="insert domain")
	parser.add_argument("-f","--file", help="insert file")
	args = parser.parse_args()
	if not args.domain:
		print "Introduce domain with -d or --domain"
	elif not args.file:
		print "Introduce file with -f or --file"
	else:
		
		search_tld(args.domain,args.file)
		
		