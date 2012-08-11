#DataSource1 = "./qemu31/qemu31_rm_int.log"
#DataSource2 = "./qemu32/qemu32_rm_int.log"


#DataSource1 = "./qemu37/run_result_37_2_a"
#DataSource2 = "./qemu37/only_instr37.log"


#DataSource1 = "./qemu38/result_38_4_a"
DataSource1 = "./qemu40/qemu40_ins_total"
DataSource2 = "./qemu38/qemu38_ins_total3"


f1 = open(DataSource1, "r")
text1 = f1.readlines()
f1.close()

f2 = open(DataSource2, "r")
text2 = f2.readlines()
f2.close()

#count = 0
count2 = count1 = 1 -1
#count2 = count1
#count2 = 19136 -1

while(1):
    if text1[count1] == text2[count2]:
        count1 += 1
        count2 += 1
    else:
        try:
            if text1[count1].split()[2].split(',')[1] == 'tmp2':
                count1 += 1
                count2 += 1
                continue
        except:
            pass
        print count1 + 1
        print count2 + 1
        print
        print text1[count1]
        print text2[count2]
        break

