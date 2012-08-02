from execute_op import *


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
'''


def get_reg_state(reg):
    return '@ EIP=%08x'%reg['eip'] + ' CR3=00000000' + ' EAX=%08x'%reg['eax']+' EBX=%08x'%reg['ebx']+' ECX=%08x'%reg['ecx']+' EDX=%08x'%reg['edx']+' ESI=%08x'%reg['esi']+' EDI=%08x'%reg['edi']+' EBP=%08x'%reg['ebp']+' ESP=%08x'%reg['esp']+' FS_BASE=%08x'%reg['fs_base']
    
def get_tmp_state(reg):
    return '@ TMP0=%08x'%reg['tmp0']+' TMP1=%08x'%reg['tmp1']+' TMP2=%08x'%reg['tmp2']+' TMP4=%08x'%reg['tmp4']+' TMP6=%08x'%reg['tmp6']+' TMP12=%08x'%reg['tmp12']+' TMP13=%08x'%reg['tmp13']+' TMP14=%08x'%reg['tmp14']

def execute_all(text,reg,tmp,mem,memmap_table,cr3,text2,vmem):
    count = 0
    #count = 9927 - 1
    while count < len(text):
        microop = text[count]
        '''
        if microop.startswith('@'):
            get_cpu_env(microop,reg)
        '''
        # XXX
        #if microop.startswith('#'):
        #text.insert(count, get_tmp_state(tmp))
        #text.insert(count, get_reg_state(reg))
        text2.append(get_reg_state(reg)+'\n')
        text2.append(get_tmp_state(reg)+'\n')
        execute_op(microop,reg,tmp,mem,memmap_table,text,count,cr3,vmem)
        
        text2.append('\n#'+text[count]+'\n')
        
        count += 1
        #print count
    '''
    string = ''
    for i in text:
        string += i+'\n'
    return string
    '''
