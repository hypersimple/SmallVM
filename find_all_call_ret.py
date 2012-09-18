DataSource = "qemu019_de_duplicate.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()


list1 = []
list2 = set(list1)

for line in text:
    if 'call' in line:
        list2.add(line.split()[1])
        if 'movi_i64' in line:
            print line
    if 'ret' in line:
        list2.add(line.split()[1])
        if 'movi_i64' in line:
            print line
        
print list2
