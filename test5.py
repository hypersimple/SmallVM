import linecache


#fp = open("/home/cy/project/test5.txt")
fp = open("/home/cy/qemu_all_op.log")
#DataWarehouse = "/home/cy/project/test5.txt"
DataWarehouse = "/home/cy/qemu_all_op.log"

text1 = []
FILE_LINE_SIZE = 23 #Real Line Size
total_count = 1
count = 0
'''
while (total_count <= FILE_LINE_SIZE):
    line = linecache.getline(DataWarehouse, total_count)
    if line and count <= 5:
        text1.append(line)
        count += 1
        total_count += 1
        continue
    elif line != '# end \n':
        text1.append(line)
        total_count += 1
        continue
    elif line == '# end \n':
        text1.append(line)
        total_count += 1
        count = 0
        #buf = fetch(text,text1)
        #for line2 in xrange(0,len(buf)):
            #f2.write(buf[line2])
        text1 = []
        #break
'''       
'''        
for line in open(DataWarehouse):
    if line and count <= 5:
        print line
'''


for i, line in enumerate(fp):
    print i,line
