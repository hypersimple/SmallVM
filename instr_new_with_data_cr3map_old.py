from mem_func import *
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

'''
def name(microop):
    return microop.split()[2]
def para1(microop):
    return microop.split()[3].split(',')[0]
def para2(microop):
    return microop.split()[3].split(',')[1]
def para3(microop):
    return microop.split()[3].split(',')[2]
def para4(microop):
    return microop.split()[3].split(',')[3]
'''


def name(microop):
    return microop.split()[1]
def para1(microop):
    return microop.split()[2].split(',')[0]
def para2(microop):
    return microop.split()[2].split(',')[1]
def para3(microop):
    return microop.split()[2].split(',')[2]
def para4(microop):
    return microop.split()[2].split(',')[3]
def para5(microop):
    return microop.split()[2].split(',')[4]




def execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3):
    '''
    print 'CPU: EAX=%08x '%reg['eax'] + 'EBX=%08x '%reg['ebx']\
    + 'ECX=%08x '%reg['ecx'] + 'EDX=%08x '%reg['edx'] + 'ESI=%08x '%reg['esi']\
    + 'EDI=%08x '%reg['edi'] + 'EBP=%08x '%reg['ebp'] + 'ESP=%08x '%reg['esp']
    
    print 'tmp0=%08x '%tmp['tmp0'] + 'tmp1=%08x '%tmp['tmp1']\
    + 'tmp2=%08x '%tmp['tmp2'] + 'tmp3=%08x '%tmp['tmp3'] + 'tmp4=%08x '%tmp['tmp4']\
    + 'tmp5=%08x '%tmp['tmp5'] + 'tmp6=%08x '%tmp['tmp6'] + 'tmp7=%08x '%tmp['tmp7']\
    + 'tmp8=%08x '%tmp['tmp8'] + 'tmp9=%08x '%tmp['tmp9'] + 'tmp10=%08x '%tmp['tmp10']\
    + 'tmp11=%08x '%tmp['tmp11'] + 'tmp12=%08x '%tmp['tmp12']
    
    print microop
    '''

    if name(microop) == "mov_i32":
        # mov_i32 tmp0,esi
        # "src" and "dst" are strings, sth like tmp['tmp0']
        src = para2(microop)
        dst = para1(microop)
    
        if src.startswith('e') and dst.startswith('tmp'):   
            tmp[dst] = reg[src]
        
        elif src.startswith('tmp'):
            if dst.startswith('e'):
                reg[dst] = tmp[src]
            elif dst == 'cc_src':
                cc_src = tmp[src]
            elif dst == 'cc_dst':
                cc_dst = tmp[src] 
            elif dst == 'cc_op':
                cc_op = tmp[src]
        else:
            #print 'mov_i32 error'
            #print microop
            # TODO: dst_str could be 'loc15'
            pass


    elif name(microop) == "movi_i32":
    
        src = para2(microop)
        dst = para1(microop)

        if dst.startswith('tmp'):
            tmp[dst] = int(src.split('x')[1],16)
        elif dst == 'cc_op':
            cc_op = int(src.split('x')[1],16)
        else:
            #print 'movi_i32 error'
            pass
        

    elif name(microop) == "add_i32":

        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        if src1.startswith('e'):
            tmp[dst] = (reg[src1] + tmp[src2]) % 0x100000000
        # XXX src2 may not startswith('tmp')
        elif src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):   
            tmp[dst] = (tmp[src1] + tmp[src2]) % 0x100000000
        else:
            #print 'add_i32 error'
            pass
        #TODO: # add_i32 tmp8,cc_dst,cc_src
        #TODO: # add_i32 cc_op,tmp6,tmp12
        #TODO: src2 may not startswith('tmp')


    elif name(microop) == "shl_i32":
    
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        
        if src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] << tmp[src2]) % 0x100000000
        else:
            pass
            #TODO: some strange para
            #print 'shl_i32 error'

    elif name(microop) == "qemu_st32" or name(microop) == "qemu_st16" or name(microop) == "qemu_st8":
        # qemu_st32 tmp1,tmp2,flag  ; from data tmp1 to location tmp2
        name_op = name(microop)
        src = para1(microop)
        dst = para2(microop)
        flag = para3(microop)

        if src.startswith('tmp') and dst.startswith('tmp'):
            #TODO:transfer from virtual to physical
            
            data = tmp[src]
            #loc_vir = tmp[dst]
            loc_vir = tmp[dst]   # XXX:the format may change, this the transformed constant format
            #print microop
            #print '%x'%loc_vir
            
            loc = memmap(loc_vir,cr3,memmap_table)
            
            try:
                if name_op == 'qemu_st32':
                    qemu_st32_mem(mem, loc, data)
                elif name_op == 'qemu_st16':
                    qemu_st16_mem(mem, loc, data)
                elif name_op == 'qemu_st8':
                    qemu_st8_mem(mem, loc, data)
            except:
                print 'qemu_st error'+'%x'%loc_vir+ ' '+cr3

            text[count] = '# ' + name_op + ' ' + src\
            + ',' + '*0x'+'%x'%loc_vir\
            + '{' + '0x%x'%data + '}'\
            + ',' + flag #+ '\n'
            

        elif src.startswith('tmp') and dst.startswith('*'):
            #TODO:transfer from virtual to physical
            
            data = tmp[src]
            #loc_vir = tmp[dst]
            loc_vir = int(dst.split('x')[1].split('{')[0],16)   # XXX:the format may change
            loc = memmap(loc_vir,cr3,memmap_table)
            
            try:
                if name_op == 'qemu_st32':
                    qemu_st32_mem(mem, loc, data)
                elif name_op == 'qemu_st16':
                    qemu_st16_mem(mem, loc, data)
                elif name_op == 'qemu_st8':
                    qemu_st8_mem(mem, loc, data)
            
            except:
                print 'qemu_st error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!' 





    elif name(microop) == "qemu_ld32" or name(microop) == "qemu_ld16s" or name(microop) == "qemu_ld16u" or name(microop) == "qemu_ld8s" or name(microop) == "qemu_ld8u":     # TODO: loc17 not all tmp
        # qemu_ld32 tmp1,tmp2,flag   ;  from location tmp2 to data tmp1
        name_op = name(microop)
        dst = para1(microop)
        src = para2(microop)
        flag = para3(microop)
        #if dst.startswith('tmp') and src.startswith('tmp'):

        if dst.startswith('tmp') and src.startswith('tmp'):
        
            loc_vir = tmp[src]    # XXX:the format may change
            loc = memmap(loc_vir,cr3,memmap_table)

            #print 'loc_vir %x'%loc_vir
            #print 'loc %x'%loc
            try:
                if name_op == 'qemu_ld32':
                    data = qemu_ld32_mem(mem, loc)
                elif name_op == 'qemu_ld16s':
                    data = qemu_ld16s_mem(mem, loc)
                elif name_op == 'qemu_ld16u':
                    data = qemu_ld16u_mem(mem, loc)
                elif name_op == 'qemu_ld8s':
                    data = qemu_ld8s_mem(mem, loc)
                elif name_op == 'qemu_ld8u':
                    data = qemu_ld8u_mem(mem, loc)
                
                if data:
                    tmp[dst] = data
                
                text[count] = '# ' + name_op + ' ' + dst\
                + ',' + '*0x'+'%x'%loc_vir +\
                '{' + '0x%x'%data + '}'\
                + ',' + flag #+ '\n'
                
            except:
                print 'qemu_ld error: '+'%x'%loc_vir+' '+cr3
                
                text[count] = '# ' + name_op + ' ' + dst\
                + ',' + '*0x'+'%x'%loc_vir +\
                '{' + '0x%x'%0xdeadbeef + '}'\
                + ',' + flag #+ '\n'
    
        elif dst.startswith('tmp') and src.startswith('*'):
        
            loc_vir = int(src.split('x')[1].split('{')[0],16)    # XXX:the format may change, this the transformed constant format
            loc = memmap(loc_vir,cr3,memmap_table)

            try:
                if name_op == 'qemu_ld32':
                    data = qemu_ld32_mem(mem, loc)
                elif name_op == 'qemu_ld16s':
                    data = qemu_ld16s_mem(mem, loc)
                elif name_op == 'qemu_ld16u':
                    data = qemu_ld16u_mem(mem, loc)
                elif name_op == 'qemu_ld8s':
                    data = qemu_ld8s_mem(mem, loc)
                elif name_op == 'qemu_ld8u':
                    data = qemu_ld8u_mem(mem, loc)
                
                if data:
                    tmp[dst] = data
            except:
                print 'qemu_ld error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
            

    elif name(microop) == "sub_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        if src1.startswith('e') and src2.startswith('tmp'):
            tmp[dst] = (reg[src1] - tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] - tmp[src2]) % 0x100000000
        else:
            #print 'sub_i32 error'
            #print microop
            pass

    elif name(microop) == "and_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        if src1.startswith('e'):
            tmp[dst] = (reg[src1] & tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] & tmp[src2]) % 0x100000000
        else:
            #print 'add_i32 error'
            pass
            
            
    elif name(microop) == "or_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        if src1.startswith('e'):
            tmp[dst] = (reg[src1] | tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] | tmp[src2]) % 0x100000000
        else:
            #print 'add_i32 error'
            pass
            
            
    elif name(microop) == "xor_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        try:
            if src1.startswith('e'):
                tmp[dst] = (reg[src1] ^ tmp[src2]) % 0x100000000
            elif src1.startswith('tmp') and dst.startswith('tmp'):
                tmp[dst] = (tmp[src1] ^ tmp[src2]) % 0x100000000
            else:
                #print 'add_i32 error'
                pass
        except:
            print 'xor_i32 error, '+microop
            
            
            
    elif name(microop) == "ext16u_i32":
        src = para2(microop)
        dst = para1(microop)

        #if src.startswith('e'):
            #tmp[dst] = (reg[src1] | tmp[src]) % 0x100000000
        if src.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src] & 0x0000ffff) % 0x100000000
        else:
            #print 'add_i32 error'
            pass
            
    elif name(microop) == "deposit_i32":
        #TODO:This is a simplified version
        # deposit_i32 eax,eax,tmp0,$0x0,$0x8
        # deposit_i32 eax,eax,tmp0,$0x0,$0x10
        # deposit_i32/i64 dest, t1, t2, pos, len
        #dest = (t1 & ~0x0f00) | ((t2 << 8) & 0x0f00)
        dest = para1(microop)
        t1 = para2(microop)
        t2 = para3(microop)
        pos = para4(microop)
        leng = para5(microop)
        
        try:
            if leng.startswith('$0x10'):
                reg[dest] = (reg[t1] & ~0x0000ffff) | (tmp[t2] & 0x0000ffff)
            elif leng.startswith('$0x8'):
                reg[dest] = (reg[t1] & ~0x000000ff) | (tmp[t2] & 0x000000ff)
        except:
            print 'deposit_i32 error'
        
        
        
    #TODO:
    '''
    # shr_i32 tmp0,eax,tmp12
    # ext8u_i32 tmp0,tmp0
    # qemu_st8 tmp0,tmp2,$0x0
    '''

def dohash(data):
    dict1 = {}
    text2 = data.split('\n')
    text2_size = len(text2)
    #print len(text2)
    for line in xrange(len(text2)):
        if text2[line] == 'OP after liveness analysis:':
            #print text2[line+1]
            address = text2[line+1].split('x')[1]
            dict1[address] = text2[line]+'\n'
            for subline in xrange(1,2000):
                if text2[line+subline] != '# end ':
                    dict1[address] += text2[line+subline]+'\n'
                else:
                    dict1[address] += '# end \n'
                    break
        if line % 1000000 == 0:
            print float(line)/float(text2_size)
    return dict1


def get_memory(memory_file):
    f = open(memory_file, 'rb')
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

def memmap(virtual,cr3,memmap_table):
    if ((virtual & 0xfffff000),cr3) in memmap_table:
        return memmap_table[(virtual & 0xfffff000),cr3] + (virtual & 0x00000fff)
    else:
        #print 'memmap error: ' + '0x%x'%(virtual) + ' | cr3: ' +cr3
        # Too many errors
        return 0x01111111


def save_mem(save_mem_file,mem):
    f = open(save_mem_file,'wb')
    print 'Writing memory into file...'
    for element in mem:
        f.write(struct.pack('B',element))
    f.close()


def execute_all(text,reg,tmp,mem,memmap_table,cr3):
    count = 0
    for microop in text:
        '''
        if microop.startswith('@'):
            get_cpu_env(microop,reg)
        '''
        if microop.startswith('#'):
            execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3)
        count += 1
    string = ''
    for i in text:
        string += i+'\n'
    return string
        

    #print 'EAX=%08x'%reg['eax']
    #print_str(mem,reg['eax'],cr3,memmap_table)
    

#-----------------------------------------------------------------------------------------    
# the cpu_env is kind of USELESS
cpu_env = '@ EIP=bf8ed843 CR3=03267000 EAX=0000ce57 EBX=e119509c ECX=0000c800 EDX=0000c800 ESI=e1039368 EDI=000000c0 EBP=fb333280 ESP=fb333278 EFLAGS=00000202'
#----------------------------------------------------------------------------
# Specify the files
number = 8

#memory_file = "./qemu25/qemu25_mem_"+str(number-1)
#memory_file = "/home/cy/xp25_1.dmp"
memory_file = "./qemu25/qemu25_mem_"+'0'

psscan_file = "/home/cy/psscan25"
memmap_file = "/home/cy/memmap25_2"

cpu_file = "./qemu25/qemu25_cpu_part_"+str(number)
#cpu_file = "./qemu19/qemu19_cpu_part_0"
#cpu_file = "./qemu25/qemu25_cpu_part_0.log"

hashfile = 'qemu25_de_duplicate.log'

#pre_calc_destfile = "./qemu21/qemu21_ins_"+str(number)+'_b'
#pre_calc_destfile = "./qemu25/qemu25_ins_0"
pre_calc_destfile = "./qemu25/qemu25_ins_"+str(number)

#save_mem_file = './qemu21/qemu21_mem_'+str(number)
save_mem_file = './qemu25/qemu25_mem_'+str(number)
#disk = 
#-----------------------------------------------------------------------------------------    
#Global declaration
reg = {}   # register, as a dict type
tmp = {}   # tmp variable, as a dict type
for i in xrange(50):
    tmp['tmp'+str(i)] = 0xdeadbeef
memmap_table = {}   # the memory mapping table
psscan_table = {}

get_cpu_env(cpu_env,reg)
mem = get_memory(memory_file)
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


f1 = open(hashfile)
data = f1.read()
f1.close()
dict1 = dohash(data)
data = 0


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
            tb = dict1[address]
            tb2 = tb.split('\n')
            tb2 = execute_all(tb2,reg,tmp,mem,memmap_table,cr3)
            text.insert(line+1,tb2)
        else:
            print 'address NOT found in dict1'
    #b = time.time()
    #print '%.10f'%(b-a)
    #print text
    line += 1
    if cpu_count % 10000 == 0:
        print cpu_count


f2 = open(pre_calc_destfile,"w")
for line2 in text:
    f2.write(line2)
f2.close()

#save_mem(save_mem_file,mem)
