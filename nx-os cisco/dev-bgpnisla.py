#!/isan/bin/python

import cisco
import re

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




def hostname(lista):
        for line in lista:
                hostname = re.search('^(.+)#.*', line)
                if hostname:
                        return hostname.group(1)

print '''       Colocar IP como argumentos
        python script.py <nIsladeServiciosPolo1> <nIsladeServiciosVillaSalvador>

        '''

output_data = cli('show ip bgp neighbors')
str(output_data)
lista=output_data.splitlines()
int_dict = {}; int_dict2 = {}; int_dict3 = {}; int_dict4 = {}
int_dict5 = {}; int_dict6 = {}; INT=[]
HOSTNAME='nIsladeServiciosPolo1'
#print output_data
#HOSTNAME=hostname(lista)
parse(lista)
show(int_dict,int_dict2,int_dict3,int_dict6,int_dict5)

