#DataSource = "./qemu30/qemu30_slicing_multi7.log"
#DataSource = "./qemu37/only_instr37.log"
DataSource = "./qemu38/qemu38_ins_total3"


f = open(DataSource, "r")
text = f.readlines()
f.close()

NUMBER_START = 2   # 2 or 3

#f3 = open("./qemu30/qemu30_slicing_multi7_tmp2.log","w")
#f3 = open("./qemu37/only_instr37_tmp2.log","w")
f3 = open("./qemu38/qemu38_ins_tmp2.log","w")

for pline in text:
    try:
        tmp2 = pline.split()[NUMBER_START].split(',')[1]
        if tmp2.startswith('*'):
            pline = pline.replace(tmp2,'tmp2')
    except:
        pass
    f3.write(pline)

f3.close()
