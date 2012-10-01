from mapping import *

DataSource = "./qemu019_5/qemu019_5_ins2.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()



index = {}
index = backmapping(text)


index2 = mapping(text)

#print index[245]
print index[17349740]

#print index2[6]
