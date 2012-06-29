from para_calc import *
from mem_func_dict import *
import string
import sys


# XXX TODO: When do slicing, compare the number, not the string, 0x001 vs 0x1


DataSource = "qemu17_fetch_new.log"
#DataSource = "test_tmp.txt"

DataDest = "qemu17_instr_calc_new.log"
#DataDest = "test_tmp_result.txt"


f = open(DataSource, "r")
text = f.readlines()  #Text is a string array


f2 = open(DataDest, "w")


# If this is a new Translation Block, we use init_get_reg_value
def init_get_reg_value(text,line,reg):
    subline = 0
    global regi
    for subline in xrange(1,1000000):
        #print text[line-subline]
        if text[line-subline].startswith('@'):
            if reg == 'eax':
                regi[1] = int(text[line-subline].split()[3].split('=')[1], 16)
                return regi[1]
            elif reg == 'ebx':
                regi[2] = int(text[line-subline].split()[4].split('=')[1], 16)
                return regi[2]
            elif reg == 'ecx':
                regi[3] = int(text[line-subline].split()[5].split('=')[1], 16)
                return regi[3]
            elif reg == 'edx':
                regi[4] = int(text[line-subline].split()[6].split('=')[1], 16)
                return regi[4]
            elif reg == 'esi':
                regi[5] = int(text[line-subline].split()[7].split('=')[1], 16)
                return regi[5]
            elif reg == 'edi':
                regi[6] = int(text[line-subline].split()[8].split('=')[1], 16)
                return regi[6]
            elif reg == 'ebp':
                regi[7] = int(text[line-subline].split()[9].split('=')[1], 16)
                return regi[7]
            elif reg == 'esp':
                regi[8] = int(text[line-subline].split()[10].split('=')[1], 16)
                return regi[8]
            elif reg == 'eip':
                regi[9] = int(text[line-subline].split()[1].split('=')[1], 16)
                return regi[9]
            else: 
                return 'init_get_reg_value error'


# If this is an old block, we use get_reg_value
def get_reg_value(text,line,reg):
    global regi
    '''
    if text[line-1].startswith('OP') or \
    (text[line-1].startswith(' ----') and text[line-2].startswith('OP')):
        return init_get_reg_value(text,line,reg)
    '''
    
    if reg == 'eax':
        if regi[1] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[1]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'ebx':
        if regi[2] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[2]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'ecx':
        if regi[3] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[3]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'edx':
        if regi[4] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[4]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'esi':
        if regi[5] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[5]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'edi':
        if regi[6] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[6]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'ebp':
        if regi[7] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[7]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'esp':
        if regi[8] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[8]
        else:
            return init_get_reg_value(text,line,reg)
    elif reg == 'eip':
        if regi[9] != 0xdeadbeef: # "deadbeef" in Hex
            return regi[9]
        else:
            return init_get_reg_value(text,line,reg)
    else: 
        return 'get_reg_value error'




temp = 0
cc_src = 0
cc_dst = 0
cc_op = 0

# Initialize the tmp array
# The element is number!!!
tmp = []
for i in xrange(0,50):
    tmp.append(0xdeadbeef)  # "deadbeef" in Hex
    
# Initialize the CPU register array
# The element is number!!!
# NO regi[0] !!!
regi = []
for i in xrange(0,10):
    regi.append(0xdeadbeef)  # "deadbeef" in Hex
    
def tmpmap(tmp_string):
    #print tmp_string
    return int(tmp_string.split('tmp')[1])
    
def regmap(reg):
    if reg == 'eax':
        return 1
    elif reg == 'ebx':
        return 2
    elif reg == 'ecx':
        return 3
    elif reg == 'edx':
        return 4
    elif reg == 'esi':
        return 5
    elif reg == 'edi':
        return 6
    elif reg == 'ebp':
        return 7
    elif reg == 'esp':
        return 8
    elif reg == 'eip':
        return 9
    else:
        return 'reg_map error'

# microop is a statement like "# add_i32 tmp2,tmp2,tmp12"
def instruction_calc_pre(text,line,microop):
    global regi,tmp,cc_src,cc_dst,cc_op
    
    #print microop
    
    if microop.split()[1] == "mov_i32" :
        '''
        if  microop.split()[1] == "movi_i32" or \
            microop.split()[1] == "movi_i64" :
        '''    
        src_str = microop.split()[2].split(',')[1]
        dst_str = microop.split()[2].split(',')[0]
        
        if src_str.startswith('e') and dst_str.startswith('tmp'):   # TODO: dst_str could be 'loc15'
            tmp[tmpmap(dst_str)] = get_reg_value(text,line,src_str)
        elif src_str.startswith('tmp'):
            if dst_str.startswith('e'):
                regi[regmap(dst_str)] = tmp[tmpmap(src_str)]
            elif dst_str == 'cc_src':
                cc_src = tmp[tmpmap(src_str)]
            elif dst_str == 'cc_dst':
                cc_dst = tmp[tmpmap(src_str)] 
            elif dst_str == 'cc_op':
                cc_op = tmp[tmpmap(src_str)]
        else:
            #print 'mov_i32 error'
            pass
    
    
    elif microop.split()[1] == "movi_i32" :
    
        src_str = microop.split()[2].split(',')[1]
        dst_str = microop.split()[2].split(',')[0]

        if dst_str.startswith('tmp'):
            tmp[tmpmap(dst_str)] = int(src_str.split('x')[1],16)
        elif dst_str == 'cc_op':
            cc_op = int(src_str.split('x')[1],16)
        else:
            #print 'movi_i32 error'
            pass
            
    elif microop.split()[1] == "add_i32" :

        src_str1 = microop.split()[2].split(',')[1]
        src_str2 = microop.split()[2].split(',')[2]
        dst_str = microop.split()[2].split(',')[0]

        if src_str1.startswith('e'):
            tmp[tmpmap(dst_str)] = (regi[regmap(src_str1)] + tmp[tmpmap(src_str2)]) % 0x100000000

        elif src_str1.startswith('tmp') and dst_str.startswith('tmp'):
            tmp[tmpmap(dst_str)] = (tmp[tmpmap(src_str1)] + tmp[tmpmap(src_str2)]) % 0x100000000
            
        else:
            #print 'add_i32 error'
            pass
        #TODO: # add_i32 tmp8,cc_dst,cc_src
        #TODO: # add_i32 cc_op,tmp6,tmp12
        
    elif microop.split()[1] == "shl_i32" :
    
        src_str1 = microop.split()[2].split(',')[1]
        src_str2 = microop.split()[2].split(',')[2]
        dst_str = microop.split()[2].split(',')[0]
        '''
        if src_str1.startswith('e'):
            tmp[tmpmap(dst_str)] = (regi[regmap(src_str1)] + tmp[tmpmap(src_str2)]) % 0x100000000
        '''
        
        if src_str1.startswith('tmp') and src_str2.startswith('tmp') and dst_str.startswith('tmp'):
            tmp[tmpmap(dst_str)] = (tmp[tmpmap(src_str1)] << tmp[tmpmap(src_str2)]) % 0x100000000
        else:
            pass
            #print 'shl_i32 error'
        
    '''    
    # for DEBUG
    print microop,
    print 'tmp0: '+ '%x'%tmp[0]
    print 'tmp2: '+ '%x'%tmp[2]
    print 'tmp4: '+ '%x'%tmp[4]
    print 'tmp12: '+ '%x'%tmp[12]
    print
    '''        

        
def parse_text(text, mem):
    line = 0
    global regi,tmp
    for line in xrange(0,len(text)):
    
        if text[line].startswith('@'):
                regi[1] = int(text[line].split()[3].split('=')[1], 16)
                regi[2] = int(text[line].split()[4].split('=')[1], 16)
                regi[3] = int(text[line].split()[5].split('=')[1], 16)
                regi[4] = int(text[line].split()[6].split('=')[1], 16)
                regi[5] = int(text[line].split()[7].split('=')[1], 16)
                regi[6] = int(text[line].split()[8].split('=')[1], 16)
                regi[7] = int(text[line].split()[9].split('=')[1], 16)
                regi[8] = int(text[line].split()[10].split('=')[1], 16)
                regi[9] = int(text[line].split()[1].split('=')[1], 16)
                
        elif text[line].startswith('#'):
            instruction_calc_pre(text,line,text[line])
                        
            if text[line].split()[1] == "qemu_st32" or text[line].split()[1] == "qemu_st16":    # TODO: loc17 not all tmp
                # qemu_st32 tmp1,tmp2,flag  ; from data tmp1 to location tmp2
                name = text[line].split()[1]
                str1 = text[line].split()[2].split(',')[0]
                str2 = text[line].split()[2].split(',')[1]
                flag = text[line].split()[2].split(',')[2]
                
                
                
                if str1.startswith('tmp') and str2.startswith('tmp'):
                
                    data = tmp[tmpmap(str1)]
                    loc = tmp[tmpmap(str2)]
                
                    text[line] = '# ' + name + ' ' + str1 \
                    + ',' + '*0x'+'%x'%loc + ',' + flag + '\n'
                    
                    if name == 'qemu_st32':
                        qemu_st32_mem(mem, loc, data)
                        
                    elif name == 'qemu_st16':
                        qemu_st16_mem(mem, loc, data)
                    
                    
                    
            elif text[line].split()[1] == "qemu_ld32" or text[line].split()[1] == "qemu_ld16s" or text[line].split()[1] == "qemu_ld16u":     # TODO: loc17 not all tmp
            
                # qemu_ld32 tmp1,tmp2,flag   ;  from location tmp2 to data tmp1
                name = text[line].split()[1]
                str1 = text[line].split()[2].split(',')[0]
                str2 = text[line].split()[2].split(',')[1]
                flag = text[line].split()[2].split(',')[2]
                
                #data = tmp[tmpmap(str1)]
                
                
                if str1.startswith('tmp') and str2.startswith('tmp'):
                
                    loc = tmp[tmpmap(str2)]
                    #print text[line]
                    
                    if name == 'qemu_ld32':
                        data = qemu_ld32_mem(mem, loc)
                    elif name == 'qemu_ld16s':
                        data = qemu_ld16s_mem(mem, loc)
                    elif name == 'qemu_ld16u':
                        data = qemu_ld16u_mem(mem, loc)
                
                    tmp[tmpmap(str1)] = data
                
                    text[line] = '# ' + name + ' ' + str1 \
                    + ',' + '*0x'+'%x'%loc +\
                    '{' + '0x%x'%data + '}'\
                    + ',' + flag + '\n'
                    

# XXX NOTE: the tmp[i] could not be assigned, because some instructions are not executed

#for i in xrange()

mem = {}  # We use a dict type to simulate the memory

#print text
#print '%x'%tmp[2]
parse_text(text, mem)
#print '%x'%tmp[2]
for i in xrange(0,len(text)):
    f2.write(text[i])

f2.close()

#line = 10
'''
print regi[7]
print regi[1]
instruction_calc_pre(text,16,"# mov_i32 eax,tmp2")

instruction_calc_pre(text,10,"# mov_i32 tmp2,ebp")
instruction_calc_pre(text,11,"# movi_i32 tmp12,$0xfffffffc")

print '%x'%tmp[2]
print '%x'%tmp[12]

instruction_calc_pre(text,12,"# add_i32 tmp2,tmp2,tmp12")
print '%x'%tmp[2]

print regi[7]
print tmp[2]
print regi[1]
print '%x' % tmp[12]
'''

