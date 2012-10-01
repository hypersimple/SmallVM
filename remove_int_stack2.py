# remove_int_stack, including the micro-op version

def next_cpu(text,count):
    try:
        for i in xrange(1,2000):
            if text[count+i].startswith('INT'):
                return count+i
            elif text[count+i].startswith('@'):
                return count+i
        print 'ERROR1'
    except:
        print 'last_line'
        return (len(text)-1)
        
        
def remove_int(sourcefile,destfile):

    f1 = open(sourcefile, "r")
    text = f1.readlines()
    f1.close()

    text2 = []
    count = 0
    int_count = 0
    
    
    while( not text[count].startswith('@') ):
        count += 1


    
    # stage 1 duplicate
    count1 = 0
    for line in xrange(len(text)):
        if text[line].startswith('@'):
            i=0
            while(i<=10):
                next_line = next_cpu(text,line)
                if text[next_line] == text[line]:
                    count1 += 1
                    for j in xrange(line,next_line):
                        text[j] = ''
                else:
                    break
                line = next_line
                i += 1
    print 'de_duplicate count(stage1): ' + str(count1)



    while(count<=len(text)-1):
        try:
            if text[count].startswith('INT') and text[count].split()[4] == 'i=0':
                #print text[count].split()[0]
                int_count += 1
                print '----------------------------------------------------'
                print 'v '+str(int_count)
                print text[count-1]
                print text[count]
                
            elif text[count].startswith('@') and text[count].split()[1].startswith('EIP=804df104'):
                print 'back 804df104 '+str(count+1)
                print text[next_cpu(text,count)]
                int_count -= 1
                
                
                # jump after two blocks
                count = next_cpu(text,count)-1
                '''
                if not text[count+1].startswith('INT'):
                    count += 1
                    count = next_cpu(text,count)-1
                '''
                
                print 'b '+str(int_count)
                print '----------------------------------------------------'
            
            elif int_count == 0:
                text2.append(text[count])

            '''    
            elif text[count].startswith('@') and text[count].split()[1].startswith('EIP=804dea5d'):
                print 'back 804dea5d '+str(count+1)
                print text[count+1]
                int_count -= 1
                print 'b '+str(int_count)
                print '----------------------------------------------------'
            '''
        except:
            #pass
            raise
        count += 1



    # Write to file
    f2 = open(destfile, "w")
    for line in xrange(0,len(text2)):
        f2.write(text2[line])
    f2.close()
    
#remove_int("test_rm_int1.txt","test_rm_int_result.txt")
remove_int("../qemu019_5.log","./qemu019_5/qemu019_5_ins_tmp.log")





sourcefile = "./qemu019_5/qemu019_5_ins_tmp.log"

f1 = open(sourcefile, "r")
text = f1.readlines()
f1.close()


# stage 2 duplicate
count1 = 0
for line in xrange(len(text)):
    if text[line].startswith('@'):
        i=0
        while(i<=10):
            next_line = next_cpu(text,line)
            if text[next_line] == text[line]:
                count1 += 1
                for j in xrange(line,next_line):
                    text[j] = ''
            else:
                break
            line = next_line
            i += 1
print 'de_duplicate count(stage2): ' + str(count1)



destfile = "./qemu019_5/qemu019_5_ins.log"

f2 = open(destfile, "w")
for line in xrange(0,len(text)):
    f2.write(text[line])
f2.close()


