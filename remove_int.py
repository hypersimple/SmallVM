def remove_int(sourcefile,destfile):

    f1 = open(sourcefile, "r")
    text = f1.readlines()
    f1.close()

    text1 = []
    text2 = []
    count = 730976 - 1
    int_count = 0
    record = ''
    
    while(count>=0):
        try:
            if text[count].startswith('@') and text[count].split()[1].startswith('EIP=804df104'):
                if int_count == 0:
                    int_count = 1
                    record = text[count+1]
            elif text[count].split()[1].startswith('v='):
                if int_count == 1:
                    if text[count-1] == record:
                        int_count = 0
                        count -= 1
                elif int_count == 0:
                    text1.append(text[count])
            elif int_count == 0:
                text1.append(text[count])
        except:
            raise
        count -= 1
    
    
    count = 730976 - 1
    int_count = 0
    record = ''
    while(count<=len(text)-1):
        try:
            if text[count].split()[1].startswith('v='):
                if int_count == 0:
                    print text[count].split()[0]
                    int_count = 1
                    record = text[count-1]
                    #print 'v '+str(int_count)
            elif text[count].startswith('@') and text[count].split()[1].startswith('EIP=804df104'):
                if int_count == 1:
                    if text[count+1] == record:
                        print 'back '+str(count+1)
                        int_count = 0
                        count += 1
                        #print 'b '+str(int_count)
                elif int_count == 0:
                    text2.append(text[count])
            elif int_count == 0:
                text2.append(text[count])
        except:
            #pass
            raise
        count += 1

    f2 = open (destfile, "w") 
    # TODO:two 7c810e17
    maxline = len(text1)-1
    for line in xrange(0,len(text1)):
        f2.write(text1[maxline-line])
    for line in xrange(0,len(text2)):
        f2.write(text2[line])
    f2.close()
    
    
#remove_int("test_rm_int1.txt","test_rm_int_result.txt")
remove_int("qemu25_cpu1.log","qemu25_rm_int.log")
