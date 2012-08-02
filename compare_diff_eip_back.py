DataSource1 = "./qemu31/qemu31_rm_int.log"
#DataSource2 = "./qemu33/qemu33_rm_int.log"
DataSource2 = "./qemu30/qemu30_cpu_part_0"

f1 = open(DataSource1, "r")
text1 = f1.readlines()
f1.close()

f2 = open(DataSource2, "r")
text2 = f2.readlines()
f2.close()

# From where
count1 = 20743 - 1

count2 = 20812 - 1

while(1):
    if text1[count1].split()[1] == text2[count2].split()[1]:
        count1 -= 1
        count2 -= 1
    else:
        print count1 + 1
        print count2 + 1
        print
        print text1[count1]
        print text2[count2]
        break

