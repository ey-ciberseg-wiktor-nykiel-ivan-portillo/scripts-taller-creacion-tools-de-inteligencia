#!/usr/bin/python
# -*- coding: utf-8 -*-
import pythonwhois
import argparse
import os.path
def copy_csv(final_result,csv,domain):
	heads_csv=['city','fax','name','state','phone','street','country','postalcode','organization','email']
	head={}
	head['domain']=domain
	head['city']=""
	head['fax']=""
	head['name']=""
	head['state']=""
	head['phone']=""
	head['street']=""
	head['country']=""
	head['postalcode']=""
	head['organization']=""
	head['email']=""
		
	for key in final_result:	
		for key2,value in key.items():
			for head_csv in heads_csv:
				if key2 in head_csv:
					head[head_csv]=value
		
		
	csv.write(head['domain']+';'+head['city']+';'+head['fax']+';'+head['name']+';'+head['state']+';'+head['phone']+';'+head['street']+';'+head['country']+';'+head['postalcode']+';'+head['organization']+';'+head['email']+"\n")


def find_csv(final_result,domain):
	
	if os.path.exists('whois_csv.csv') is False:
		csv = open('whois_csv.csv','a+')
		csv.write('Domain;City;Fax;name;State;Phone;Street;Country;Postal Code;Organization;Email\n')
		copy_csv(final_result,csv,domain)
		csv.close()
	else:
		csv = open('whois_csv.csv','a+')
		copy_csv(final_result,csv,domain)
		csv.close()
	
def search_whois(domain):
	print domain
	final_result=[]
	domain_whois = pythonwhois.get_whois(domain)
	result_domain=domain_whois['contacts']


	for key,value in result_domain.items():
		if 'registrant' in key:
		
			print value
			final_result.append(value)
	
	
	find_csv(final_result,domain)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-d","--domain", help="insert domain")
	args = parser.parse_args()
	if not args.domain:
		print "Introduce domain with -d or --domain"
	else:
		
		search_whois(args.domain)