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
        PASSWORD = 'Lima2017#'

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
                                show logging | i change
                                exit
                                ''')
                        output_data = stdout.read()	
			print str(output_data)
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
	raw_input('Press Enter to quit.')

