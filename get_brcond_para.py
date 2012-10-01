# get the first two parameters of brcond in the text for slicing
from mapping import *

# the diff result is the real line number, but here the line begins from 0
def get_brcond_para(lines,text,indexall):
    for j in lines:
        line = int(j) - 1
        line2 = indexall[line][1]
        for i in xrange(1000):
            if text[line2-i].startswith('# brcond'):
                para1 = text[line2-i].split()[2].split(',')[0]
                para2 = text[line2-i].split()[2].split(',')[1]
                
                #print out the result, the line begins at 0
                print line2-i,para1
                print line2-i,para2
                
                break
            elif text[line2-i].startswith('@'):
                break
                print 'ERROR!!!'


SourceFile = "./qemu019_5/qemu019_5_ins2.log"
BrcondFile = "./qemu019_5/diff_line_5.txt"

f0 = open(SourceFile)
text = f0.readlines()
f0.close()

f1 = open(BrcondFile)
lines = f1.readlines()
f1.close()

indexall = mapping(text)

get_brcond_para(lines,text,indexall)
