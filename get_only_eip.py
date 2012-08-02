DataSource1 = "./qemu33/qemu33_rm_int.log"
destfile = "./qemu33/qemu33_eip.log"

f1 = open(DataSource1, "r")
text = f1.readlines()
f1.close()


for count in xrange(len(text)):
    text[count] = text[count].split()[1]+'\n'
    count += 1


f2 = open(destfile,"w")
for count2 in xrange(0, len(text)):
    f2.write(text[count2])
f2.close()
