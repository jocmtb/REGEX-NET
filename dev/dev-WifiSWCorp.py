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

def show(HOST,comandos):
	for item in HOST:
        	try:
                	tn = telnetlib.Telnet(item)
                	tn.read_until("username: ")
                	tn.write((user + "\n").encode('ascii'))
                	tn.read_until("password: ")
                	tn.write((password + "\n").encode('ascii'))
                	tn.write("terminal len 0\n")
			for comando in comandos:
                		tn.write(comando)
                	tn.write("exit\n")
                	print "# Getting info from device "+item
                	running = tn.read_all()
                	output=str(running)
                	print output
                	tn.close()
                	del tn
        	except:
                	print("# Unexpected ERROR: on host " + item)

if __name__=='__main__':
	x = datetime.datetime.now()
	date = ("%s-%s-%s_%s:%s" % (x.year, x.month, x.day,x.hour,x.minute) )
	START = ("%s-%s-%s_%s:%s:%s" % (x.year, x.month, x.day,x.hour,x.minute,x.second) )
	HOST1=['172.19.231.132']
	HOST2=['172.19.231.148']
	os.system('clear')
	print '''
             <<  Script para switches Wifi  >>
	      '''
	user = "E702778"
	password = "Lima2017#"


	comand1=['show version | i uptime \n'
	        ,'show spann det | i change\n'
	        ,'show int desc  | e admin \n']
	show(HOST1,comand1)
	#show(HOST2,comand1)

	y = datetime.datetime.now()
	STOP = ("%s-%s-%s_%s:%s:%s" % (y.year, y.month, y.day,y.hour,y.minute,y.second) )
	print("Time Execution of the script:")
	print("Start: " + START)
	print("Stop: " + STOP)

	exit()
