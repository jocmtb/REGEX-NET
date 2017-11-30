'''
Jose Costa
Enero 2017
Claro Peru
'''
from pprint import pprint
import sys
import os
import re
import paramiko as pm
import getpass

def ordenar(lista):

	for x in lista:
		if x.count('/')==1:
			y=x.split('/')
			if len(y[1])==1:
				jose=y[0]+'/0'+y[1]
				lista2.append(jose)
		else:
			lista2.append(x)
	lista2.sort()

	for x in lista2:
		if x.count('/')==1:
			y=x.split('/')
			if y[1].startswith('0'):
				y[1]=y[1][1:]
				jose=y[0]+'/'+y[1]
				lista3.append(jose)
		else:
			lista3.append(x)


def show(int_dict,int_dict2,int_dict3):
 print " +--"+"-"*110+"-+"
 print " | %20s | %20s | %20s | %20s | %19s |" % (HOSTNAME,HOSTNAME,HOSTNAME,HOSTNAME,HOSTNAME) 	
 print " +--"+"-"*110+"-+"
 print " |%-24s |%10s| %10s| %-60s|" % ('Interface','Input(Mbps)','Output(Mbps)','Description')
 print " +--"+"-"*110+"-+"
 Ks=list(int_dict.keys())
 Ks.sort()
 ordenar(Ks)
 for k in lista3:
  if(float(int_dict[k])>0.9 or float(int_dict2[k])>0.9):
   if (float(int_dict[k])>100 or float(int_dict2[k])>100):
    if int_dict[k]!=str(HIGH):
     print " |%-24s*|%10s| %10s| %-63s|" % (k, int_dict[k], int_dict2[k], int_dict3[k])
    else:
     print " |%-23s>*|%10s| %10s| %-63s|" % (k, int_dict[k], int_dict2[k], int_dict3[k])
   elif int_dict[k]==str(HIGH):
    print " |%-24s>|%10s| %10s| %-63s|" % (k, int_dict[k], int_dict2[k], int_dict3[k]) 
   else:
     print " |%-24s |%10s| %10s| %-63s|" % (k, int_dict[k], int_dict2[k], int_dict3[k])
 print " +--"+"-"*110+"-+"

def parse(lista):
	for line in lista:

		interface = re.search(r"^(.+) is up, line protocol is up", line)
		if interface:
			INT.append(interface.group(1))

		description = re.search(r"^  Description:(.+)", line)
		if description and INT:
			joc=INT[0]
			int_dict3[joc] = description.group(1)

		intrate = re.search(r"input rate (.+) bits/sec", line)
		if intrate and INT:
			joc=INT[0]
			rate=intrate.group(1)
			joc2=float(rate)/1000000
			joc3=str(joc2)
			int_dict[joc] = joc3

		outrate = re.search(r"output rate (.+) bits/sec", line)
		if outrate and INT:
			joc=INT[0]
			rate=outrate.group(1)
			joc2=float(rate)/1000000
			joc3=str(joc2)
			int_dict2[joc] = joc3
			INT.pop()

def hostname(lista):
        for line in lista:

                hostname = re.search('^(.+)#.*', line)
                if hostname:
                        return hostname.group(1)

def highval(lista):
	HIGH=0.0
	for line in lista.values():
		if float(line)>HIGH:
			HIGH=float(line)
	return HIGH	

class AllowAllKeys(pm.MissingHostKeyPolicy):
                def missing_host_key(self, client, hostname, key):
                        return

if __name__=='__main__':
	#pwd=getpass.getpass()
	os.system('clear')
	print''' Script to check traffic
	Script version is 1.12, local customer ID is CLARO PE
	Status:  * - 'more than 100Mbps', > - 'highest'
	'''	

	if len(sys.argv)==3:
		ip1=sys.argv[1]
		ip2=sys.argv[2]
		HOSTS=[ip1,ip2]
	elif len(sys.argv)==2:
                ip1=sys.argv[1]
                HOSTS=[ip1]
	else:
		ip1='172.22.152.4'
		ip2='172.22.152.5'
		HOSTS=[ip1,ip2]
	
	USER = 'E702778'
        PASSWORD = 'Lima2017+'

	for device in HOSTS:
		try:
			client = pm.SSHClient()
                        client.load_system_host_keys()
                        #client.load_host_keys(os.path.expanduser('~/.ssh/known_hosts'))
                        client.set_missing_host_key_policy(AllowAllKeys())
                        client.connect(device, username=USER, password=PASSWORD)

                        channel = client.invoke_shell()
                        stdin = channel.makefile('wb')
                        stdout = channel.makefile('rb')

                        stdin.write('''
                                terminal length 0
                                sh interfaces | i Port-channel|Gigabit|Ten|Description|rate
                                exit
                                ''')
                        output_data = stdout.read()	
			str(output_data)
			lista=output_data.splitlines()
		except Exception as e:
			print 'Connection Error to host ',device
			print e
			print type(e).__name__
			continue
		try:
			int_dict = {}
			int_dict2 = {}
			int_dict3 = {}
			INT=[]
			lista2=[]
			lista3=[]
			HOSTNAME=hostname(lista)
			parse(lista)
			HIGH=highval(int_dict)
			show(int_dict,int_dict2,int_dict3)
		except Exception as e:
			print 'Error in parse show function ',e
	
	raw_input('\nPress Enter to quit.')

