DataSource = "qemu019_de_duplicate.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()

dict1 = {}

for line in text:
    try:
        if line.startswith('0x'):
            address1 = line.split()[0].split('x')[1].lstrip('0')
            address = ('0x' + address1).rstrip(':')
            dict1[address] = 1
    except:
        #raise
        #pass
        print line
        raise


#-------------------------------------------    
'''
DataSource = "../qemu25_in_asm.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()

for line in text:
    try:
        if line.startswith('0x'):
            address1 = line.split()[0].split('x')[1].lstrip('0')
            address = ('0x' + address1).rstrip(':')
            dict1[address] = 1
    except:
        #raise
        #pass
        print line
        raise
#---------------------------------------------------
'''
DataSource = "./qemu019/qemu019_ins_total"

f = open(DataSource, "r")
text = f.readlines()
f.close()


for i in xrange(len(text)):
    if text[i].startswith(' ---- 0x'):
        address = text[i].split()[1]
        if address in dict1:
            pass
        else:
            print text[i]
