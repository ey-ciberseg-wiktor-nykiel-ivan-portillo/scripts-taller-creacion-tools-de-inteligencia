#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import os.path
import nmap
def copy_csv(final_result,csv):
	
	
	
		
	for key,value in final_result.items():
		ip=key
		ports=""
		product=""
		state=""
		version=""
		extra_info=""
		cpe=""
		
		if value.has_key('status'):
			listaProtocolos = ["udp", "tcp", "icmp"]
			for protocol in listaProtocolos:
				if value.has_key(protocol):
					list_ports = value[protocol].keys()
					for port in list_ports:
						ports=port
						product = value[protocol][port]['product']
						state = value[protocol][port]['state']
						version = value[protocol][port]['version']
						extra_info = value[protocol][port]['extrainfo']
						cpe = value[protocol][port]['cpe']
						print str(key)+';'+str(ports)+';'+str(product)+';'+str(state)+';'+str(version)+';'+str(extra_info.replace(';',','))+';'+str(cpe)+"\n"
						csv.write(str(key)+';'+str(ports)+';'+str(product)+';'+str(state)+';'+str(version)+';'+str(extra_info.replace(';',','))+';'+str(cpe)+"\n")


def find_csv(final_result):
	
	if os.path.exists('nmap_csv.csv') is False:
		csv = open('nmap_csv.csv','a+')
		csv.write('ip;Ports;Product;State;Version;Extra Info;cpe\n')
		copy_csv(final_result,csv)
		csv.close()
	else:
		csv = open('nmap_csv.csv','a+')
		copy_csv(final_result,csv)
		csv.close()
		
def ejecutar_nmap(host, argumentos, puertos=""):  # Ejecutar comandos de nmap
    try:
        escaneo = nmap.PortScanner()                            # Abre el portscanner de nmap
        escaneo.scan(host, arguments=argumentos)            # Ejecuta el comando con los argumentos pasados
        return escaneo
    except Exception:
        RuntimeWarning
				
def search_nmap(ip):
	print ip
	final_result=[]

	nmap_result=ejecutar_nmap(ip,"-sS -O -sV")
	
	for clave, valor in list(nmap_result.__dict__.items()):  # recorre el resultado
           if isinstance(valor, dict):
				print valor['scan']
				find_csv(valor['scan'])

		
	#find_csv(final_result,domain)

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument("-ip","--ip", help="insert IP")
	args = parser.parse_args()
	if not args.ip:
		print "Introduce IP with -ip or --ip"
	else:
	
		search_nmap(args.ip)