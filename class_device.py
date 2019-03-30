
import paramiko as pm
import time
import re
import socket
'''
Class to instance network objects
'''
class BaseDevice():
	def __init__(self,ip_address,comando='',user='jcostav',password='Lima2018$'):
		self.ip_address=ip_address
		self.hostname='unknown'
		self.portssh=22
		self.comand=comando+'\nexit\n'
		self.user=user
		self.buffer=''
		self.version='unknown'
		self.uptime='0 days'
		self.paging='terminal length 0\n'
		self.password=password
	def ssh_connect(self,comandos=[],):
		if isinstance(comandos,list):
			comandos.append(self.comand)
			comandosn=[x+'\n' for x in comandos]
		else:
			return 'method expects a list variable'
		try:
			client = pm.SSHClient()
			client.load_system_host_keys()
			client.set_missing_host_key_policy(pm.AutoAddPolicy())
			client.connect(self.ip_address, username=self.user, password=self.password)
			channel = client.invoke_shell()
			time.sleep(1)
			channel.settimeout(10)
			stdin = channel.makefile('wb')
			stdout = channel.makefile('rb')
			stdin.write(self.paging)
			for cmd in comandosn:
				stdin.write(cmd)
			output_data = stdout.read()
			self.buffer += output_data
			stdout.close(); stdin.close(); client.close()
			return output_data
		except Exception as e:
			return type(e).__name__, str(e)
	def validate_ip(self):
		ipv=self.ip_address.split('.')
		if len(ipv) != 4:
			return False
		for i,x in enumerate(ipv):
			if i==0 and int(x) > 0 and int(x) < 256:
				continue
			elif i>0 and int(x) >= 0 and int(x) < 256:
				continue
			else:
				return False
		return True
	def clear_buffer(self):
		self.buffer=''
	def ssh_active(self):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.settimeout(2)
		result = sock.connect_ex((self.ip_address,self.portssh))
		if result == 0:
			print self.ip_address+" : Port " + str(self.portssh)+ " is open"
		else:
			print "Port " + str(self.portssh)+ " is not open"
			print '  >> port CLOSED, connect_ex returned: '+str(result)
	def get_hostname(self,texto=''):
		if isinstance(texto,basestring) and texto!='':
			lista=texto.splitlines()
		elif texto=='' and self.buffer!='':
			lista=self.buffer.splitlines()
		elif texto=='' and self.buffer=='':
			return 'Buffer is empty.'
		else:
			return 'method expects a string variable'
		for line in lista:
			hostname = re.search('^(.+)#.*', line)
			if hostname:
				host1=hostname.group(1)
				if ':'in host1:
					host2=host1.split(':')
					self.hostname=host2[1]
					return host2[1]
				elif '@'in host1:
					host2=host1.split('@')
					self.hostname=host2[1]
					return host2[1]
	def __repr__(self):
		return 'device: {0}'.format(self.ip_address)
	def parse_bgpsum(self):
 		array1=[]
		for line in self.buffer.splitlines():
			bgpsum = re.search('^[0-9]+.[0-9]+.[0-9]+.[0-9]+\s+.*', line)
			if (bgpsum and len(line.split())==10):
				array1.append(line.split())
		return array1
	def parse_shipintbri(self):
                array1=[]
                for line in self.buffer.splitlines():
                        shipintbri = re.search('^(.+)\s+(.+)\s+([USD].+)\s+([USDP].+)\s+(.+)$', line)
                        if (shipintbri and len(line.split())==5):
                                array1.append(line.split())
                return array1
	def parse_shisisnei(self):
                array1=[]
                for line in self.buffer.splitlines():
                        shisisnei = re.search('^(.+)\s+(.+)\s+(.+)\s+(.+)\s+(.+)\s+(.+)\s+(.+)$', line)
                        if (shisisnei and len(line.split())==7):
                                array1.append(line.split())
                return array1
	def parse_shmplsnei(self):
                array1=[]
                for line in self.buffer.splitlines():
                        shmplsnei = re.search('^Peer LDP Identifier: (.+)$', line)
                        if shmplsnei:
                                ldpnei=shmplsnei.group(1)
                        shmplsnei2 = re.search('^\s+([GTPBS].+)$', line)
                        if (shmplsnei2 and len(line.split())==1):
                                array1.append([ldpnei,shmplsnei2.group(1)])
                return array1
	def parse_shplatform(self):
                array1=[]
                for line in self.buffer.splitlines():
                        shplatform = re.search('^(0/.+)\s+(.+)\s+.*$', line)
                        if (shplatform and len(line.split())>=4):
				bana=line.split()
                                array1.append([bana[0],bana[1],' '.join(bana[2:-1]),bana[-1]])
                return array1
	def get_version(self):
                for line in self.buffer.splitlines():
                        gversion = re.search('^Cisco IOS.*$', line)
                        if (gversion):
                                self.version=line
			guptime = re.search('^(.+)\s+uptime\s+is\s+(.+)$', line)
                        if (guptime):
                                self.uptime=guptime.group(2)

class DeviceLinux(BaseDevice):
	portssh=22
	def __init__(self,ip_address,comando='',user='root',password='t3l3f0n1c4!'):
		self.ip_address=ip_address
		self.portssh=22
		self.buffer=''
		self.hostname='None'
		self.comand=comando+'\nexit\n'
		self.user=user
		self.paging='date\n'
		self.password=password
	def get_hostname(self,texto=''):
		if isinstance(texto,basestring) and texto!='':
			lista=texto.splitlines()
		elif texto=='' and self.buffer!='':
			lista=self.buffer.splitlines()
		elif texto=='' and self.buffer=='':
			return 'Buffer is empty.'
		else:
			return 'method expects a string variable'
		for line in lista:
			hostname = re.search('^(.+)\s+(.+)#.*', line)
			if hostname:
				host1=hostname.group(1)
				if '@'in host1:
					host2=host1.split('@')
					self.hostname=host2[1]
					return host2[1]
	def __repr__(self):
		return 'device: {0}'.format(self.ip_address)

if __name__=='__main__':
	time1=time.time()
	router1=BaseDevice('200.37.0.239','date','root','t3l3f0n1c4!')
	logs1=router1.ssh_connect()
	print logs1
	time2=time.time()-time1
	print 'Elapsed Time: ',time2
