#!/usr/bin/env python
# -*- coding: utf-8 -*-

tmp = []
for i in xrange(0,50):
    tmp.append('1')
    
print tmp[0]


a="%x"%(int('a',16)+int('1',16))
print a

tmp_string='tmp12'
print int(tmp_string.split('tmp')[1])

# 函数传值测试，传列表名相当与传递指针
examplelist=[]
examplelist.append(1)


def change(example):
    example[0] = 2
    
change(examplelist)
print examplelist[0]

print 3%4

print "Trace 0x449810e0 [77f18a1e]\n".split()[2].split('[')[1].split(']')[0]

aa= '00a4'
print aa.lstrip('0')
print aa

for i in xrange(-1,2):
    print i
    
    
DataSource = "/home/cy/project/test4.txt"
DataWarehouse = "/home/cy/qemu_all_op.log"
#DataWarehouse = "/home/cy/project/test5.txt"
DataDest = "/home/cy/project/test6.txt"

f = open(DataSource, "r")
text = f.readlines(1)  #Text is a string array
print text
