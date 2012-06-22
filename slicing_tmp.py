from para_calc import *

# TODO: remove the constant number ($0x11) from slice_set / srcpara set

def slicing(instr_line, microop,slice_set,instruction_list):
    if set(destpara(microop)) <= slice_set: # If included in the slice_set
        #print 1
        slice_set = slice_set - set(destpara(microop))  #Minus of set
        slice_set = slice_set | set(srcpara(microop))   #Union of set
        instruction_list.append(str(instr_line)+' '+microop)
        
        print str(instr_line)+' '+microop
        print slice_set
        
    return (slice_set, instruction_list)                # return a tuple



#DataSource = "/home/cy/project/parsed_test.txt"
DataSource = "/home/cy/project/qemu15_instr_calc3.log"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array



instruction_list = []

init_list = []
init_list.append('eax')    # The destination parameter, and the line as the same

slice_set = set(init_list)


#line = 310653 - 1
#line = 312408 - 1
line = 1896129 - 1        # Set the interested line; 0x7e43b6d6; the destination para
for subline in xrange(0,line+1):
    if text[line-subline].startswith('#'):
        (slice_set, instruction_list) = slicing(line-subline+1, text[line-subline],slice_set,instruction_list)
        



#print slice_set
#(slice_set, instruction_list) = slicing("# add_i32 tmp3,tmp2,tmp12",slice_set,instruction_list)
#(slice_set, instruction_list) = slicing("# add_i32 tmp2,tmp2,tmp13",slice_set,instruction_list)

#print instruction_list

'''
for i in xrange(0,len(instruction_list)):
    print instruction_list[i]

print slice_set
'''
