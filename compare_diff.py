#DataSource1 = "./qemu31/qemu31_rm_int.log"
#DataSource2 = "./qemu32/qemu32_rm_int.log"


DataSource1 = "./qemu37/run_result_37_2_a"
DataSource2 = "./qemu37/only_instr37.log"


f1 = open(DataSource1, "r")
text1 = f1.readlines()
f1.close()

f2 = open(DataSource2, "r")
text2 = f2.readlines()
f2.close()

#count = 0
count1 = 9927 -1
count2 = 9927 -1

while(1):
    if text1[count1] == text2[count2]:
        count1 += 1
        count2 += 1
    else:
        print count1 + 1
        print count2 + 1
        print
        print text1[count1]
        print text2[count2]
        break

