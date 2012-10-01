DataSource1 = "qemu019_5/qemu019_5_rm_int.log"
destfile = "qemu019_5/qemu019_5_eip.log"

f1 = open(DataSource1, "r")
text = f1.readlines()
f1.close()


text2 = []

for count in xrange(len(text)):
    if text[count].startswith('@'):
        text2.append(text[count].split()[1]+'\n')
        count += 1
    else:
        print 'INT',count+1


f2 = open(destfile,"w")
for count2 in xrange(0, len(text2)):
    f2.write(text2[count2])
f2.close()
