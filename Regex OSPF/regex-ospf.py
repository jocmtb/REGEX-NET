'''
Script en Python 2,7
Jose Costa
Parser para OSPF Database
'''

import re

print """

  -------------------------------------
  |  Script para parsear OSFP DataBase |
  -------------------------------------

 OSFP LInk States
 ----------------
"""


f = open ('ospf1.txt','r')
f2 = open ('ospf2.txt','r')
lista=[]
for line in f.readlines():
	match=re.search(r'Link States',line)
	if match:
		lista.append(line.split()[0])
	search=re.search(r'^([0-9])*\.([0-9])*\.([0-9])*\.([0-9])*',line)
	#print match.group(0)
	if search:
		field=line.split()
		string=field[0]+" "+field[1]
		lista.append(string)
		#print " {0:>18}".format(string)
print "\n Numero de Link States:  {0:>10} ".format(len(lista)-4)

f.close()
index=[]

for i,j in enumerate(lista):
	if j=='Router':
		index.append(i)
	if j=='Summary':
		index.append(i)
	if j=='Type-5':
		index.append(i)
#print lista[0:10]
index.append(len(lista))
#print index	
print "Router LSA: "+str(int(index[1])-int(index[0])-1)+" Summary LSA: "+str(int(index[2])-int(index[1])-1)
print "Sum ASBR LSA: "+str(int(index[3])-int(index[2])-1)+" Type-5 LSA: "+str(int(index[4])-int(index[3])-1)
print

lista2=[]
for line in f2.readlines():
	match=re.search(r'Link States',line)
	if match:
		lista2.append(line.split()[0])
	search=re.search(r'^([0-9])*\.([0-9])*\.([0-9])*\.([0-9])*',line)
	#print match.group(0)
	if search:
		field2=line.split()
		string2=field2[0]+" "+field2[1]
		lista2.append(string2)
		#print " {0:>18}".format(string2)
print "\n Numero de Link States:  {0:>10} ".format(len(lista2)-4)
print

f2.close()
index2=[]

for i,j in enumerate(lista2):
	if j=='Router':
		index2.append(i)
	if j=='Summary':
		index2.append(i)
	if j=='Type-5':
		index2.append(i)
#print lista[0:10]
index2.append(len(lista2))
#print index	
print "Router LSA: "+str(int(index2[1])-int(index2[0])-1)+" Summary LSA: "+str(int(index2[2])-int(index2[1])-1)
print "Sum ASBR LSA: "+str(int(index2[3])-int(index2[2])-1)+" Type-5 LSA: "+str(int(index2[4])-int(index2[3])-1)
print

for x in lista:
	if x not in lista2:
		print x

print
for x in lista2:
	if x not in lista:
		print x

raw_input('Press Enter to quit.')
