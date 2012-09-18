# Keep CPU and hardware interrupt

def get_only_cpu(sourcefile,destfile):

    flag = 0
    flag2 = 1

    f = open(sourcefile, "r")
    text = f.readlines()
    f.close()
    
    count = 0
    while(count<=len(text)-1):
        try:
            if (text[count].startswith('@')) or (text[count].split()[1].startswith('v=')):
                if (text[count].startswith('@')):
                    if text[count].split()[2] != "CR3=1331e000": #XXX remove CR3=00039000
                        flag2 = 1
                    else:
                        flag2 = 0


                if flag2 == 0:
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
get_only_cpu('../qemu021.log','./qemu021/qemu021_cpu3.log')
