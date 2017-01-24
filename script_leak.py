#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import json
import requests
import os
import time

def copy_csv(email,list_leak,csv):


	csv.write(email+';'+str(list_leak)+';\n')

def find_csv(email,list_leak):

	if os.path.exists('leak_csv.csv') is False:
		csv = open('leak_csv.csv','a+')
		csv.write('email;leak\n')
		copy_csv(email,list_leak,csv)
		csv.close()
	else:
		csv = open('leak_csv.csv','a+')
		copy_csv(email,list_leak,csv)
		csv.close()
		
def search_all_leaks(leak_user):

	leaks=[]
	url = "https://haveibeenpwned.com/api/v2/breachedaccount/"+leak_user
	response = requests.get(url)
	if response.status_code == 200:
		results = response.json()
		for result in results:
			leaks.append(result['Name'])
	else:
		print "Error code %s" % response.status_code
	
	return leaks
		
def search_leak(file):
	
	emails_leak=[]
	
	emails=open(file,'r')
	for line in emails.read().split('\r\n'):
		emails_leak.append(line.encode('utf8'))

	for line_email in emails_leak:
		leak_dict={}
		leak_dict['user']=""
		leak_dict['leaks']=[]
		leak_dict['user']=line_email

		leak_dict['leaks']=search_all_leaks(leak_dict['user'])
		print leak_dict['user'] , leak_dict['leaks']
		find_csv(leak_dict['user'],leak_dict['leaks'])
		time.sleep(2)

	


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-f","--file", help="insert file")
	args = parser.parse_args()
	if not args.file:
		print "Insert a File with emails"
	else:		
		search_leak(args.file)