#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import json
import dns.resolver
def copy_csv(domain,a,ns,mx,csv):
	list_ns={}
	list_mx={}
	list_ns["ns1"]=""
	list_ns["ns2"]=""
	list_ns["ns3"]=""
	list_ns["ns4"]=""
	list_mx["mx1"]=""
	list_mx["mx2"]=""
	list_mx["mx3"]=""
	list_mx["mx4"]=""
	cont_ns=0
	cont_mx=0
	
	for i in ns:
		cont_ns=cont_ns+1
		list_ns['ns'+str(cont_ns)]=i
		
	for i in mx:
		cont_mx=cont_mx+1
		list_mx['mx'+str(cont_mx)]=str(i)
	
	if [] is a:
		a_result="None"
	else:
		a_result=str(a)
	
	csv.write(domain+';'+a_result+';'+list_ns["ns1"]+';'+list_ns["ns2"]+';'+list_ns["ns3"]+';'+list_ns["ns4"]+';'+list_mx["mx1"]+';'+list_mx["mx2"]+';'+list_mx["mx3"]+';'+list_mx["mx4"]+';\n')

def find_csv(domain,a,ns,mx):
	
	if os.path.exists('tlds_domains_csv.csv') is False:
		csv = open('tlds_domains_csv.csv','a+')
		csv.write('Domain;A;NS1;NS2;NS3;NS4;MX1;MX2;MX3;MX4\n')
		copy_csv(domain,a,ns,mx,csv)
		csv.close()
	else:
		csv = open('tlds_domains_csv.csv','a+')
		copy_csv(domain,a,ns,mx,csv)
		csv.close()

def search_ns(domain):

	list_ns=[]
	num_ns=0
	try:
		answers_ns = dns.resolver.query(domain, 'NS')
		for i in answers_ns:
			num_ns=num_ns+1			
			if num_ns<=4:
				if num_ns==1:
					ns1=i.to_text()
					list_ns.append(ns1)

				elif num_ns==2:
					ns2=i.to_text()
					list_ns.append(ns2)
				elif num_ns==3:
					ns3=i.to_text()
					list_ns.append(ns3)		
				elif num_ns==4:
					ns4=i.to_text()
					list_ns.append(ns4)		
	except:
		print "error"
	return list_ns
	
def search_mx(domain):
	list_mx=[]
	num_mx=0
	try:
		answers_mx = dns.resolver.query(domain, 'MX')
		for i in answers_mx:
			num_mx=num_mx+1
			if num_mx<=4:
				if num_mx==1:
					mx1=i.exchange
					list_mx.append(mx1)
				elif num_mx==2:
					mx2=i.exchange
					list_mx.append(mx2)
				elif num_mx==3:
					mx3=i.exchange
					list_mx.append(mx3)	
				elif num_mx==4:
					mx4=i.exchange
					list_mx.append(mx4)
	except:
		mx1=""
		mx2=""
		mx3=""
		mx4=""		
	return list_mx	
	
def search_domains(domain):
	a=[]
	try:	
		answer = dns.resolver.query(domain, 'A')
		for i in answer:
			a.append(str(i))
		
	except:
		a=[]
	
	ns=search_ns(domain)
	mx=search_mx(domain)
	print a,domain,ns,mx
	find_csv(domain,a,ns,mx)


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-d","--domain", help="insert domain")
	args = parser.parse_args()
	if not args.domain:
		print "Introduce domain with -d or --domain"
	else:		
		search_domains(args.domain)