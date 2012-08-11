from execute_op import *

'''
def memmap(virtual,cr3,memmap_table):
    if ((virtual & 0xfffff000),cr3) in memmap_table:
        return memmap_table[(virtual & 0xfffff000),cr3] + (virtual & 0x00000fff)
    else:
        #print 'memmap error: ' + '0x%x'%(virtual) + ' | cr3: ' +cr3
        # Too many errors
        return 0x01111111
'''

def get_reg_state(reg):
    return '@ EAX=%08x'%reg['eax']+' EBX=%08x'%reg['ebx']+' ECX=%08x'%reg['ecx']+' EDX=%08x'%reg['edx']+' ESI=%08x'%reg['esi']+' EDI=%08x'%reg['edi']+' EBP=%08x'%reg['ebp']+' ESP=%08x'%reg['esp']+' EIP=%08x'%reg['eip']
    
def get_tmp_state(reg):
    return '@ TMP0=%08x'%reg['tmp0']+' TMP1=%08x'%reg['tmp1']+' TMP2=%08x'%reg['tmp2']+' TMP4=%08x'%reg['tmp4']+' TMP6=%08x'%reg['tmp6']+' TMP12=%08x'%reg['tmp12']+' TMP13=%08x'%reg['tmp13']+' TMP14=%08x'%reg['tmp14']

def execute_all(text,reg,tmp,mem,memmap_table,cr3,vmem,flagdict):
    count = 0
    
    while count < len(text):
        if text[count].startswith('#'):
            microop = text[count]
            
            
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
                    if reg['ecx'] == 0:
                        break
            '''
                    
            execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3,vmem,flagdict)
            count += 1
        else:
            count += 1

    string = ''
    for i in text:
        string += i+'\n'
    return string
