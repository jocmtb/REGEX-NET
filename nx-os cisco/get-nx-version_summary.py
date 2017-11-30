#!/isan/bin/python

import cisco
import re


result=cli('show version')

for line in result.split('\n'):
        jimmy=re.search('.*version.*',line)
        if jimmy:
                if line.split()[1]=='version':
                        print '+-'+'-'*25+'-+'
                        print "|{0:12} | {1:12}|".format(line.split()[0],line.split()[2])
print '+-'+'-'*25+'-+'