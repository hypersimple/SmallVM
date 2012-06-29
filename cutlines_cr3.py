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
'''
start_line = 25338314 #-50
end_line = 25366055  #+5


DataSource = "/home/cy/project/qemu13_replace_OP.log"

f2 = open ("/home/cy/project/qemu13_cutlines.log", "w")
'''
'''
    with open(filename) as file_:
        for line in file_:
            do_something(line)
'''
# Rewrite, not append file

def cr3(cpu_string):
    return cpu_string.split()[2].split('=')[1]

def cutlines_cr3(sourcefile,destfile,line):

    f1 = open(sourcefile)
    text = f1.readlines()
    f1.close()
    
    cr3_tmp = cr3(text[line-1])
    for subline in xrange(1,len(text)):
        if text[line-1-subline].startswith('@'):
            if cr3(text[line-1-subline]) != cr3_tmp:
                line_result = line-1-subline
                break
            else:
                pass
    start_line = line_result
    end_line = line-1
    
    count = 0

    f2 = open (destfile, "w")
    for line2 in text:
        if count == end_line+1:
            break
        elif count >= start_line:
            f2.write(line2)
        count += 1
    f2.close()


origin = "qemu17.log"

sourcefile_name = origin.split('.')[0]

sourcefile = sourcefile_name+'_de_duplicate.log'
destfile = sourcefile_name+'_cutlines_cr3.log'

cutlines_cr3(sourcefile,destfile,11962427)


