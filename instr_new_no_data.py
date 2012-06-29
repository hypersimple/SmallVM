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




def execute_op(microop,reg,tmp,text,count):
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
            '''
            elif dst == 'cc_src':
                cc_src = tmp[src]
            elif dst == 'cc_dst':
                cc_dst = tmp[src] 
            elif dst == 'cc_op':
                cc_op = tmp[src]
            '''
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
        flag = para3(microop)
        
        #if src.startswith('tmp') and dst.startswith('tmp'):
        '''
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
        '''        
                
        if src.startswith('tmp') and dst.startswith('tmp'):
            #TODO:transfer from virtual to physical
            
            #data = tmp[src]
            #loc_vir = tmp[dst]
            loc_vir = tmp[dst]   # XXX:the format may change, this the transformed constant format
            #print microop
            #print '%x'%loc_vir
            '''
            loc = memmap(loc_vir,memmap_table)
            
            if name_op == 'qemu_st32':
                qemu_st32_mem(mem, loc, data)
            elif name_op == 'qemu_st16':
                qemu_st16_mem(mem, loc, data)
            '''
            
            text[count] = '# ' + name_op + ' ' + src\
            + ',' + '*0x'+'%x'%loc_vir\
            + ',' + flag + '\n'


    elif name(microop) == "qemu_ld32" or name(microop) == "qemu_ld16s" or name(microop) == "qemu_ld16u":     # TODO: loc17 not all tmp
        # qemu_ld32 tmp1,tmp2,flag   ;  from location tmp2 to data tmp1
        name_op = name(microop)
        dst = para1(microop)
        src = para2(microop)
        flag = para3(microop)
        #if dst.startswith('tmp') and src.startswith('tmp'):
        '''
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
        ''' 
            
        if dst.startswith('tmp') and src.startswith('tmp'):
        
            loc_vir = tmp[src]    # XXX:the format may change
            '''
            loc = memmap(loc_vir,memmap_table)

            if name_op == 'qemu_ld32':
                data = qemu_ld32_mem(mem, loc)
            elif name_op == 'qemu_ld16s':
                data = qemu_ld16s_mem(mem, loc)
            elif name_op == 'qemu_ld16u':
                data = qemu_ld16u_mem(mem, loc)
            tmp[dst] = data
            '''
            text[count] = '# ' + name_op + ' ' + dst\
            + ',' + '*0x'+'%x'%loc_vir +\
            '{' + '0x%x'%0 + '}'\
            + ',' + flag + '\n'
            

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


def execute_all(text,cpu_string,reg,tmp):

    get_cpu_env(cpu_string,reg)
    count = 0
    for microop in text:
        if microop.startswith('#'):
            execute_op(microop,reg,tmp,text,count)
        count += 1
    return text
    
    #print 'EAX=%08x'%reg['eax']
    #print_str(mem,reg['eax'],memmap_table)
    




