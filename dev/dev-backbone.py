#!/usr/bin/python

#-------------------------------------------------------------------------------
# Purpose:     Monitor Nexus
# Enterprise:  CLARO Cisco
# Date:     15 de Setiembre 2017
#-------------------------------------------------------------------------------

import datetime
import getpass
import time
import sys
import telnetlib
import os
import re

def show(HOST,comandos):
	for item in HOST:
        	try:
                	tn = telnetlib.Telnet(item)
                	tn.read_until("username: ")
                	tn.write((user + "\n").encode('ascii'))
                	tn.read_until("password: ")
                	tn.write((password + "\n").encode('ascii'))
                	tn.write("terminal len 14\n")
			for comando in comandos:
                		tn.write(comando)
                	tn.write("exit\n")
                	#print "# Getting info from device "+item
                	running = tn.read_all()
                	output=str(running)[4:]
                	print output
			return output
                	tn.close()
                	del tn
        	except:
                	print("# Unexpected ERROR: on host " + item)

def parse(salida):
	for line in salida.split('\n'):
		topochange=re.search('^          from (.+)',line)
		if topochange:
			TCN=topochange.group(1)
			return TCN
	#print TCN

if __name__=='__main__':
	x = datetime.datetime.now()
	date = ("%s-%s-%s_%s:%s" % (x.year, x.month, x.day,x.hour,x.minute) )
	START = ("%s-%s-%s_%s:%s:%s" % (x.year, x.month, x.day,x.hour,x.minute,x.second) )
	HOST1=['172.19.204.1']
	HOST2=['172.19.204.2']
	os.system('clear')
	print '''
             <<  Script para Topology Change in MST  >>
	      '''
	user = "E702778"
	password = "Lima2017#"

	#TCN=''
	comand1=['show spanning detail \n'
	        ,'q \n'
	        ,'\n']
	#comand2=['show interface '+TCN+' description \n','q \n','\n']
	output=show(HOST1,comand1)
	TCN=parse(output).rstrip()
	comand3=['show interface '+TCN+' description \n','q \n','\n']
	#print comand3
	show(HOST1,comand3)
	output2=show(HOST2,comand1)
	TCN2=parse(output2).rstrip()
	comand4=['show interface '+TCN2+' description \n','q \n','\n']
	show(HOST2,comand4)

	y = datetime.datetime.now()
	STOP = ("%s-%s-%s_%s:%s:%s" % (y.year, y.month, y.day,y.hour,y.minute,y.second) )
	print("Time Execution of the script:")
	print("Start: " + START)
	print("Stop: " + STOP)

	exit()
