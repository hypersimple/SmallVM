#!/usr/bin/env python

#import string
#import sys
#import re

'''
def read_in_chunks(file_object, chunk_size=1024):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


f = open('really_big_file.dat')
for piece in read_in_chunks(f):
    process_data(piece)
'''


DataSource0 = "./qemu25/qemu25_ins_0"
DataSource1 = "./qemu25/qemu25_ins_1"
DataSource2 = "./qemu25/qemu25_ins_2"
DataSource3 = "./qemu25/qemu25_ins_3"
DataSource4 = "./qemu25/qemu25_ins_4"
DataSource5 = "./qemu25/qemu25_ins_5"
DataSource6 = "./qemu25/qemu25_ins_6"
DataSource7 = "./qemu25/qemu25_ins_7"
DataSource8 = "./qemu25/qemu25_ins_8"


f2 = open ("./qemu25/qemu25_ins_total", "w")


# Rewrite, not append file

#result = []

for i in xrange(0,8+1):
    print i
    for line in open("./qemu25/qemu25_ins_"+str(i)):
        f2.write(line)


f2.close()


#text = f.readlines(1)  #Text is a string array

'''
#result = []
line = 0
#count = 0
start_line = 1
end_line = 12 #3697461


for line in range(start_line-1, end_line):
    result.append(text[line]);
    #count = count + 1;
    
f2 = open ("/home/cy/project/test7", "w")
f2.writelines(result)
#print >> f2, result,
'''
