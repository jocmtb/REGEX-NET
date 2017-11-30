'''
Jose Costa
Check interface input/output Errors
04 Octubre 2017
Claro Peru
'''
from pprint import pprint
import re
import paramiko as pm
import sys

def show(int_dict,int_dict2,int_dict3,int_dict4,int_dict5):
 print "+--"+'-'*118+"--+"
 print "| %28s | %28s | %28s | %27s |" % (HOSTNAME,HOSTNAME,HOSTNAME,HOSTNAME) 	
 print "+--"+'-'*118+"--+"
 print "|{0:24} |{1:12} |{2:12} |{3:12} |{4:12} |{5:40}|".format('Interface','InputErrors','OutputErrors','CRC','drop','Description')
 print "+--"+'-'*118+"--+"
 Ks=list(int_dict.keys())
 Ks.sort()
 for k in Ks:
  if(float(int_dict[k])>1 or float(int_dict2[k])>1):
   if (float(int_dict[k])>1000 or float(int_dict2[k])>1000):
    print "|%-24s*|%12s| %12s| %12s| %12s| %-40s|" % (k, int_dict[k], int_dict2[k],int_dict4[k] , int_dict5[k], int_dict3[k])
   else:
    print "|%-24s |%12s| %12s| %12s |%12s| %-40s|" % (k, int_dict[k], int_dict2[k],int_dict4[k] , int_dict5[k], int_dict3[k])
 print "+--"+'-'*118+"--+"

def parse(lista):
	for line in lista:

		interface = re.search(r"^(.+) is up, line protocol is up", line)
		if interface:
			INT.append(interface.group(1))

		description = re.search(r"^  Description:(.+)", line)
		if description and INT:
			joc=INT[0]
			int_dict3[joc] = description.group(1)
		
		outdrop = re.search('.*; Total output drops: (.+)$', line)
                if outdrop and INT:
                        joc=INT[0]
                        int_dict5[joc] = outdrop.group(1)		

		intrate = re.search(r"^    (.+) input error", line)
		if intrate and INT:
			joc=INT[0]
			error=intrate.group(1)
			int_dict[joc] = error

		outrate = re.search(r"^    (.+) output error", line)
		if outrate and INT:
			joc=INT[0]
			error=outrate.group(1)
			int_dict2[joc] = error
			INT.pop()
			
		crc = re.search(r", (.+) CRC,", line)
		if crc and INT:
			joc=INT[0]
			error2=crc.group(1)
			int_dict4[joc] = error2

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
	python script.py <IP1> <IP2>
	
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
                                sh interfaces | i Port-channel|Gigabit|error|Ten|Description|drop
                                exit
                                ''')
                        output_data = stdout.read()	
			str(output_data)
			lista=output_data.splitlines()

			int_dict = {}
			int_dict2 = {}
			int_dict3 = {}
			int_dict4 = {}
			int_dict5 = {}
			INT=[]

		except Exception as e:
			print 'Connection Error to host ',device
			print "Type exception: ",type(e).__name__
                        print"  >Error message: "+str(e)
			continue
		try:
			HOSTNAME=hostname(lista)
			parse(lista)
			show(int_dict,int_dict2,int_dict3,int_dict4,int_dict5)
		except Exception as e:
                        print 'Aca esta mal mijo '
			print int_dict5
			#print int_dict4
			#print int_dict3	

	raw_input('Press Enter to quit.')

