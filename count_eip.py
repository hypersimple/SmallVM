sourcefile = "/tmp/qemu.log"

f1 = open(sourcefile)
text = f1.readlines()
f1.close()

dict1 = {}

for line in text:
    if line.startswith("@"):
        dict1[ line.split()[1] ] = 1
        
print len(dict1)
