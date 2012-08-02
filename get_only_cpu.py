# Keep CPU and hardware interrupt

def get_only_cpu(sourcefile,destfile):

    flag = 0
    
    f = open(sourcefile, "r")
    text = f.readlines()
    f.close()
    
    count = 0
    while(count<=len(text)-1):
        try:
            if (text[count].startswith('@')) or (text[count].split()[1].startswith('v=')):
                if (text[count].startswith('@')):
                    if flag == 0:
                        start_line = count
                        flag = 1
                    end_line = count
                count += 1    
                continue
        except:
            pass
        text[count] = ''
        count += 1
        
    f2 = open(destfile,"w")
    for count2 in xrange(start_line, end_line+1):
        f2.write(text[count2])
    f2.close()

    
#get_only_cpu('qemu25_de_duplicate.log','qemu25_cpu.log')
#get_only_cpu('test_rm_int.txt','test_rm_int1.txt')
get_only_cpu('../qemu37.log','./qemu37/qemu37_cpu.log')
