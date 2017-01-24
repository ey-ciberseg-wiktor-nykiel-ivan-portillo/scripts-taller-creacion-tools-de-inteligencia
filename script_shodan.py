#!/usr/bin/python
# -*- coding: utf-8 -*-
import argparse
import os
import json
import shodan
from conf import API_SHODAN
def copy_csv(activos,rango,csv):

	for activo in activos:
		csv.write(rango+';'+str(activo['ip'])+';'+str(activo['asn'])+';'+str(activo['isp'])+';'+str(activo['puertos'])+';'+str(activo['modulo'])+';'+str(activo['org'])+';'+str(activo['domains'])+';'+str(activo['location'])+';'+str(activo['hostnames'])+';'+str(activo['os'])+';'+str(activo['cpe'])+';'+str(activo['product'])+';'+str(activo['vuln'])+';'+str(activo['ssh'])+';\n')

def find_csv(activo,rango):

	if os.path.exists('shodan_csv.csv') is False:
		csv = open('shodan_csv.csv','a+')
		csv.write('rango;ip;asn;isp;puertos;module;org;domains;location;hostnames;os;cpe;product;vuln;ssh\n')
		copy_csv(activo,rango,csv)
		csv.close()
	else:
		csv = open('shodan_csv.csv','a+')
		copy_csv(activo,rango,csv)
		csv.close()

def search_shodan(rango):
	api = shodan.Shodan(API_SHODAN)
	dict_shodan={}
	dict_shodan["rango"]=rango
	activo=[]
	print dict_shodan["rango"]
	try:
		# busqueda de rangos IP en Shodan
		host = api.search("net:'%s'" %(rango))

        # recorrido de cada resultado de shodanl
		for i in host['matches']:
			dict_shodan["ips"]={}
			dict_shodan["ips"]["asn"]=""
			dict_shodan["ips"]["puertos"]=""
			dict_shodan["ips"]["isp"]=""
			dict_shodan["ips"]["org"]=""
			dict_shodan["ips"]["domains"]=""
			dict_shodan["ips"]["hostnames"]=""
			dict_shodan["ips"]["location"]=""
			dict_shodan["ips"]["ip"]=""
			dict_shodan["ips"]["os"]=""
			dict_shodan["ips"]["cpe"]=[]
			dict_shodan["ips"]["product"]=""
			dict_shodan["ips"]["modulo"]=[]
			dict_shodan["ips"]['vuln']=[]
			dict_shodan["ips"]['ssh']=[]
			host_buscar=api.host(i['ip_str'])
			if 'ssh' in i:
				dict_shodan["ips"]['ssh']=i['ssh']
			if 'cpe' in i:
				dict_shodan["ips"]["cpe"]=i['cpe']
			dict_shodan["ips"]["os"]=i['os']
			dict_shodan["ips"]["modulo"]=i['_shodan']['module']
			dict_shodan["ips"]["domains"]=i['domains']

			for it in host_buscar['data']:
				if 'org' in it:
					dict_shodan["ips"]["org"]=it['org'].decode('utf-8')
					if 'asn' in it:
						dict_shodan["ips"]["asn"]=it['asn'].decode('utf-8')
			if 'vuln' in host_buscar:
				dict_shodan["ips"]['vuln']=host_buscar['vuln']
			# Imprimimos los banners
			dict_shodan["ips"]["ip"]=host_buscar['ip_str']
			print(host_buscar['ip_str'])
			if 'product' in i: 
				dict_shodan["ips"]["product"]=i['product']
			dict_shodan["ips"]["puertos"]=host_buscar['ports']
			dict_shodan["ips"]["isp"]=host_buscar['isp'].decode('utf-8')
			dict_shodan["ips"]["location"]=host_buscar['country_name']
			activo.append(dict_shodan["ips"])
			print activo
			find_csv(activo,rango)
			print '\n--------------------\n'
		
		
	except Exception as e:
		print 'Ha ocurrido un error: %s' % e	


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-r","--rango", help="inserte rango")
	args = parser.parse_args()
	if not args.rango:
		args.rango='194.165.144.224-194.165.144.231'
			
	search_shodan(args.rango)