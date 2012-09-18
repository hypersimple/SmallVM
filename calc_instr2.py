#from mem_func import *
from cut_cpu_into_parts import *
from execute_all3 import *
#import time
import struct

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


def print_str(mem,loc_vir,cr3,memmap_table):
    loc = memmap(loc_vir,cr3,memmap_table)
    buf = ''
    while(mem[loc] != 0):
        buf += chr(mem[loc])
        loc += 1
    print buf

# XXX: two formats:
# (1)12345 # mov_i32
# (2)# mov_i32




def dohash(data):
    dict1 = {}
    text2 = data.split('\n')
    text2_size = len(text2)
    #print len(text2)
    for line in xrange(len(text2)):
        if text2[line] == 'OP after liveness analysis:':
            #print text2[line+1]
            address = text2[line+1].split('x')[1]
            temp = text2[line]+'\n'
            for subline in xrange(1,2000):
                if text2[line+subline] != '# end ':
                    temp += text2[line+subline]+'\n'
                else:
                    temp += '# end \n'
                    break
            if address in dict1:
                flag = 0
                for i in xrange(len(dict1[address])):
                    if dict1[address][i] == temp:
                        flag = 1
                if flag == 0:
                    dict1[address].append(temp)
            else:
                dict1[address] = []          # a list
                dict1[address].append(temp)
                
        if line % 1000000 == 0:
            print float(line)/float(text2_size)
    return dict1



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




def save_mem(save_mem_file,mem):
    f = open(save_mem_file,'wb')
    print 'Writing memory into file...'
    for element in mem:
        f.write(struct.pack('B',element))
    f.close()

        

    #print 'EAX=%08x'%reg['eax']
    #print_str(mem,reg['eax'],cr3,memmap_table)
    

def assign_again(number,cpu_file_init,pre_calc_destfile_init):
    #memory_file = "./qemu25/qemu25_mem_"+str(number-1)
    cpu_file = cpu_file_init + str(number)
    pre_calc_destfile = pre_calc_destfile_init + str(number)
    #save_mem_file = './qemu25/qemu25_mem_'+str(number)

    return (cpu_file,pre_calc_destfile)

#-----------------------------------------------------------------------------------------    
# This cpu_env is USELESS
cpu_env = '@ EIP=78b0379c CR3=0e11b000 EAX=78b52028 EBX=0434d4f0 ECX=0000000b EDX=008f0040 ESI=037004f8 EDI=78ab1ec6 EBP=0012abac ESP=0012ab88 EFLAGS=00000206 FS_BASE=7ffdf000'
#-----------------------------------------------------------------------------

#-----------------------------------------------------------------------------

# Specify the files
#number = 0

# Initialize the file parameter

#memory_file = "./qemu25/qemu25_mem_"+str(number-1)
memory_file = "/home/cy/xp020_1.dmp"
#memory_file = "./qemu25/qemu25_mem_"+'0'

vmem_file = "/home/cy/xpv020_1.dmp"

psscan_file = "/home/cy/psscan020"
memmap_file = "/home/cy/memmap020_2"

#cpu_file = "./qemu25/qemu25_cpu_part_"+str(number)
#cpu_file = "./qemu19/qemu19_cpu_part_0"
#cpu_file = "./qemu25/qemu25_cpu_part_0.log"

hashfile = 'qemu020_de_duplicate.log'

#pre_calc_destfile = "./qemu21/qemu21_ins_"+str(number)+'_b'
#pre_calc_destfile = "./qemu25/qemu25_ins_0"
#pre_calc_destfile = "./qemu25/qemu25_ins_"+str(number)

#save_mem_file = './qemu21/qemu21_mem_'+str(number)
#save_mem_file = './qemu25/qemu25_mem_'+str(number)
save_mem_file = './qemu020/qemu020_mem_final'

final_ins_file = "./qemu020/qemu020_ins_total"

# TOTAL_NUMBER (chunk_number): wc -l, use the beginning digit,usually,XXX: 10000 level
TOTAL_NUMBER = 35

print 'Cutting cpu file...'

cpu_file_init = "./qemu020/qemu020_cpu_part_"
#cut_cpu_into_parts('qemu29_cpu.log', cpu_file_init, 100000, TOTAL_NUMBER)
cut_cpu_into_parts('./qemu020/qemu020_rm_int.log', cpu_file_init, 10000, TOTAL_NUMBER)
pre_calc_destfile_init = "./qemu020/qemu020_ins_"

#disk = 
#-----------------------------------------------------------------------------------------    
#Global declaration
reg = {}   # register, as a dict type

for i in xrange(50):
    reg['tmp'+str(i)] = 0xdeadbeef
for i in xrange(50):
    reg['loc'+str(i)] = 0xdeadbeef
reg['cc_src'] = 0xdeadbeef
reg['cc_dst'] = 0xdeadbeef
reg['cc_op'] = 0xdeadbeef
#reg['env'] = 0xdeadbeef


tmp = {}   # tmp variable, as a dict type
for i in xrange(50):
    tmp['tmp'+str(i)] = 0xdeadbeef

memmap_table = {}   # the memory mapping table
psscan_table = {}

mem = []
vmem = []

flagdict = {}

flagdict['$set_inhibit_irq'] = 0

print 'Initializing memory...'

get_cpu_env(cpu_env,reg)
#mem = get_memory(memory_file)
vmem = get_vmem(vmem_file)

preprocess_psscan(psscan_file,psscan_table)
preprocess_memmap(memmap_file,memmap_table,psscan_table)
# mem as the physical shadow memory of the guest OS
#-----------------------------------------------------------------------------------------

'''
# We need not to assign the value back
print '%x'%reg['eip']
#-----------------------------------------------------------------------------------------

#execute_op('# qemu_st32 tmp1,tmp2,flag',reg,tmp,mem)

print '%x'%memmap_table[0x0000010000]
print '%x'%memmap(0x147dd0,memmap_table)
#print '%c'%mem[0]
print '%c'%mem[memmap(0x147dd1,memmap_table)]
#qemu_st32_mem(mem, memmap(0x147dd0,memmap_table), 1)
#print mem[memmap(0x147dd1,memmap_table)]
print_str(mem,0x147dd0,cr3,memmap_table)
print '%c'%mem[0]

print psscan_table
print '%x'%memmap(0x800e1fff,'00039000',memmap_table)
'''

#print memmap_table
#XXX:
#print memmap_table[0x80550f24,'00039000']  # some addresses are not found, maybe the code to modify page table
# some addresses are very weird, like fee00300, out of range
'''
# ------------------------------------------
# deposit_i32 test
text = '1'
count = 0
cr3 = 0x111111
reg['eax'] = 0x22222222
print '%x'%reg['eax']
tmp['tmp0'] = 0x140011
execute_op('# deposit_i32 eax,eax,tmp0,$0x0,$0x8',reg,tmp,mem,memmap_table,text,count,cr3)
print '%x'%reg['eax']
# -------------------------------------------
'''
print 'Do the hashing...'
f1 = open(hashfile)
data = f1.read()
f1.close()
dict1 = dohash(data)
data = 0

print 'Begin the loop...'
for number in xrange(0,TOTAL_NUMBER+1):
    (cpu_file,pre_calc_destfile) = assign_again(number,cpu_file_init,pre_calc_destfile_init)
    
    print ''
    print 'number: '+str(number)
    
    f = open(cpu_file, "r")
    text = f.readlines()
    f.close()

    line = 0
    cpu_count = 0
    while(line <= len(text)-1):
        #a = time.time()
        if text[line].startswith('@'):
            cpu_count += 1
            address = text[line].split()[1].split('=')[1]
            address = address.lstrip('0')
            
            get_cpu_env(text[line],reg)
            cr3 = text[line].split()[2].split('=')[1]
            if address in dict1:
                tb = dict1[address][0]
                tb2 = tb.split('\n')
                tb2 = execute_all(tb2,reg,tmp,mem,memmap_table,cr3,vmem,flagdict)
                text.insert(line+1,tb2)
            else:
                print 'address NOT found in dict1'
        #b = time.time()
        #print '%.10f'%(b-a)
        #print text
        line += 1
        if cpu_count % 1000 == 0:
            print cpu_count
    
    print 'Writing to ins file...'
    print ''
    f2 = open(pre_calc_destfile,"w")
    for line2 in text:
        f2.write(line2)
    f2.close()


print 'Combining and saving the ins file...'
f3 = open (final_ins_file, "w")
for i in xrange(0, TOTAL_NUMBER+1):
    print i
    for line in open(pre_calc_destfile_init+str(i)):
        f3.write(line)
f3.close()


#save_mem(save_mem_file,mem)


