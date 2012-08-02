DataSource = "./qemu37/qemu37_ins_total"

f = open(DataSource, "r")
text = f.readlines()
f.close()

f2 = open('./qemu37/only_instr37.log','w')

for line in xrange(len(text)):
    if text[line].startswith('#'):
        f2.write(str(line)+'  '+text[line])
        
f2.close()
