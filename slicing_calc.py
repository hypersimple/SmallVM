from instr_new_no_data import *
from para_calc import *
#import time

def init_tmp(tmp):
    for i in xrange(0,50):
        tmp['tmp'+str(i)] = 0xdeadbeef


def slicing_calc(text,init_text,line,dict1):
    reg = {}
    tmp = {}
    init_tmp(tmp)
    instruction_list = []
    init_list = []
    init_list.append('eax')    # XXX
    slice_set = set(init_list)
    init_text = execute_all(init_text,init_text[0],reg,tmp)
    #print init_text
    slice_set = init_slicing(init_text,slice_set,instruction_list)
    
    while(line != -1):
        if text[line].startswith('@'):
            address = text[line].split()[1].split('=')[1]
            address = address.lstrip('0')
            if address in dict1:
                tb = dict1[address]
                tb2 = tb.split('\n')
                #a = time.time()
                tb2 = execute_all(tb2,text[line],reg,tmp)
                #b = time.time()
                slice_set = slicing_back(line,tb2,slice_set,instruction_list)
                #c = time.time()
                #print 'b-a: %.10f'%(b-a)
                #d = time.time()
                #print 'c-b: %.10f'%(c-b)
                #print 'd-c: %.30f'%(d-c)
            else:
                print 'address NOT found in dict1'
            line -= 1
            if len(instruction_list) % 100 == 0:
                write_to_file(instruction_list)
                instruction_list = []
    return instruction_list


def write_to_file(instruction_list):
    f2 = open('result_tmp2.txt',"a")
    for i in xrange(len(instruction_list)):
        f2.write(instruction_list[i]+'\n')
    f2.close()


def slicing(instr_line, microop,slice_set,instruction_list):
    if set(destpara(microop)) <= slice_set: # If included in the slice_set
        slice_set = slice_set - set(destpara(microop))  #Minus of set
        slice_set = slice_set | set(srcpara(microop))   #Union of set
        remove_tmp = []
        for i in slice_set:
            if i.startswith('$'):
                remove_tmp.append(i)
        for j in remove_tmp:
            slice_set.remove(j)
        instruction_list.append(str(instr_line + 1)+' '+microop)
        #instruction_list.append(microop)
        
        print str(instr_line + 1)+' '+microop
        #print slice_set
        
    return (slice_set, instruction_list)
        

def slicing_back(line,text,slice_set,instruction_list):
    line2 = len(text)-1
    for subline in xrange(0,line2):
        if text[line2-subline].startswith('#'):
            (slice_set, instruction_list) = slicing(line, text[line2-subline], slice_set,instruction_list)
    return slice_set


def init_slicing(text,slice_set,instruction_list):
    line2 = len(text)-1
    line = 0
    for subline in xrange(0,line2):
        if text[line2-subline].startswith('#'):
            (slice_set, instruction_list) = slicing(line, text[line2-subline], slice_set,instruction_list)
    return slice_set


    
def dohash(data):
    dict1 = {}
    text2 = data.split('\n')
    text2_size = len(text2)
    #print len(text2)
    for line in xrange(len(text2)):
        if text2[line] == 'OP after liveness analysis:':
            #print text2[line+1]
            address = text2[line+1].split('x')[1]
            dict1[address] = text2[line]+'\n'
            for subline in xrange(1,2000):
                if text2[line+subline] != '# end ':
                    dict1[address] += text2[line+subline]+'\n'
                else:
                    dict1[address] += '# end \n'
                    break
        if line % 1000000 == 0:
            print float(line)/float(text2_size)
    return dict1

    
def main(sourcefile,init_text_file,line,destfile):
    f1 = open(sourcefile)
    data = f1.read()
    f1.close()
    dict1 = dohash(data)
    data = 0     # To free memory

    f = open(sourcefile, "r")
    text = f.readlines()  #Text is a string array
    f.close()
    
    f = open(init_text_file,"r")
    init_text = f.readlines()
    f.close()
    
    instruction_list = slicing_calc(text,init_text,line,dict1)
    
    
    f2 = open(destfile,"w")
    i = len(instruction_list)-1
    while(i != -1):
        #print instruction_list[i]
        f2.write(instruction_list[i])
        i -= 1
    f2.close()


#----------------------------------------------------------------------
sourcefile = 'qemu17_de_duplicate.log'
init_text_file = 'test_slicing_calc.txt'
line = 11962423 - 1
destfile = 'qemu17_slicing4.log'
#----------------------------------------------------------------------
main(sourcefile,init_text_file,line,destfile)

