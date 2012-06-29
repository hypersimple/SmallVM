from mem_func import *

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


def get_memory(memory_file):
    f = open(memory_file, 'rb')
    data = f.read()
    f.close()
    return bytearray(data)
    


def get_disk(disk_file):
    pass


def preprocess_memmap(memmap_file,memmap_table):
    f = open(memmap_file, "r")
    text = f.readlines()
    f.close()
    for line in xrange(2,len(text)):
        memmap_table[int(text[line].split()[0],16)] = int(text[line].split()[1],16)


def memmap(virtual,memmap_table):
    return memmap_table[virtual & 0xfffff000] + (virtual & 0x00000fff)


def print_str(mem,loc_vir,memmap_table):
    loc = memmap(loc_vir,memmap_table)
    buf = ''
    while(mem[loc] != 0):
        buf += chr(mem[loc])
        loc += 1
    print buf

# XXX: two formats:
# 12345 # mov_i32
# # mov_i32

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
'''



def execute_op(microop,reg,tmp,mem,memmap_table):

    print 'CPU: EAX=%08x '%reg['eax'] + 'EBX=%08x '%reg['ebx']\
    + 'ECX=%08x '%reg['ecx'] + 'EDX=%08x '%reg['edx'] + 'ESI=%08x '%reg['esi']\
    + 'EDI=%08x '%reg['edi'] + 'EBP=%08x '%reg['ebp'] + 'ESP=%08x '%reg['esp']
    
    print 'tmp0=%08x '%tmp['tmp0'] + 'tmp1=%08x '%tmp['tmp1']\
    + 'tmp2=%08x '%tmp['tmp2'] + 'tmp3=%08x '%tmp['tmp3'] + 'tmp4=%08x '%tmp['tmp4']\
    + 'tmp5=%08x '%tmp['tmp5'] + 'tmp6=%08x '%tmp['tmp6'] + 'tmp7=%08x '%tmp['tmp7']\
    + 'tmp8=%08x '%tmp['tmp8'] + 'tmp9=%08x '%tmp['tmp9'] + 'tmp10=%08x '%tmp['tmp10']\
    + 'tmp11=%08x '%tmp['tmp11'] + 'tmp12=%08x '%tmp['tmp12']
    
    print microop


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
            elif dst_str == 'cc_src':
                cc_src = tmp[src]
            elif dst_str == 'cc_dst':
                cc_dst = tmp[src] 
            elif dst_str == 'cc_op':
                cc_op = tmp[src]
        else:
            #print 'mov_i32 error'
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
        elif src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] + tmp[src2]) % 0x100000000
        else:
            #print 'add_i32 error'
            pass
        #TODO: # add_i32 tmp8,cc_dst,cc_src
        #TODO: # add_i32 cc_op,tmp6,tmp12


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

    elif name(microop) == "qemu_st32" or name(microop) == "qemu_st16":
        # qemu_st32 tmp1,tmp2,flag  ; from data tmp1 to location tmp2
        name_op = name(microop)
        src = para1(microop)
        dst = para2(microop)
        #flag = para3(microop)   #useless
        
        #if src.startswith('tmp') and dst.startswith('tmp'):
        if src.startswith('tmp') and dst.startswith('*'):
            #TODO:transfer from virtual to physical
            
            data = tmp[src]
            #loc_vir = tmp[dst]
            loc_vir = int(dst.split('x')[1].split('{')[0],16)   # XXX:the format may change
            loc = memmap(loc_vir,memmap_table)
            
            if name_op == 'qemu_st32':
                qemu_st32_mem(mem, loc, data)
            elif name_op == 'qemu_st16':
                qemu_st16_mem(mem, loc, data)
                
                
        elif src.startswith('tmp') and dst.startswith('tmp'):
            #TODO:transfer from virtual to physical
            
            data = tmp[src]
            #loc_vir = tmp[dst]
            loc_vir = tmp[dst]   # XXX:the format may change, this the transformed constant format
            loc = memmap(loc_vir,memmap_table)
            
            if name_op == 'qemu_st32':
                qemu_st32_mem(mem, loc, data)
            elif name_op == 'qemu_st16':
                qemu_st16_mem(mem, loc, data)



    elif name(microop) == "qemu_ld32" or name(microop) == "qemu_ld16s" or name(microop) == "qemu_ld16u":     # TODO: loc17 not all tmp
        # qemu_ld32 tmp1,tmp2,flag   ;  from location tmp2 to data tmp1
        name_op = name(microop)
        dst = para1(microop)
        src = para2(microop)
        #flag = para3(microop)   #useless
        #if dst.startswith('tmp') and src.startswith('tmp'):
        if dst.startswith('tmp') and src.startswith('*'):
        
            loc_vir = int(src.split('x')[1].split('{')[0],16)    # XXX:the format may change, this the transformed constant format
            loc = memmap(loc_vir,memmap_table)

            if name_op == 'qemu_ld32':
                data = qemu_ld32_mem(mem, loc)
            elif name_op == 'qemu_ld16s':
                data = qemu_ld16s_mem(mem, loc)
            elif name_op == 'qemu_ld16u':
                data = qemu_ld16u_mem(mem, loc)
            tmp[dst] = data
            
        elif dst.startswith('tmp') and src.startswith('tmp'):
        
            loc_vir = tmp[src]    # XXX:the format may change
            loc = memmap(loc_vir,memmap_table)

            if name_op == 'qemu_ld32':
                data = qemu_ld32_mem(mem, loc)
            elif name_op == 'qemu_ld16s':
                data = qemu_ld16s_mem(mem, loc)
            elif name_op == 'qemu_ld16u':
                data = qemu_ld16u_mem(mem, loc)
            tmp[dst] = data
            

    elif name(microop) == "sub_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        if src1.startswith('e'):
            tmp[dst] = (reg[src1] - tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] - tmp[src2]) % 0x100000000
        else:
            #print 'add_i32 error'
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


def execute_all(trace_file,reg,tmp,mem,memmap_table):
    f = open(trace_file, "r")
    text = f.readlines()
    f.close()
    for microop in text:
        execute_op(microop,reg,tmp,mem,memmap_table)
    print 'EAX=%08x'%reg['eax']
    print_str(mem,reg['eax'],memmap_table)
    


#-----------------------------------------------------------------------------------------    
# Specify the files
memory_file = "/home/cy/xp17_1.dmp"
memmap_file = "memmap17_1"
cpu_env = '@ EIP=804de710 CR3=03267000 EAX=000010f7 EBX=7e4298d5 ECX=80042000 EDX=0013e7c4 ESI=0013e8d4 EDI=001a3350 EBP=fb333934 ESP=fb3339a4 EFLAGS=00000002'
trace_file = "qemu17_slicing.log"
#disk = 
#-----------------------------------------------------------------------------------------    
#Global declaration
reg = {}   # register, as a dict type
tmp = {}   # tmp variable, as a dict type
for i in xrange(40):
    tmp['tmp'+str(i)] = 0xdeadbeef
memmap_table = {}   # the memory mapping table

get_cpu_env(cpu_env,reg)
mem = get_memory(memory_file)
preprocess_memmap(memmap_file,memmap_table)
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
print_str(mem,0x147dd0,memmap_table)
'''
execute_all(trace_file,reg,tmp,mem,memmap_table)


