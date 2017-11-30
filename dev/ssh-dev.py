'''
Paramiko usando SSHClient method
                invoke_shell()
'''

import sys
#sys.stderr = open('/dev/null')       # Silence silly warnings from paramiko
import paramiko as pm
#sys.stderr = sys.__stderr__
import os
import datetime


if __name__=='__main__':
	class AllowAllKeys(pm.MissingHostKeyPolicy):
		def missing_host_key(self, client, hostname, key):
			return
	HOSTS=['172.19.204.1','172.19.204.2','172.19.216.1','172.19.216.2'
	,'172.19.216.3','192.168.252.100' ,'10.128.9.158' ,'192.168.252.59','192.168.252.81'
	,'10.38.0.4' ,'10.38.0.132' ,'172.26.9.3'  
	,'172.26.9.4' ,'172.17.22.22','172.19.212.81','172.19.212.82'      
	,'172.19.212.83','172.19.212.84','172.19.212.85','172.19.212.86'
	,'172.19.212.87','172.22.152.4','172.22.152.5','172.22.153.4'   
	,'172.22.153.5','172.22.154.4','172.22.154.5','172.22.155.4'   
	,'172.22.155.5','172.22.156.4' ,'172.22.156.5'    
	,'172.22.157.4','172.22.157.5','172.22.158.4','172.22.158.5'     
	,'172.19.4.6','172.19.4.7','10.244.42.5','10.244.35.5','172.22.5.5'
	,'172.22.28.254','172.22.27.254','172.22.11.252','172.22.11.253'
	,'172.22.12.252','172.22.12.253','172.22.16.98'
	,'172.22.16.66','172.22.26.9','172.22.26.8','172.22.26.7'
	,'172.22.26.6','172.22.26.5','172.22.24.6','172.22.23.8','172.22.21.5','172.22.20.6','172.22.20.5'
	,'10.244.45.2','172.22.19.6','172.22.19.5','172.22.17.6'
	,'172.22.17.5','172.22.32.6','172.22.32.5','172.22.34.5','172.22.40.5'
	,'172.22.41.5','172.22.52.6','172.22.52.5'
	,'172.22.77.5','172.22.31.5','172.22.68.5','172.22.70.5','172.22.58.5','172.22.56.5'
	,'172.22.25.5','172.22.78.5','172.22.75.5'
	,'172.22.62.6','172.22.62.5','172.22.49.5','172.22.69.5','172.22.99.194','172.22.89.5'
	,'172.22.87.5','10.244.22.247','10.244.22.248','10.244.22.242' ]		
	HOST = '172.22.152.4'
	USER = 'E702778'
	PASSWORD = 'Lima2017!'
	x = datetime.datetime.now()
	fecha_actual = ("%s-%s-%s_%s-%s" % (x.year, x.month, x.day,x.hour,x.minute) )
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
				show version
				show running-config
				show inventory
				exit
				''')
			output_data = stdout.read()
			#print output_data
			file=open(device+'_'+fecha_actual+'.txt','w')
			file.write(output_data)
			file.close()

			stdout.close(); stdin.close(); client.close()
			print "Device OK "+device
		except Exception as e:
			print "Error in device"+device
			print"  >Error message: "+str(e)
	raw_input("Press any key to close..")
