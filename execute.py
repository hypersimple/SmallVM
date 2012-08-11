from execute_all2 import *


def get_cpu_env(cpu_string,reg):
    if cpu_string.startswith('@'):   #XXX: NO '\n'
        reg['eax'] = int(cpu_string.split()[3].split('=')[1], 16)
        reg['ebx'] = int(cpu_string.split()[4].split('=')[1], 16)
        reg['ecx'] = int(cpu_string.split()[5].split('=')[1], 16)
        reg['edx'] = int(cpu_string.split()[6].split('=')[1], 16)
        reg['esi'] = int(cpu_string.split()[7].split('=')[1], 16)
        reg['edi'] = int(cpu_string.split()[8].split('=')[1], 16)
        reg['ebp'] = int(cpu_string.split()[9].split('=')[1], 16)
        reg['esp'] = int(cpu_string.split()[10].split('=')[1], 16)
        reg['eip'] = int(cpu_string.split()[1].split('=')[1], 16)
        reg['fs_base'] = int(cpu_string.split()[12].split('=')[1], 16)
        #return reg
        #print '%x'%reg['eax']
    else:
        print 'get_cpu_env error!'


def get_memory(memory_file):
    f = open(memory_file, 'rb')
    data = f.read()
    f.close()
    return bytearray(data)


def get_vmem(vmem_file):
    f = open(vmem_file, 'rb')
    data = f.read()
    f.close()
    return bytearray(data)


def get_disk(disk_file):
    pass


def preprocess_psscan(psscan_file,psscan_table):
    f = open(psscan_file, "r")
    text = f.readlines()
    f.close()
    for line in xrange(len(text)):
        if text[line].startswith('0x'):
            pid = text[line].split()[2]
            cr3 = text[line].split()[4].split('x')[1]
            psscan_table[pid] = cr3  # return PID
            
            
def pidmap(pid,psscan_table):
    if pid in psscan_table:
        return psscan_table[pid]
    else:
        print 'pidmap error, pid: ' + pid


def preprocess_memmap(memmap_file,memmap_table,psscan_table):
    f = open(memmap_file, "r")
    text = f.readlines()
    f.close()
    for line in xrange(0,len(text)):
        try:
            if text[line].split()[1] == 'pid:':
                pid = text[line].split()[2]
                cr3 = pidmap(pid,psscan_table)
            if text[line].startswith('0x'):
                memmap_table[int(text[line].split()[0],16),cr3] = int(text[line].split()[1],16)
        except:
            pass



#------------------------------------------------------------------------
cpu_env = '@ EIP=78b0379c CR3=0eaec000 EAX=78b52028 EBX=05a49670 ECX=0000000b EDX=008f0040 ESI=037004e0 EDI=78ab1ec6 EBP=0012abac ESP=0012ab88 EFLAGS=00000206 FS_BASE=7ffdd000'

start_line_1 = 1

#cpu_env = '@ EIP=00c894c9 CR3=0de44000 EAX=04225040 EBX=0012aad3 ECX=04227050 EDX=04234bf8 ESI=0012aa48 EDI=01e33500 EBP=00dc5dc8 ESP=0012aa30 EFLAGS=00000202 FS_BASE=7ffdf000'

memory_file = "/home/cy/xp38_1.dmp"

vmem_file = "/home/cy/xpv38_1.dmp"

psscan_file = "/home/cy/psscan38"

memmap_file = "/home/cy/memmap38_2"

#------------------------------------------------------------------------


reg = {}   # register, as a dict type
tmp = {}   # tmp variable, as a dict type

vmem = []
mem = []

for i in xrange(50):
    reg['tmp'+str(i)] = 0xdeadbeef
for i in xrange(50):
    reg['loc'+str(i)] = 0xdeadbeef
reg['cc_src'] = 0xdeadbeef
reg['cc_dst'] = 0xdeadbeef
reg['cc_op'] = 0xdeadbeef
#reg['env'] = 0xdeadbeef


memmap_table = {}   # the memory mapping table
psscan_table = {}


flagdict = {}
flagdict['$set_inhibit_irq'] = 0
flagdict['exit_tb'] = 0

get_cpu_env(cpu_env,reg)
#mem = get_memory(memory_file)
vmem = get_vmem(vmem_file)

preprocess_psscan(psscan_file,psscan_table)
preprocess_memmap(memmap_file,memmap_table,psscan_table)


#------------------------------------------------------------------------
#f = open('./qemu30/qemu30_slicing_multi7_tmp2.log', "r")
#f = open('./qemu37/only_instr37_tmp2.log', "r")
f = open('./qemu38/qemu38_ins_tmp2.log', "r")


text = f.readlines()
f.close()

text2 = []
cr3 = '0eaec000'
execute_all(text,reg,tmp,mem,memmap_table,cr3,text2,vmem,start_line_1,flagdict)

#f2 = open('./qemu30/result30_7_13.log',"w")
f2 = open('./qemu38/result_38_4_a',"w")
for line2 in text:
    f2.write(line2)
f2.close()
#------------------------------------------------------------------------


#f2 = open('./qemu30/result30_7_14.log',"w")
f2 = open('./qemu38/result_38_4_b',"w")
for line2 in text2:
    f2.write(line2)
f2.close()

#------------------------------------------------------------------------
