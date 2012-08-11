from mem_func import *

PARA_POSITION = 1


if PARA_POSITION == 1:
    # starts with "#"
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
    def paraw(microop):   # whole parameter
        return microop.split()[2]



if PARA_POSITION == 2:
    # starts with number
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
    def para5(microop):
        return microop.split()[3].split(',')[4]
    def paraw(microop):   # whole parameter
        return microop.split()[3]




def memmap(virtual,cr3,memmap_table):
    if ((virtual & 0xfffff000),cr3) in memmap_table:
        return memmap_table[(virtual & 0xfffff000),cr3] + (virtual & 0x00000fff)
    else:
        #print 'memmap error: ' + '0x%x'%(virtual) + ' | cr3: ' +cr3
        # Too many errors
        return 0xdeadbeef


def execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3,vmem,flagdict):


    PRINT_ERROR = 0
    PRINT_OTHER_ERROR = 0
    PRINT_MEM_ERROR = 0
    PRINT_UNDEFINED_ERROR = 0

    #print microop

    if name(microop) == "mov_i32":
        # mov_i32 tmp0,esi
        # "src" and "dst" are strings, sth like tmp['tmp0']
        src = para2(microop)
        dst = para1(microop)
    
        try:
            reg[dst] = reg[src]
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
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
            # TODO: dst_str could be 'loc15'
        '''
            


    elif name(microop) == "movi_i32":
    
        src = para2(microop)
        dst = para1(microop)
        try:
            reg[dst] = int(src.split('x')[1],16)
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if dst.startswith('tmp'):
            tmp[dst] = int(src.split('x')[1],16)
        elif dst.startswith('e'):
            reg[dst] = int(src.split('x')[1],16)
        elif dst == 'cc_op':
            cc_op = int(src.split('x')[1],16)
        else:
        '''
        
        

    elif name(microop) == "add_i32":

        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        try:
            reg[dst] = (reg[src1] + reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src1.startswith('e'):
            tmp[dst] = (reg[src1] + tmp[src2]) % 0x100000000
        # XXX src2 may not startswith('tmp')
        elif src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] + tmp[src2]) % 0x100000000
        else:
        '''
        
        #TODO: # add_i32 tmp8,cc_dst,cc_src
        #TODO: # add_i32 cc_op,tmp6,tmp12
        #TODO: src2 may not startswith('tmp')


    elif name(microop) == "shl_i32":
    
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        
        try:
            reg[dst] = (reg[src1] << reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] << tmp[src2]) % 0x100000000
        else:
        '''
        
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
            
            data = reg[src]
            loc_vir = reg[dst]   # XXX:the format may change, this the transformed constant format
            #print microop
            #print '%x'%loc_vir
            
            loc = memmap(loc_vir,cr3,memmap_table)

            if len(mem) != 0 and loc != 0xdeadbeef:
                try:
                    if name_op == 'qemu_st32':
                        qemu_st32_mem(mem, loc, data)
                    elif name_op == 'qemu_st16':
                        qemu_st16_mem(mem, loc, data)
                    elif name_op == 'qemu_st8':
                        qemu_st8_mem(mem, loc, data)
                except:
                    print 'qemu_st phy error: '+'%x'%loc_vir+ ' '+cr3
            else:
                try:
                    if name_op == 'qemu_st32':
                        qemu_st32_vmem(vmem, loc_vir, data)
                    elif name_op == 'qemu_st16':
                        qemu_st16_vmem(vmem, loc_vir, data)
                    elif name_op == 'qemu_st8':
                        qemu_st8_vmem(vmem, loc_vir, data)
                except:
                    print 'qemu_st vir error: '+'%x'%loc_vir+ ' '+cr3
                    
            
            text[count] = text[count].replace('tmp2','*0x'+'%x'%loc_vir+'{' + '0x%x'%data + '}')
            
            '''
            text[count] = '# ' + name_op + ' ' + src\
            + ',' + '*0x'+'%x'%loc_vir\
            + '{' + '0x%x'%data + '}'\
            + ',' + flag + '\n'
            '''

        elif src.startswith('tmp') and dst.startswith('*'):
            #TODO:transfer from virtual to physical
            
            data = reg[src]
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
        else:
            if PRINT_MEM_ERROR == 1:
                print microop
            else:
                pass





    elif name(microop) == "qemu_ld32" or name(microop) == "qemu_ld16s" or name(microop) == "qemu_ld16u" or name(microop) == "qemu_ld8s" or name(microop) == "qemu_ld8u":     # TODO: loc17 not all tmp
        # qemu_ld32 tmp1,tmp2,flag   ;  from location tmp2 to data tmp1
        name_op = name(microop)
        dst = para1(microop)
        src = para2(microop)
        flag = para3(microop)
        #if dst.startswith('tmp') and src.startswith('tmp'):

        if dst.startswith('tmp') and src.startswith('tmp'):
        
            loc_vir = reg[src]    # XXX:the format may change
            loc = memmap(loc_vir,cr3,memmap_table)
            
            #print 'loc_vir %x'%loc_vir
            #print '%x'%loc
            
            if len(mem) != 0 and loc != 0xdeadbeef:
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
                    
                    #if data != 0xdeadbeef:
                    reg[dst] = data
                    
                    text[count] = text[count].replace('tmp2','*0x'+'%x'%loc_vir+'{' + '0x%x'%data + '}')
                    
                    '''
                    text[count] = '# ' + name_op + ' ' + dst\
                    + ',' + '*0x'+'%x'%loc_vir +\
                    '{' + '0x%x'%data + '}'\
                    + ',' + flag + '\n'
                    '''
                except:
                    print 'qemu_ld phy error: '+'%x'%loc_vir+' '+cr3
                    
                    text[count] = text[count].replace('tmp2','*0x'+'%x'%loc_vir+'{' + '0x%x'%0xdeadbeef + '}')
                
                    '''
                    text[count] = '# ' + name_op + ' ' + dst\
                    + ',' + '*0x'+'%x'%loc_vir +\
                    '{' + '0x%x'%0xdeadbeef + '}'\
                    + ',' + flag #+ '\n'
                    '''
                    
            else:
                try:
                    if name_op == 'qemu_ld32':
                        data = qemu_ld32_vmem(vmem, loc_vir)
                    elif name_op == 'qemu_ld16s':
                        data = qemu_ld16s_vmem(vmem, loc_vir)
                    elif name_op == 'qemu_ld16u':
                        data = qemu_ld16u_vmem(vmem, loc_vir)
                    elif name_op == 'qemu_ld8s':
                        data = qemu_ld8s_vmem(vmem, loc_vir)
                    elif name_op == 'qemu_ld8u':
                        data = qemu_ld8u_vmem(vmem, loc_vir)
                    
                    #if data != 0xdeadbeef:
                    reg[dst] = data
                    
                    text[count] = text[count].replace('tmp2','*0x'+'%x'%loc_vir+'{' + '0x%x'%data + '}')
                    
                    '''
                    text[count] = '# ' + name_op + ' ' + dst\
                    + ',' + '*0x'+'%x'%loc_vir +\
                    '{' + '0x%x'%data + '}'\
                    + ',' + flag + '\n'
                    '''
                except:
                    print 'qemu_ld vir error: '+'%x'%loc_vir+' '+cr3
                    
                    text[count] = text[count].replace('tmp2','*0x'+'%x'%loc_vir+'{' + '0x%x'%0xdeadbeef + '}')
                
                    '''
                    text[count] = '# ' + name_op + ' ' + dst\
                    + ',' + '*0x'+'%x'%loc_vir +\
                    '{' + '0x%x'%0xdeadbeef + '}'\
                    + ',' + flag #+ '\n'
                    '''
                
                
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
                
                if data != 0xdeadbeef:
                    reg[dst] = data
            except:
                print 'qemu_ld error!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'
        else:
            if PRINT_MEM_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "sub_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        try:
            reg[dst] = (reg[src1] - reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src1.startswith('e') and src2.startswith('tmp'):
            tmp[dst] = (reg[src1] - tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] - tmp[src2]) % 0x100000000
        else:
        '''
        


    elif name(microop) == "and_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        try:
            reg[dst] = (reg[src1] & reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''    
        if src1.startswith('e'):
            tmp[dst] = (reg[src1] & tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] & tmp[src2]) % 0x100000000
        else:
        '''
        
            
            
    elif name(microop) == "or_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        try:
            reg[dst] = (reg[src1] | reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src1.startswith('e'):
            tmp[dst] = (reg[src1] | tmp[src2]) % 0x100000000
        elif src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] | tmp[src2]) % 0x100000000
        else:
        '''
        
            
            
    elif name(microop) == "xor_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        try:
            reg[dst] = (reg[src1] ^ reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
            '''
            if src1.startswith('e'):
                tmp[dst] = (reg[src1] ^ tmp[src2]) % 0x100000000
            elif src1.startswith('tmp') and dst.startswith('tmp'):
                tmp[dst] = (tmp[src1] ^ tmp[src2]) % 0x100000000
            else:
                print microop
            '''
        
            
            
            
    elif name(microop) == "ext16u_i32":
        src = para2(microop)
        dst = para1(microop)

        #if src.startswith('e'):
            #tmp[dst] = (reg[src1] | tmp[src]) % 0x100000000
        try:
            reg[dst] = (reg[src] & 0x0000ffff) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src] & 0x0000ffff) % 0x100000000
        else:
        '''


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
                reg[dest] = (reg[t1] & ~0x0000ffff) | (reg[t2] & 0x0000ffff)
            elif leng.startswith('$0x8'):
                reg[dest] = (reg[t1] & ~0x000000ff) | (reg[t2] & 0x000000ff)
        except:
            #print 'deposit_i32 error'
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "not_i32":
        src1 = para2(microop)
        dst = para1(microop)
        
        try:
            reg[dst] = ~reg[src1] % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src1.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = ~tmp[src1] % 0x100000000
        else:
        '''

        

    elif name(microop) == "shr_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        
        try:
            reg[dst] = (reg[src1] >> reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src1.startswith('tmp') and src2.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = (tmp[src1] >> tmp[src2]) % 0x100000000
        else:
        '''
    
    elif name(microop) == "ext8s_i32":
        src = para2(microop)
        dst = para1(microop)
        try:
            if (reg[src] & 0x00000080):
                reg[dst] = ((reg[src] & 0x000000ff) | 0xffffff00) % 0x100000000
            else:
                reg[dst] = (reg[src] & 0x000000ff) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
        '''
        if src.startswith('tmp') and dst.startswith('tmp'):
            tmp[dst] = ((tmp[src] & 0x000000ff) | 0xffffff00) % 0x100000000
        else:
        '''
        
    elif name(microop) == "ext8u_i32":
        src = para2(microop)
        dst = para1(microop)
        try:
            reg[dst] = (reg[src] & 0x000000ff) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass
    
    # the highest bit occupies the moved bits     
    elif name(microop) == "sar_i32":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        try:
            if reg[src1] & 0x80000000:
                bits = reg[src2]
                mask = (0xffffffff << (32 - bits)) % 0x100000000
                reg[dst] = ((reg[src1] >> reg[src2]) | mask) % 0x100000000
            else:
                reg[dst] = (reg[src1] >> reg[src2]) % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "neg_i32":     #XXX: Not confirmed
        src1 = para2(microop)
        dst = para1(microop)
        
        try:
            reg[dst] = ~reg[src1]+1 % 0x100000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass



    elif name(microop) == "mul_i64":

        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        try:
            reg[dst] = (reg[src1] * reg[src2]) % 0x10000000000000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass

        
    elif name(microop) == "ext32u_i64":
        src = para2(microop)
        dst = para1(microop)

        #if src.startswith('e'):
            #tmp[dst] = (reg[src1] | tmp[src]) % 0x100000000
        try:
            reg[dst] = (reg[src] & 0x00000000ffffffff) % 0x10000000000000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "ext32s_i64":
        src = para2(microop)
        dst = para1(microop)
        try:
            if (reg[src] & 0x0000000080000000):
                reg[dst] = ((reg[src] & 0x00000000ffffffff) | 0xffffffff00000000) % 0x10000000000000000
            else:
                reg[dst] = (reg[src] & 0x00000000ffffffff) % 0x10000000000000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "shr_i64":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)
        
        try:
            reg[dst] = (reg[src1] >> reg[src2]) % 0x10000000000000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "add_i64":
        src1 = para2(microop)
        src2 = para3(microop)
        dst = para1(microop)

        try:
            reg[dst] = (reg[src1] + reg[src2]) % 0x10000000000000000
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "ld_i32":
        dst = para1(microop)
        env = para2(microop)
        constant = para3(microop)
        
        try:
            if env == 'env':
                if constant.startswith('$0x84'):
                    reg[dst] = reg['fs_base']
                elif constant.startswith('$0x74'):   # ds_base, always=0
                    reg[dst] = 0
                elif constant.startswith('$0x34'): # es related, always=1
                    reg[dst] = 1
                else:
                    reg[dst] = 0
                    if PRINT_ERROR == 1:
                        print microop
                     
            else:
                if PRINT_ERROR == 1:
                    print microop
            
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop) == "st_i32":
        src = para1(microop)
        env = para2(microop)
        constant = para3(microop)
        
        try:
            if env == 'env':
                if constant.startswith('$0x84'):
                    reg[fs_base] = reg[src]
                elif constant.startswith('$0x20'):
                    pass
                else:
                    if PRINT_ERROR == 1:   #XXX 0, not 1
                        print microop
                     
            else:
                if PRINT_ERROR == 1:
                    print microop
            
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass


    elif name(microop).startswith('movi_i64'):
        src = para2(microop)
        dst = para1(microop)
        try:
            #reg[dst] = int(src.split('x')[1],16)
            if src.startswith('$sysenter'):  #sysexit is implemented outside the execution
                reg['esp'] = 0xf896c000
                
            elif src.startswith('$sysexit'):
                reg['esp'] = reg['ecx']
                
            elif src.startswith('$divl_EAX'):
                temp = reg['edx']*0x100000000 + reg['eax']
                temp1 = temp / reg['tmp0']
                remainder = temp % reg['tmp0']
                reg['eax'] = temp1
                reg['edx'] = remainder
                
            elif src.startswith('$set_inhibit_irq'):
                flagdict['$set_inhibit_irq'] = 1
            
            elif src.startswith('$reset_inhibit_irq'):
                flagdict['$set_inhibit_irq'] = 0
            
            else:
                reg[dst] = src
                
                if PRINT_ERROR == 1:
                    print microop
                else:
                    pass
        except:
            if PRINT_ERROR == 1:
                print microop
            else:
                pass

    elif name(microop) == 'call':
        cname = para1(microop)  # cname = callname
        try:
            if paraw(microop).startswith('tmp13,$0x0,$0,tmp12,tmp6'):  # load_seg
                if reg['tmp6'] == 0x30:
                    reg['fs_base'] = 0xffdff000
                elif reg['tmp6'] == 0x3b:
                    reg['fs_base'] = 0x7ffdf000
                elif reg['tmp6'] == 0x23:
                    pass
                    # ds related, do nothing here
            elif reg[cname] == '$bsf':
                src = para5(microop)
                dst = para4(microop)
                bit = 0
                while bit != 32:
                    if (reg[src] >> bit) & 0x1:
                        reg[dst] = bit
                        break
                    else:
                        bit += 1
            elif reg[cname] == '$bsr':
                src = para5(microop)
                dst = para4(microop)
                bit = 0
                while bit != 32:
                    if (reg[src] << bit) & 0x80000000:
                        reg[dst] = bit
                        break
                    else:
                        bit += 1

        except:
            if PRINT_ERROR == 1:
                print microop
                raise
            else:
                pass
                
    elif name(microop) == 'exit_tb':
        flagdict['exit_tb'] = 1

    elif name(microop).startswith('goto')\
        or name(microop).startswith('exit')\
        or name(microop).startswith('nop')\
        or name(microop).startswith('discard')\
        or name(microop).startswith('end'):
        
        if PRINT_OTHER_ERROR == 1:
            print microop
        else:
            pass
                
    else:
        if PRINT_UNDEFINED_ERROR == 1:
            print microop
        else:
            pass

    
    
    
        
    #TODO:
    '''
    # sar_i32 tmp0,tmp0,tmp12
    # shr_i64 tmp13,tmp13,tmp15
    # ext32s_i64 tmp13,tmp0
    
     ---- 0x7c913cb2
    # ext32s_i64 tmp13,tmp0
    # movi_i64 tmp14,$0xfffe
    # mul_i64 tmp13,tmp13,tmp14
    # movi_i64 tmp15,$0x20
    # shr_i64 tmp13,tmp13,tmp15
    # nopn $0x2,$0x2
    
    
    # br $0x1
    # shr_i32 tmp0,eax,tmp12
    # qemu_st8 tmp0,tmp2,$0x0
    '''
