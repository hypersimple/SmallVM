from para_calc import *
import string



def get_reg_value(text,line,reg):
    subline = 0
    for subline in range(1,1000000):
        if text[line-subline].startswith('&') and text[line-subline].endswith('HLT=0'):
            if reg == 'eax':
                return text[line-subline].split()[1].split('=')[1]
            if reg == 'ebx':
                return text[line-subline].split()[2].split('=')[1]
            if reg == 'ecx':
                return text[line-subline].split()[3].split('=')[1]
            if reg == 'edx':
                return text[line-subline].split()[4].split('=')[1]
            if reg == 'esi':
                return text[line-subline].split()[5].split('=')[1]
            if reg == 'edi':
                return text[line-subline].split()[6].split('=')[1]
            if reg == 'ebp':
                return text[line-subline].split()[7].split('=')[1]
            if reg == 'esp':
                return text[line-subline].split()[8].split('=')[1]
            if reg == 'eip':
                return text[line-subline].split()[9].split('=')[1]
            if reg == 'efl':
                return text[line-subline].split()[10].split('=')[1]
            if reg == 'cr3':
                return text[line-subline].split()[12].split('=')[1]


# Initialize the tmp array
tmp = []
for i in range(0,50):
    tmp.append('')


# microop is a statement like "# add_i32 tmp2,tmp2,tmp12"
def instruction_calc_pre(text,line,microop):
    value = ''
    
    if  microop.split()[1] == "movi_i32" or \
        microop.split()[1] == "movi_i64" :
        
        if microop.split()[2].split(',')[1].startswith('e'):
            value = '$0x'+get_reg_value(text,line,microop.split()[2].split(',')[1])
        
    return microop.split()[0]+' '+value+''
    
    
    
    #microop.split()[1] == "mov_i32" or \
