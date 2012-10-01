# Keep CPU and hardware interrupt

def get_only_cpu(sourcefile,destfile):

    flag = 0
    
    f = open(sourcefile, "r")
    text = f.readlines()
    f.close()
    
    count = 0
    
    
    while( not text[count].startswith('@') ):
        count += 1
    
    
    while(count<=len(text)-1):
        try:
            if (text[count].startswith('@')) or (text[count].startswith('INT')):
                #if (text[count].startswith('@')):
                if 1:
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
get_only_cpu('../qemu019_5.log','./qemu019_5/qemu019_5_cpu_tmp.log')


sourcefile = './qemu019_5/qemu019_5_cpu_tmp.log'

f = open(sourcefile, "r")
text = f.readlines()
f.close()


print '\nNow begin to de_duplicate\n'
# de_duplicate
count1 = 0

for line in xrange(len(text)):
    if text[line].startswith('@'):
        for subline in xrange(1,200):
            if (line+subline) < len(text):
                if text[line+subline] == text[line]:
                    count1 += 1
                    #print text[line]
                    text[line+subline] = ''
                else:
                    break
print 'de_duplicate count: ' + str(count1)


destfile = './qemu019_5/qemu019_5_cpu.log'

f2 = open(destfile,"w")
for line in text:
    f2.write(line)
f2.close()
