from para_calc import *

# TODO: remove the constant number ($0x11) from slice_set / srcpara set
# remove the cc_src cc_op cc_dst

def slicing_forward(instr_line, microop,slice_set,instruction_list):
    if srcpara(microop)[0] != 'cc_src'\
    and destpara(microop)[0] != 'cc_src'\
    and srcpara(microop)[0] != 'cc_dst'\
    and destpara(microop)[0] != 'cc_dst'\
    and set(srcpara(microop)) <= slice_set: # If included in the slice_set

        #print destpara(microop)[0]
        slice_set = slice_set - set(srcpara(microop))  #Minus of set
        slice_set = slice_set | set(destpara(microop))   #Union of set
        instruction_list.append(str(instr_line)+' '+microop)
        
        print str(instr_line)+' '+microop
        print slice_set
        
    return (slice_set, instruction_list)                # return a tuple



#DataSource = "/home/cy/project/parsed_test.txt"
DataSource = "/home/cy/project/qemu15_instr_calc.log"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array



instruction_list = []

init_list = []
#init_list.append('*0x12f5f0')    # The source parameter, and the line as the same
init_list.append('$0x415410')

slice_set = set(init_list)


#line = 310653 - 1
#line = 312408 - 1
line = 48 - 1  #2403 - 1        # Set the interested line; 0x7e43b6d6; the destination para
for subline in xrange(0,len(text)):   # FIXME: the end line
    if text[line+subline].startswith('#'):
        (slice_set, instruction_list) = slicing_forward(line+subline+1, text[line+subline],slice_set,instruction_list)
        

### XXX: cc_src cc_dst are big problems
'''
 ---- 0x7c802510
# mov_i32 tmp2,esp
# qemu_ld32 tmp0,*0x12f5f0,$0x1
# movi_i32 tmp12,$0x4
# add_i32 tmp4,esp,tmp12
# mov_i32 esp,tmp4
# st_i32 tmp0,env,$0x20
# movi_i32 cc_op,$0x10
# exit_tb $0x0
# end 
'''

#print slice_set
#(slice_set, instruction_list) = slicing("# add_i32 tmp3,tmp2,tmp12",slice_set,instruction_list)
#(slice_set, instruction_list) = slicing("# add_i32 tmp2,tmp2,tmp13",slice_set,instruction_list)

#print instruction_list

'''
for i in xrange(0,len(instruction_list)):
    print instruction_list[i]

print slice_set
'''
