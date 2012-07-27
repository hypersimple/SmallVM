DataSource1 = "./qemu30/result30_7_9.log"
DataSource2 = "./qemu30/only_instr30.log"

f1 = open(DataSource1, "r")
text1 = f1.readlines()
f1.close()

f2 = open(DataSource2, "r")
text2 = f2.readlines()
f2.close()

count = 0
while(1):
    if text1[count] == text2[count]:
        count += 1
    else:
        print count + 1
        print
        print text1[count]
        print text2[count]
        break

