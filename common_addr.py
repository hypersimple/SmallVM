#DataSource = "./qemu019/slicing019_2.txt"
DataSource = "./qemu019/019_slicing3_http.txt"


f = open(DataSource, "r")
text1 = f.readlines()
f.close()

DataSource = "./qemu019_2/019_2_slicing3.txt"

f = open(DataSource, "r")
text2 = f.readlines()
f.close()

list1=[]
set1 = set(list1)

for line in text1:
    if line.startswith('['):
        temp = line.split(',')
        for i in temp:
            if i.startswith(" '*"):
                c=i.rstrip('\n')
                c=c.rstrip(']')
                set1.add(c)

    
list2=[]
set2 = set(list2)

for line2 in text2:
    if line2.startswith('['):
        temp = line2.split(',')
        for i in temp:
            if i.startswith(" '*"):
                c=i.rstrip('\n')
                c=c.rstrip(']')
                set2.add(c)

                
#print set1

set3 = set1 & set2

for i in set3:
    print i
    
#print set3
