def remove_int(sourcefile,destfile):

    f1 = open(sourcefile, "r")
    text = f1.readlines()
    f1.close()

    text2 = []
    count = 0
    int_count = 0
    while(count<=len(text)-1):
        try:
            if text[count].split()[1].startswith('v='):
                #print text[count].split()[0]
                int_count += 1
                print '----------------------------------------------------'
                print 'v '+str(int_count)
                print text[count-1]
                print text[count]
                
            elif text[count].startswith('@') and text[count].split()[1].startswith('EIP=804df104'):
                print 'back 804df104 '+str(count+1)
                print text[count+1]
                int_count -= 1
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

    count1 = 0

    print '\nNow begin to de_duplicate\n'
    # de_duplicate
    for line in xrange(len(text2)):
        if text2[line].startswith('@'):
            for subline in xrange(1,200):
                if (line+subline) < len(text2):
                    if text2[line+subline] == text2[line]:
                        count1 += 1
                        #print text2[line]
                        text2[line+subline] = ''
                    else:
                        break
    print 'de_duplicate count: ' + str(count1)

    # Write to file
    f2 = open (destfile, "w") 
    for line in xrange(0,len(text2)):
        f2.write(text2[line])
    f2.close()
    
#remove_int("test_rm_int1.txt","test_rm_int_result.txt")
remove_int("./qemu40/qemu40_cpu.log","./qemu40/qemu40_rm_int.log")
