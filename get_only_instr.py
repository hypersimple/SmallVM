DataSource = "./qemu30/qemu30_ins_total4"

f = open(DataSource, "r")
text = f.readlines()
f.close()

f2 = open('./qemu30/only_instr30.log','w')

for line in xrange(len(text)):
    if text[line].startswith('#'):
        f2.write(str(line)+'  '+text[line])
        
f2.close()
