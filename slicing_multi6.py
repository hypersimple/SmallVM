from para_calc2 import *
from mapping import *

# now include code blocks

# calculate only the final address
# TODO: remove the constant number ($0x11) from slice_set / srcpara set

def slicing(instr_line_0, microop,slice_set,instr_list,tmp2_dict,index_list,index):
    if set(destpara(microop)) <= slice_set: 
        
        #if index[instr_line_0] in index_list:  #wrong
        if (instr_line_0,microop) in instr_list:
            slice_set = slice_set - set(destpara(microop)) 
            print 'repeat!!!!!!!!!!!!!!!'
        else:
            slice_set = slice_set - set(destpara(microop)) 
            slice_set = slice_set | set(srcpara(microop)) 

            instr_list.append( (instr_line_0,microop) )
            
            block = index[instr_line_0]
            if not block in index_list:
                index_list.append( index[instr_line_0] )
        
        
        if microop.startswith('# qemu_ld'):
            address2 = microop.split()[2].split(',')[1].split('{')[0]
            tmp2_dict[address2] = instr_line_0
        print '#'+str(instr_line_0+1)+' '+microop
        #print microop
    return (slice_set, instr_list)


def do_slicing(text,init_line_0,slice_set,instr_list,tmp2_dict,index_list,index):
    for subline in xrange(0,init_line_0 + 1):
        if len(slice_set) == 0:
            break
        if text[init_line_0-subline].startswith('#'):
            (slice_set, instr_list) = slicing(init_line_0-subline, text[init_line_0-subline], slice_set,instr_list,tmp2_dict,index_list,index)
            
    return (slice_set, instr_list)


DataSource = "./qemu019_5/qemu019_5_ins2.log"

f = open(DataSource, "r")
text = f.readlines()
f.close()



index = {}
index = backmapping(text)

index_list = []



instr_list = []
slice_list = []
tmp2_dict = {}

init_list = []

temp1 = []
slice_history = set(temp1)


#init_list.append('eax')    # The destination parameter, and the line as the same
init_list.append('tmp0')
init_line_0 = 17347796 - 1   

slice_set = set(init_list)



slice_list.append( ( 17347796 - 1,'tmp0') )  


#this should include all the string data, and brcond
# The slicesource file, includding line and set
SliceSource = "./qemu019_5/slicing_source.txt"

f = open(SliceSource, "r")
text1 = f.readlines()
f.close()

for line in text1:
    para1 = line.split()[0]
    para2 = line.split()[1]
    slice_list.append( (int(para1),para2) )





stage = 0
last_line_0 = 1
#recorded_line = 0

'''
#--
# Put the first translation block into instr_list, to ensure tmp2 is correct
for j in xrange(0,44162):
    if text[j].startswith('#'):
        instr_list.append( (j,text[j]) )
#--
'''

while(len(slice_list)!=0):
    print ''
    print '-------------------------------------------------'
    print 'stage: ' + str(stage)
    print '-------------------------------------------------'
    print ''
    
    if stage == 0:
        slice_list.pop(0)
    else:
        last_line_0 = slice_list.pop(0)[0]
        
        print 'last_line_0: ' + str(last_line_0)
        
        i = 1
        while (1):
            if text[last_line_0-i].startswith('#'):
                if 'tmp2' in set(destpara(text[last_line_0-i])):
                    last_tmp2_line = last_line_0-i
                    break
            i += 1

        init_line_0 = last_tmp2_line
        slice_set.clear()
        slice_set.add('tmp2')

        print 'last_tmp2_line: ' + str(last_tmp2_line)
    
    (slice_set, instr_list) = do_slicing(text,init_line_0,slice_set,instr_list,tmp2_dict,index_list,index)

    first_appear_line_0 = 0
    for element in slice_set:
        if element.startswith('*'):
            first_appear_line_0 = tmp2_dict[element]
            #print 'first_appear_line_0'
            #print first_appear_line_0
            
            #print 'dict:'
            #print tmp2_dict
            '''
            for line1 in xrange(0,len(text)):
                try:
                    address = text[line1].split()[2].split(',')[1].split('{')[0]
                    if address == element:
                        first_appear_line_0 = line1
                        break
                except:
                    pass
                line1 += 1
            '''   
            if (first_appear_line_0,element) in slice_history:
                pass
            else:
                slice_list.append( (first_appear_line_0,element) )
                slice_history.add( (first_appear_line_0,element) )

    slice_list = list(set(slice_list))
    slice_list.sort()
    
    print 'slice_list:'
    print slice_list
    '''
    if stage != 0:
        #if (recorded_line == last_tmp2_line):
            #break
        recorded_line = last_tmp2_line
    '''
    stage += 1

    print 'slice_set:'
    print slice_set


print 'final_slice_set:'
print slice_set

print 'slice_history:'
print slice_history




instr_list = list(set(instr_list))
instr_list.sort()

i = 0
f2 = open("./qemu019_5/qemu019_5_slicing.log","w")
while(i != len(instr_list)):
    f2.write(str(instr_list[i][0]))
    f2.write('  ')
    f2.write(instr_list[i][1])
    i += 1
f2.close()

instr_list = []






index_list = list(set(index_list))
index_list.sort()

i = 0
f2 = open("./qemu019_5/qemu019_5_slicing_block.log","w")
while(i != len(index_list)):
    f2.write(str(index_list[i]))
    f2.write('\n')
    i += 1
f2.close()




'''
i = 0
f3 = open("./qemu38/qemu38_slicing3_pure2.log","w")
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

'''

