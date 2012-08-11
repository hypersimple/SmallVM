from para_calc2 import *

# TODO: remove the constant number ($0x11) from slice_set / srcpara set

def slicing(instr_line, microop,slice_set,instruction_list):
    global first_cpu
    
    if set(destpara(microop)) <= slice_set: # If included in the slice_set
        #print 1
        slice_set = slice_set - set(destpara(microop))  #Minus of set
        slice_set = slice_set | set(srcpara(microop))   #Union of set
        instruction_list.append(str(instr_line)+' '+microop)
        #instruction_list.append(microop)
        print str(instr_line)+' '+microop
        
        first_cpu = 1
        '''
        if microop.split()[1] != 'movi_i32' and microop.split()[1] != 'mov_i32'\
        and microop.split()[1] != 'qemu_ld32' and microop.split()[1] != 'qemu_st32'\
        and microop.split()[1] != 'add_i32':
            print str(instr_line)+' '+microop
        '''
        #print slice_set
    '''
    elif microop.startswith('# call'):
        instruction_list.append(str(instr_line)+' '+microop)
        print str(instr_line)+' '+microop
    '''
    
    return (slice_set, instruction_list)                # return a tuple



DataSource = "./qemu40/qemu40_ins_total"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array
f.close()


instruction_list = []

init_list = []

#init_list.append('eax')    # The destination parameter, and the line as the same
init_list.append('tmp0')

slice_set = set(init_list)


#line = 310653 - 1
#line = 312408 - 1
#line = 806670 - 1        # Set the interested line; 0x7e43b6d6; the destination para
#line = len(text) -1
line = 735771 - 1

first_cpu = 1
for subline in xrange(0,line+1):
    if text[line-subline].startswith('#'):
        (slice_set, instruction_list) = slicing(line-subline+1, text[line-subline], slice_set,instruction_list)
        
    elif text[line-subline].startswith('@'):
        if first_cpu == 1:
            instruction_list.append('-----------------------------------------------------------------------\n')
            instruction_list.append(text[line-subline])
            instruction_list.append('-----------------------------------------------------------------------\n')
            first_cpu = 0


f2 = open("./qemu40/qemu40_slicing_tmp.log","w")

i = len(instruction_list)-1
while(i != -1):
    #print instruction_list[i]
    f2.write(instruction_list[i])
    i -= 1
f2.close()

print 'slice_set:'
print slice_set



#print slice_set
#(slice_set, instruction_list) = slicing("# add_i32 tmp3,tmp2,tmp12",slice_set,instruction_list)
#(slice_set, instruction_list) = slicing("# add_i32 tmp2,tmp2,tmp13",slice_set,instruction_list)

#print instruction_list

'''
for i in xrange(0,len(instruction_list)):
    print instruction_list[i]

print slice_set
'''
#print 'begin write to file'


# replace tmp2 with the concrete address, use the following code


'''
# NOT replace tmp2 with the concrete address, use the following code
f2 = open("qemu17_slicing.log","w")

i = len(instruction_list)-1
while(i != -1):
    #print instruction_list[i]
    if instruction_list[i].split()[2].startswith('qemu_st') or instruction_list[i].split()[2].startswith('qemu_ld'):
       tmp = instruction_list[i]
       instruction_list[i] = tmp.split()[0] + ' ' + '# ' + tmp.split()[2]+' '+tmp.split()[3].split(',')[0]+','+'tmp2'+','+tmp.split()[3].split(',')[2]+'\n'
    f2.write(instruction_list[i])
    i -= 1
f2.close()
'''






'''
# Without the line number, NOT use the concrete address, use the following code
f2 = open("qemu17_slicing.log","w")

i = len(instruction_list)-1
while(i != -1):
    #print instruction_list[i]
    if instruction_list[i].startswith('# qemu_st') or instruction_list[i].startswith('# qemu_ld'):
       tmp = instruction_list[i]
       instruction_list[i] = '# ' + tmp.split()[1]+' '+tmp.split()[2].split(',')[0]+','+'tmp2'+','+tmp.split()[2].split(',')[2]+'\n'
    f2.write(instruction_list[i])
    i -= 1
f2.close()
'''
