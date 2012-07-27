from para_calc import *

# TODO: remove the constant number ($0x11) from slice_set / srcpara set

def slicing(instr_line, microop,slice_set,instruction_list,last_line,instruction_pure):
    global first_cpu
    
    if set(destpara(microop)) <= slice_set: # If included in the slice_set
        slice_set = slice_set - set(destpara(microop))  #Minus of set
        slice_set = slice_set | set(srcpara(microop))   #Union of set
        instruction_list.append(str(instr_line)+' '+microop)
        instruction_pure.append(microop)
        last_line = instr_line
        #instruction_list.append(microop)
        print str(instr_line)+' '+microop
        
        first_cpu = 1

    return (slice_set, instruction_list,last_line,instruction_pure)                # return a tuple



DataSource = "./qemu30/qemu30_ins_total"

f = open(DataSource, "r")
text = f.readlines()
f.close()


instruction_list = []
instruction_pure = []

init_list = []

#init_list.append('eax')    # The destination parameter, and the line as the same
init_list.append('*0x6c87000')

slice_set = set(init_list)


#line = 806670 - 1        # Set the interested line; 0x7e43b6d6; the destination para
line = 4634232 - 1

stage = 1
last_line = 1
recorded_line = 0

while(last_line >= 1):
    print ''
    print 'stage: ' + str(stage)
    print ''
    instruction_list.append('\nstage: '+str(stage)+'\n')

    first_cpu = 1
    for subline in xrange(0,line+1):
        if text[line-subline].startswith('#'):
            (slice_set, instruction_list,last_line,instruction_pure) = slicing(line-subline+1, text[line-subline], slice_set,instruction_list, last_line,instruction_pure)
        '''    
        elif text[line-subline].startswith('@'):
            if first_cpu == 1:
                instruction_list.append('-----------------------------------------------------------------------\n')
                instruction_list.append(text[line-subline])
                instruction_list.append('-----------------------------------------------------------------------\n')
                first_cpu = 0
        '''
    
    print 'last_line: ' + str(last_line)
    print ''
    instruction_list.append('\nlast_line: '+str(last_line)+'\n')
    
    i = 1
    while (1):
        if text[last_line-1-i].startswith('#'):
            if 'tmp2' in set(destpara(text[last_line-1-i])):
                last_tmp2_line = last_line-1   # The actual line from 0, +1
                break
        i += 1
    
    print 'slice_set(before):'
    print slice_set
    print ''
    instruction_list.append('\nslice_set(before): '+str(slice_set)+'\n')
    
    print 'last_tmp2_line: ' + str(last_tmp2_line)
    print ''
    instruction_list.append('\nlast_tmp2_line: '+str(last_tmp2_line)+'\n')
    
    if (recorded_line == last_tmp2_line):
        break
    
    recorded_line = last_tmp2_line
    
    line = last_tmp2_line
    stage += 1
    
    # XXX TODO: Maybe there are more than 1 address to load parameter, though some as shl_i32 parameter
    # TODO: add the stage to file result
    
    slice_set.clear()
    slice_set.add('tmp2')


f2 = open("./qemu30/qemu30_slicing_multi2.log","w")

i = len(instruction_list)-1
while(i != -1):
    #print instruction_list[i]
    f2.write(instruction_list[i])
    i -= 1
f2.close()

print 'final_slice_set:'
print slice_set



f3 = open("./qemu30/qemu30_slicing_pure.log","w")


i = len(instruction_pure)-1
while(i != -1):
    try:
        tmp2 = instruction_pure[i].split()[2].split(',')[1]
        if tmp2.startswith('*'):
            instruction_pure[i] = instruction_pure[i].replace(tmp2,'tmp2')
    except:
        pass
    f3.write(instruction_pure[i])
    i -= 1
f3.close()


