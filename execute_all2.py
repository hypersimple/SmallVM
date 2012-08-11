from execute_op import *


def get_reg_state(reg):
    return '@ EIP=%08x'%reg['eip'] + ' CR3=00000000' + ' EAX=%08x'%reg['eax']+' EBX=%08x'%reg['ebx']+' ECX=%08x'%reg['ecx']+' EDX=%08x'%reg['edx']+' ESI=%08x'%reg['esi']+' EDI=%08x'%reg['edi']+' EBP=%08x'%reg['ebp']+' ESP=%08x'%reg['esp']+' FS_BASE=%08x'%reg['fs_base']
    
def get_tmp_state(reg):
    return '@ TMP0=%08x'%reg['tmp0']+' TMP1=%08x'%reg['tmp1']+' TMP2=%08x'%reg['tmp2']+' TMP4=%08x'%reg['tmp4']+' TMP6=%08x'%reg['tmp6']+' TMP12=%08x'%reg['tmp12']+' TMP13=%08x'%reg['tmp13']+' TMP14=%08x'%reg['tmp14']



def execute_all(text,reg,tmp,mem,memmap_table,cr3,text2,vmem,start_line_1,flagdict):
    # XXX: set the line begin to execute
    #count = 0
    count = start_line_1 - 1

    while count < len(text):

        if text[count].startswith('#'):
            microop = text[count]
            
            if flagdict['exit_tb'] == 1:
                while not name(text[count]).startswith('end'):
                    count += 1
                flagdict['exit_tb'] = 0
            
            # the brcond_i32 instr
            if name(microop) == ('brcond_i32'):
                p1 = para1(microop)
                p2 = para2(microop)
                cond = para3(microop)
                label = para4(microop)
                
                if cond == 'eq': # equal
                    if reg[p1] == reg[p2]:
                        while(not (name(text[count])=='set_label' \
                        and para1(text[count])==label ) ):
                            count += 1
                            
                elif cond == 'ne': # not equal
                    if reg[p1] != reg[p2]:
                        while(not (name(text[count])=='set_label' \
                        and para1(text[count])==label ) ):
                            count += 1
                            
                elif cond == 'lt': # less than
                    # all positive
                    if not ((0x80000000&reg[p1]) or (0x80000000&reg[p2])):
                        if reg[p1] < reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # p1 is negative and p2 is positive
                    elif (0x80000000&reg[p1]) and (not (0x80000000&reg[p2])):
                        while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # all negative
                    elif (0x80000000&reg[p1]) and (0x80000000&reg[p2]):
                        if reg[p1] > reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    
                elif cond == 'le':
                    # all positive
                    if not ((0x80000000&reg[p1]) or (0x80000000&reg[p2])):
                        if reg[p1] < reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # p1 is negative and p2 is positive
                    elif (0x80000000&reg[p1]) and (not (0x80000000&reg[p2])):
                        while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # all negative
                    elif (0x80000000&reg[p1]) and (0x80000000&reg[p2]):
                        if reg[p1] > reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # equal
                    elif reg[p1] == reg[p2]:
                        while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    
                elif cond == 'gt':
                    # all positive
                    if not ((0x80000000&reg[p1]) or (0x80000000&reg[p2])):
                        if reg[p1] > reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # p1 is positive and p2 is negative
                    elif (not (0x80000000&reg[p1])) and (0x80000000&reg[p2]):
                        while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # all negative
                    elif (0x80000000&reg[p1]) and (0x80000000&reg[p2]):
                        if reg[p1] < reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                                
                elif cond == 'ge':
                    # all positive
                    if not ((0x80000000&reg[p1]) or (0x80000000&reg[p2])):
                        if reg[p1] > reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # p1 is positive and p2 is negative
                    elif (not (0x80000000&reg[p1])) and (0x80000000&reg[p2]):
                        while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # all negative
                    elif (0x80000000&reg[p1]) and (0x80000000&reg[p2]):
                        if reg[p1] < reg[p2]:
                            while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                    # equal
                    elif reg[p1] == reg[p2]:
                        while(not (name(text[count])=='set_label' \
                            and para1(text[count])==label ) ):
                                count += 1
                                
                elif cond == 'ltu':
                    if reg[p1] < reg[p2]:
                        while(not (name(text[count])=='set_label' \
                        and para1(text[count])==label ) ):
                            count += 1
                                
                elif cond == 'leu':
                    if reg[p1] <= reg[p2]:
                        while(not (name(text[count])=='set_label' \
                        and para1(text[count])==label ) ):
                            count += 1
                            
                elif cond == 'gtu':
                    if reg[p1] > reg[p2]:
                        while(not (name(text[count])=='set_label' \
                        and para1(text[count])==label ) ):
                            count += 1
                            
                elif cond == 'geu':
                    if reg[p1] >= reg[p2]:
                        while(not (name(text[count])=='set_label' \
                        and para1(text[count])==label ) ):
                            count += 1
                            
                else:
                    print microop
            
            
            '''
            if microop.startswith('# brcond_i32 tmp4,tmp12,ne,$0x0'):
                if text[count+1].startswith('# set_label $0x1'):
                    #print microop
                    if reg['ecx'] == 0:
                        for subcount in xrange(2,200):
                            if text[count+subcount].startswith('# end'):
                                break
                        count = count+subcount
                    #print count
                    count += 2
                    continue
            '''
            
            '''
            if microop.startswith('@'):
                get_cpu_env(microop,reg)
            '''
            # XXX
            #if microop.startswith('#'):
            #text.insert(count, get_tmp_state(tmp))
            #text.insert(count, get_reg_state(reg))
            text2.append(get_reg_state(reg)+'\n')
            #text2.append(get_tmp_state(reg)+'\n')
            execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3,vmem,flagdict)
            
            text2.append('\n#'+str(count+1)+'  '+text[count]+'\n')
            
            count += 1
            #print count
        else:
            count += 1
            
        '''
        elif text[count].startswith('@'):
            if text[count].split()[1] == 'EIP=7c913e09'\
            or text[count].split()[1] == 'EIP=8057c87c'\
            or text[count].split()[1] == 'EIP=805643b1':
                if reg['ecx'] == 0:
                    count += 27
            elif text[count].split()[1] == 'EIP=7c913e0b':
                count += 38
            elif text[count].split()[1] == 'EIP=80564372':
                count += 30
            elif text[count].split()[1] == 'EIP=80564374':
                count += 41
            count += 1
        else:
            count += 1
        '''
    '''
    string = ''
    for i in text:
        string += i+'\n'
    return string
    '''
