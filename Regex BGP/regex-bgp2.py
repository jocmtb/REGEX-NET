'''
Script en Python 2,7
Jose Costa
Parser para BGP
'''

import re

print """

  -------------------------------------
  |  Script para parsear tabla BGP  |
  -------------------------------------

 BGP Prefixes
 ----------------
"""


f = open ('bgp.txt','r')
f2 = open ('bgp2.txt','r')
lista=[]
for line in f.readlines():
	search=re.search(r'(^.*[0-9])*\.([0-9])*\.([0-9])*\.([0-9])*.*[i,?]$',line)
	#print match.group(0)
	if search:
		field=line.split()
		if field[1].count('/')==1:
			string=field[1]
			while string[0].isdigit()==False:
				string=string[1:]
			lista.append(string)
		elif len(field[0])>10:
			string=field[0]
			while string[0].isdigit()==False:
				string=string[1:]
			lista.append(string)
		#print " {0:>18}".format(string)
print '\n Numero de Prefijos: '
print len(lista)

lista2=[]
for line in f2.readlines():
	search=re.search(r'(^.*[0-9])*\.([0-9])*\.([0-9])*\.([0-9])*.*[i,?]$',line)
	#print match.group(0)
	if search:
		field2=line.split()
		if field2[1].count('/')==1:
			string2=field2[1]
			while string2[0].isdigit()==False:
				string2=string2[1:]
			lista2.append(string2)
		elif len(field2[0])>10:
			string2=field2[0]
			while string2[0].isdigit()==False:
				string2=string2[1:]
			lista2.append(string2)
		#print " {0:>18}".format(field[1])
print '\n Numero de Prefijos: '
print len(lista2)

f.close()
f2.close()

print
for x in lista:
	if x not in lista2:
		print x

print
for x in lista2:
	if x not in lista:
		print x

raw_input('Press Enter to quit.')
