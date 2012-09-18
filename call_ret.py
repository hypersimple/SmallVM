DataSource = "qemu019_2_de_duplicate.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()

calldict = {}
retdict = {}

for line in text:
    try:
        if line.startswith('0x'):
            if line.split()[1] == 'call':
                address1 = line.split()[0].split('x')[1].lstrip('0')
                address = ('0x' + address1).rstrip(':')
                calldict[address] = 1
            elif line.split()[1] == 'ret':
                address1 = line.split()[0].split('x')[1].lstrip('0')
                address = '0x' + address1.rstrip(':')
                retdict[address] = 1
            elif line.split()[1] == 'repz' and line.split()[2] == 'ret':
                address1 = line.split()[0].split('x')[1].lstrip('0')
                address = '0x' + address1.rstrip(':')
                retdict[address] = 1
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
            if line.split()[1] == 'call':
                address1 = line.split()[0].split('x')[1].lstrip('0')
                address = ('0x' + address1).rstrip(':')
                calldict[address] = 1
            elif line.split()[1] == 'ret':
                address1 = line.split()[0].split('x')[1].lstrip('0')
                address = '0x' + address1.rstrip(':')
                retdict[address] = 1
            elif line.split()[1] == 'repz' and line.split()[2] == 'ret':
                address1 = line.split()[0].split('x')[1].lstrip('0')
                address = '0x' + address1.rstrip(':')
                retdict[address] = 1
    except:
        #raise
        print line
        raise


calldict['0xfb3cd7'] = 1
retdict['0xfb3ce9'] = 1
'''
#---------------------------------------------------

DataSource = "./qemu019_2/qemu019_2_ins_total"

f = open(DataSource, "r")
text = f.readlines()
f.close()

# the initial call stack level
init = 0
level = init

for i in xrange(len(text)):
    if text[i].startswith(' ---- 0x'):
        address = text[i].split()[1]
        if address in calldict:
            # before call
            for j in xrange(1,100):
                if text[i+j].startswith('# qemu_st32'):
                    call_address = text[i+j].split()[2].split(',')[1].split('{')[1].split('}')[0]
                    break
            print str(i+1)+' '+address+' call '+str(level)+' '+call_address
            level += 1
        elif address in retdict:
            # after ret
            for j in xrange(1,100):
                if text[i+j].startswith('# qemu_ld32'):
                    ret_address = text[i+j].split()[2].split(',')[1].split('{')[1].split('}')[0]
                    break
            level -= 1
            print str(i+1)+' '+address+' ret '+str(level)+' '+ret_address
            
# format: line_number,address,call/ret,level,call/ret address
