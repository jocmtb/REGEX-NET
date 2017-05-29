'''
Script en Python 2,7
Jose Costa
Parser para Tabla de MAC
'''

import re

print """

  -------------------------------------
  |  Script para parsear tabla MAC   |
  -------------------------------------

 MAC aDdresses
 ----------------
"""


f = open ('mac1.txt','r')
f2 = open ('mac2.txt','r')
lista=[]
for line in f.readlines():
	search=re.search(r'dynamic',line)
	#print match.group(0)
	if search:
		field=line.split()
		string=field[1]+" "+field[2]+" "+field[7]
		lista.append(string)
		#print " {0:>18}".format(string)
print '\n Numero de MACs: '
print len(lista)

lista2=[]
for line in f2.readlines():
	search=re.search(r'dynamic',line)
	#print match.group(0)
	if search:
		field2=line.split()
		string2=field2[1]+" "+field2[2]+" "+field2[7]
		lista2.append(string2)
		#print " {0:>18}".format(string2)
print '\n Numero de MACs: '
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