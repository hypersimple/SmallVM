#!/usr/bin/env python

import string
import re



DataSource = "/home/cy/qemu12.log"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array
line = 0
eax = 0
slice_set=[]
#slicecount = 0
i = 0

for line in range(0,10000000):
    if text[line].find('# movi_i32 tmp4,$0x7e42b415') != -1:
        
        for subline in range(0,1000):
            if text[line-subline].find('OP') == -1:
                slice_set.append(text[line-subline])
            else: 
                slice_set.append('-------------------------------------------------')
                break
                #slicecount = slicecount + 1


for i in range(0,100):
    print slice_set[i],    #If put a "," at the end, it won't print \n
#print 1
#print 2

'''
print text[0]
count = 0

p = re.compile('CR3')

tmp = p.search('CR34444CR3').span()

print tmp
'''

'''
for eachline in text:

    temp = eachline.find("CR3")
    if temp != -1:
        count = count + 1
print count
'''
#print text.find("CR3")
