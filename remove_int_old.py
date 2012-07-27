def remove_int(sourcefile,destfile):

    f1 = open(sourcefile, "r")
    text = f1.readlines()
    f1.close()

    count = 0
    int_count = 0
    while(count<=len(text)-1):
        #print count

        try:
            #print text[count]
            if text[count] != '':
                if text[count].split()[1].startswith('v='):
                    print '-----------------------------'
                    print 'a_int number: '+text[count].split()[0]
                    print text[count]
                    print text[count-1]
                    print 'a_before EIP: '+text[count-1].split()[1]
                    
                    int_count += 1
                    print 'a_int_count '+str(int_count)
                    print '-----------------------------'
                    text[count] = ''
                    #for subline in xrange(1,5000000):
                    subline = 1
                    while subline != 5000000:
                        if text[count+subline].split()[1].startswith('v='):
                            #print text[count+subline].split()[0]
                            int_count += 1
                            print '-----------------------------'
                            print 'b_int number: '+text[count].split()[0]
                            if 
                            print 'b_before EIP: '+text[count+subline-1].split()[1]
                            print 'b_int_count '+str(int_count)
                            print '-----------------------------'
                            #print 'Multiple Interrupts!'
                            #print (count+1)
                            #break
                            text[count+subline] = ''
                        elif text[count+subline].startswith('@') and text[count+subline].split()[1].startswith('EIP=804df104'):
                            text[count+subline] = ''
                            int_count -= 1
                            print '-----------------------------'
                            print 'c_after EIP: '+text[count+subline+1].split()[1]
                            print 'c_int_count '+str(int_count)
                            print '-----------------------------'
                            #print 'int_count:'+str(int_count)
                            if int_count == 0:
                                text[count+subline+1] = ''
                                break
                        else:
                            text[count+subline] = ''
                        
                        subline += 1
        except:
            #pass
            raise
        count += 1

    f2 = open (destfile, "w") 
    for line2 in xrange(0,len(text)):
        f2.write(text[line2])
    f2.close()
    
    
#remove_int("test_rm_int1.txt","test_rm_int_result.txt")
remove_int("qemu25_cpu1.log","qemu25_rm_int.log")
