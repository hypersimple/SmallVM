DataSource = "./qemu38/qemu38_slicing_multi.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()


a =[]

for line in text:
    tmp = line.split()[2]
    a.append(tmp)
    
a = list(set(a))

for i in a:
    print i
    
