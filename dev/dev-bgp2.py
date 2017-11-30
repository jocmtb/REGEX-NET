'''
Jose Costa
Check BGP sessions hacia BRs
06 Octubre 2017
Claro Peru
'''
from pprint import pprint
import re
import paramiko as pm
import telnetlib
import sys

def show(int_dict,int_dict2,int_dict3,int_dict4,int_dict5):
 print "+--"+'-'*118+"--+"
 print "| %38s | %38s | %38s|" % (HOSTNAME,HOSTNAME,HOSTNAME) 	
 print "+--"+'-'*118+"--+"
 print "|{0:16} |{1:12} |{2:10} |{3:10} |{4:10} |{5:55}|".format('BGP Neighbor','State','Up for','PfxReceived','SentPaths','Description')
 print "+--"+'-'*118+"--+"
 Ks=list(int_dict.keys())
 Ks.sort()
 for k in Ks:
  print "|%-16s |%12s| %10s| %10s |%10s| %-55s|" % (k,int_dict[k],int_dict2[k],int_dict3[k],int_dict4[k],int_dict5[k])
 print "+--"+'-'*118+"--+"

def parse(lista):
	for line in lista:

		bgpnei = re.search('^BGP neighbor is (.+),  remote AS (.+),.*', line)
		if bgpnei:
			INT.append(bgpnei.group(1))
			int_dict5[INT[0]] ='None'

		description = re.search('^  Description: (.+)', line)
		if description and INT:
			joc=INT[0]
			int_dict5[joc] = description.group(1)
		
		state = re.search('BGP state = (.+), (.+) for (.+)', line)
                if state and INT:
                        joc=INT[0]
                        int_dict[joc] = state.group(1)
			int_dict2[joc] = state.group(3)[:9]		

		prefixes = re.search('^  (.+) accepted paths consume (.+) bytes of memory', line)
		if prefixes and INT:
			joc=INT[0]
			int_dict3[joc] = prefixes.group(1)
			int_dict4[joc] = prefixes.group(2)
		

		paths = re.search('^  (.+) sent paths', line)
                if paths and INT:
                        joc=INT[0]
                        int_dict6[joc] = paths.group(1)
                        INT.pop()


def hostname(lista):
        for line in lista:
                hostname = re.search('^(.+)#.*', line)
                if hostname:
                        return hostname.group(1)
		
class AllowAllKeys(pm.MissingHostKeyPolicy):
                def missing_host_key(self, client, hostname, key):
                        return

if __name__=='__main__':
	print '''	Colocar IP como argumentos
	python script.py <nIsladeServiciosPolo1> <nIsladeServiciosVillaSalvador>
	
	'''
	if len(sys.argv)==3:
		ip1=sys.argv[1]
		ip2=sys.argv[2]
		HOSTS=[ip1,ip2]
	elif len(sys.argv)==2:
		ip1=sys.argv[1]
		HOSTS=[ip1]
	else:
		ip1='10.235.0.56'
		ip2='10.235.0.57'
		HOSTS=[ip1,ip2]
	
	USER = 'E702778'
        PASSWORD = 'Lima2017+'

	for device in HOSTS:
		try:
                        telshell = telnetlib.Telnet(device)
                        telshell.read_until("login: ")
                        telshell.write((USER + "\n").encode('ascii'))
                        telshell.read_until("assword: ")
                        telshell.write((PASSWORD + "\n").encode('ascii'))
                        telshell.write("terminal len 0\n")
                        telshell.write("show ip bgp neighbors\n")
                        telshell.write("exit\n")
                        print "# Getting info from device: ",device
                        output_data = telshell.read_until("^exit\n")
			str(output_data)
			lista=output_data.splitlines()
			int_dict = {};int_dict2 = {};int_dict3 = {}; int_dict4 = {}
			int_dict5 = {};int_dict6 = {};INT=[]
		except Exception as e:
			print 'Connection Error to host ',device
			print "Type exception: ",type(e).__name__
                        print"  >Error message: "+str(e)
			continue
		try:
			HOSTNAME=hostname(lista)
			parse(lista)
			show(int_dict,int_dict2,int_dict3,int_dict6,int_dict5)
		except Exception as e:
                        print "Type exception: ",type(e).__name__
                        print"  >Error message: "+str(e)

	raw_input('Press Enter to quit.')

