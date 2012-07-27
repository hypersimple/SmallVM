DataSource = "./qemu30/qemu30_slicing_multi6.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()

NUMBER_START = 3   # 2 or 3

f3 = open("./qemu30/qemu30_slicing_multi6_tmp2.log","w")

for pline in text:
    try:
        tmp2 = pline.split()[NUMBER_START].split(',')[1]
        if tmp2.startswith('*'):
            pline = pline.replace(tmp2,'tmp2')
    except:
        pass
    f3.write(pline)

f3.close()
