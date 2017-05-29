'''
Script en Python 2,7
Jose Costa
Parser para BGP Sessions
'''

import re

print """

  -------------------------------------
  |  Script para parsear BGP Sessions |
  -------------------------------------

 BGP Neighbors Sessions
 ----------------
"""
def show(lista,lista2):
	print
	print "{0:15} {1:6} {2:10}".format('Neighbor','AS','State')
	print "{0:15} {1:6} {2:10}".format('---------','---','------')
	for x in lista:
		if x not in lista2:
			cadena=x.split()
			print "{0:15} {1:6} {2:10}".format(cadena[0],cadena[1],cadena[2])

f = open ('bgpsum1.txt','r')
f2 = open ('bgpsum2.txt','r')
lista=[]
for line in f.readlines():
	search=re.search(r'(^[0-9])*\.([0-9])*\.([0-9])*\.([0-9])*(.*)4',line)
	#print match.group(0)
	if search and len(line.split())==10:
		field=line.split()
		string=field[0]+" "+field[2]+" "+field[9]
		lista.append(string)
		#print " {0:>18}".format(string)
print '\n Numero de BGP Sessions: '
print " {0:>20} ".format(len(lista))

lista2=[]
for line in f2.readlines():
	search=re.search(r'(^[0-9])*\.([0-9])*\.([0-9])*\.([0-9])*(.*)4',line)
	#print match.group(0)
	if search and len(line.split())==10:
		field2=line.split()
		string2=field2[0]+" "+field2[2]+" "+field2[9]
		lista2.append(string2)
		#print " {0:>18}".format(string2)
print '\n Numero de BGP Sessions: '
print " {0:>20} ".format(len(lista2))

f.close()
f2.close()

show(lista,lista2)
show(lista2,lista)

print(" ")
raw_input('Press Enter to quit.')