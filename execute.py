from mem_func import *

def get_cpu_env(cpu_string,reg):
    if cpu_string.startswith('&') and cpu_string.endswith('HLT=0'):   #XXX: NO '\n'
        reg['eax'] = int(cpu_string.split()[1].split('=')[1], 16)
        reg['ebx'] = int(cpu_string.split()[2].split('=')[1], 16)
        reg['ecx'] = int(cpu_string.split()[3].split('=')[1], 16)
        reg['edx'] = int(cpu_string.split()[4].split('=')[1], 16)
        reg['esi'] = int(cpu_string.split()[5].split('=')[1], 16)
        reg['edi'] = int(cpu_string.split()[6].split('=')[1], 16)
        reg['ebp'] = int(cpu_string.split()[7].split('=')[1], 16)
        reg['esp'] = int(cpu_string.split()[8].split('=')[1], 16)
        reg['eip'] = int(cpu_string.split()[9].split('=')[1], 16)
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


def execute_op(microop,reg,tmp,mem,memmap_table):
    print microop
    #TODO : and_i32 and or_i32 are very important for comparing
    
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



    elif name(microop) == "qemu_ld32" or name(microop) == "qemu_ld16s" or name(microop) == "qemu_ld16u":     # TODO: loc17 not all tmp
        # qemu_ld32 tmp1,tmp2,flag   ;  from location tmp2 to data tmp1
        name_op = name(microop)
        dst = para1(microop)
        src = para2(microop)
        #flag = para3(microop)   #useless
        #if dst.startswith('tmp') and src.startswith('tmp'):
        if dst.startswith('tmp') and src.startswith('*'):
        
            loc_vir = int(src.split('x')[1].split('{')[0],16)    # XXX:the format may change
            loc = memmap(loc_vir,memmap_table)

            if name_op == 'qemu_ld32':
                data = qemu_ld32_mem(mem, loc)
            elif name_op == 'qemu_ld16s':
                data = qemu_ld16s_mem(mem, loc)
            elif name_op == 'qemu_ld16u':
                data = qemu_ld16u_mem(mem, loc)
            tmp[dst] = data


def execute_all(trace_file,reg,tmp,mem,memmap_table):
    f = open(trace_file, "r")
    text = f.readlines()
    f.close()
    for microop in text:
        execute_op(microop,reg,tmp,mem,memmap_table)
    #print '%x'%reg['eax']
    print_str(mem,reg['eax'],memmap_table)
    


#-----------------------------------------------------------------------------------------    
# Specify the files
memory_file = "/home/cy/xp15.dmp"
memmap_file = "/home/cy/project/memmap15"
cpu_env = '& EAX=09c00501 EBX=00147cc0 ECX=0000029d EDX=00000009 ESI=00000000 EDI=00000000 EBP=0012fa28 ESP=0012f9f8 EIP=7e433f07 EFL=00000246 [---Z-P-] CR3=0f397000 CPL=3 II=0 A20=1 SMM=0 HLT=0'
trace_file = "/home/cy/project/slicing_result.txt"
#disk = 
#-----------------------------------------------------------------------------------------    
#Global declaration
reg = {}   # register, as a dict type
tmp = {}   # tmp variable, as a dict type
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


