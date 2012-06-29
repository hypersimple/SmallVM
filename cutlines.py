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

start_line = 11950000 #-50
end_line = 11962427  #+5


DataSource = "qemu17_de_duplicate.log"

f2 = open ("qemu17_cutlines.log", "w")


# Rewrite, not append file

#result = []
count = 0

for line in open(DataSource):
    if count == end_line:
        break
    elif count >= start_line - 1:
        f2.write(line)
    count += 1



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
