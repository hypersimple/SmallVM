from para_calc2 import *

# TODO: remove the constant number ($0x11) from slice_set / srcpara set

def slicing(instr_line_0, microop,slice_set,instr_list,slice_list):
    if set(destpara(microop)) <= slice_set: # If included in the slice_set
        slice_set = slice_set - set(destpara(microop))  #Minus of set
        slice_set = slice_set | set(srcpara(microop))   #Union of set
        
        #---
        if (instr_line_0,microop) in instr_list:
            print str(instr_line_0)+' '+microop
            print 'repeat! , slice_set: '
            print slice_set
            if len(slice_set) >= 2:
                print 'repeat error'
                # tmp12 tmp2 is not a problem, tmp6 is a problem
            print ''
            slice_set.clear()
            return (slice_set, instr_list)
        #---
            
        instr_list.append( (instr_line_0,microop) )
        if microop.startswith('# qemu_'):
            address2 = microop.split()[2].split(',')[1].split('{')[0]
            slice_list.append( (instr_line_0, address2) )
        #print str(instr_line_0)+' '+microop
    return (slice_set, instr_list)         # return a tuple


def do_slicing(text,init_line_0,slice_set,instr_list,slice_list):
    for subline in xrange(0,init_line_0 + 1):
        if len(slice_set) == 0:
            break
        if text[init_line_0-subline].startswith('#'):
            (slice_set, instr_list) = slicing(init_line_0-subline, text[init_line_0-subline], slice_set,instr_list,slice_list)
            
    return (slice_set, instr_list)


DataSource = "./qemu30/qemu30_ins_total"

f = open(DataSource, "r")
text = f.readlines()
f.close()


instr_list = []
slice_list = []
#tmp2_dict = {}

init_list = []


#init_list.append('eax')    # The destination parameter, and the line as the same
init_list.append('*0x6c87000')

slice_set = set(init_list)

slice_list.append( (4634232 - 1,'*0x6c87000') )    # Just an example

#line = 806670 - 1        # Set the interested line; 0x7e43b6d6; the destination para
init_line_0 = 4634232 - 1

stage = 0
#last_line_0 = 1
#recorded_line = 0

'''
# Put the first translation block into instr_list, to ensure tmp2 is correct
for j in xrange(0,44162):
    if text[j].startswith('#'):
        instr_list.append( (j,text[j]) )
'''

while(len(slice_list)!=0):
    print ''
    print '-------------------------------------------------'
    print 'stage: ' + str(stage)
    print '-------------------------------------------------'
    print ''
    
    print 'slice_list:'
    print slice_list
    
    if stage == 0:
        slice_list.pop(0)
    else:
        init_line_0 = slice_list.pop(0)[0]
        
        print 'init_line_0: ' + str(init_line_0)
        
        '''
        i = 1
        while (1):
            if text[last_line_0-i].startswith('#'):
                if 'tmp2' in set(destpara(text[last_line_0-i])):
                    last_tmp2_line = last_line_0-i
                    break
            i += 1

        init_line_0 = last_tmp2_line
        '''
        print 'slice_set:'
        print slice_set
        
        slice_set.clear()
        slice_set.add('tmp2')

        #print 'last_tmp2_line: ' + str(last_tmp2_line)
    
    (slice_set, instr_list) = do_slicing(text,init_line_0,slice_set,instr_list,slice_list)

    '''
    first_appear_line_0 = 0
    for element in slice_set:
        if element.startswith('*'):
            first_appear_line_0 = tmp2_dict[element]
                  
            slice_list.append( (first_appear_line_0,element) )
    '''
    
    slice_list = list(set(slice_list))
    
    '''
    if stage != 0:
        #if (recorded_line == last_tmp2_line):
            #break
        recorded_line = last_tmp2_line
    '''
    stage += 1



print 'final_slice_set:'
print slice_set

instr_list = list(set(instr_list))
instr_list.sort()

i = 0
f2 = open("./qemu30/qemu30_slicing_multi7.log","w")
while(i != len(instr_list)):
    f2.write(str(instr_list[i][0]))
    f2.write('  ')
    f2.write(instr_list[i][1])
    i += 1
f2.close()

i = 0
f3 = open("./qemu30/qemu30_slicing_pure7.log","w")
while(i != len(instr_list)):
    try:
        tmp2 = instr_list[i][1].split()[2].split(',')[1]
        if tmp2.startswith('*'):
            instr_list[i] = (instr_list[i][0], instr_list[i][1].replace(tmp2,'tmp2'))
    except:
        pass
    f3.write(instr_list[i][1])
    i += 1
f3.close()


