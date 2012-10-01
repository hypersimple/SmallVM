from mapping import *

DataSource = "./qemu019_5/qemu019_5_ins.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()


BlockSource = "./qemu019_5/qemu019_5_slicing_cut_block.log"

f = open(BlockSource, "r")
text2 = f.readlines()
f.close()


index = mapping(text)
#index2 = backmapping(text)

text3 = []

for line in text2:
    tmp = index[int(line)]   #tuple
    text3.append(text[tmp[0]-1])
    for i in xrange(tmp[0],tmp[1]+1):
        text3.append(text[i])



f2 = open("./qemu019_5/qemu019_5_subset2.log","w")
for line in text3:
    f2.write(line)
f2.close()



#print index2[17349740]

#print index[6]
