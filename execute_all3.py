from mem_func import *
from execute_op import *


def memmap(virtual,cr3,memmap_table):
    if ((virtual & 0xfffff000),cr3) in memmap_table:
        return memmap_table[(virtual & 0xfffff000),cr3] + (virtual & 0x00000fff)
    else:
        #print 'memmap error: ' + '0x%x'%(virtual) + ' | cr3: ' +cr3
        # Too many errors
        return 0x01111111

def get_reg_state(reg):
    return '@ EAX=%08x'%reg['eax']+' EBX=%08x'%reg['ebx']+' ECX=%08x'%reg['ecx']+' EDX=%08x'%reg['edx']+' ESI=%08x'%reg['esi']+' EDI=%08x'%reg['edi']+' EBP=%08x'%reg['ebp']+' ESP=%08x'%reg['esp']+' EIP=%08x'%reg['eip']
    
def get_tmp_state(reg):
    return '@ TMP0=%08x'%reg['tmp0']+' TMP1=%08x'%reg['tmp1']+' TMP2=%08x'%reg['tmp2']+' TMP4=%08x'%reg['tmp4']+' TMP6=%08x'%reg['tmp6']+' TMP12=%08x'%reg['tmp12']+' TMP13=%08x'%reg['tmp13']+' TMP14=%08x'%reg['tmp14']

def execute_all(text,reg,tmp,mem,memmap_table,cr3):
    count = 0
    for microop in text:
        '''
        if microop.startswith('@'):
            get_cpu_env(microop,reg)
        '''
        # XXX
        #if microop.startswith('#'):
        #text.insert(count, get_tmp_state(tmp))
        #text.insert(count, get_reg_state(reg))
        #text2.append(get_reg_state(reg)+'\n')
        #text2.append(get_tmp_state(reg)+'\n')
        if microop.startswith('#'):
            execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3)
        
        #text2.append('\n'+text[count]+'\n')
        
        count += 1
        #print count
    string = ''
    for i in text:
        string += i+'\n'
    return string
