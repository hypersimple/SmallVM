#import linecache

#DataSource = "/home/cy/project/test4.txt"
DataSource = "/home/cy/project/qemu12_cutted_1.log"
DataWarehouse = "/home/cy/qemu_all_op.log"
#DataWarehouse = "/home/cy/project/test5.txt"
#DataDest = "/home/cy/project/test6.txt"


f = open(DataSource, "r")
text = f.readlines()  #Text is a string array

f1 = open(DataWarehouse, "r")

'''
text1 = f1.readlines(3000000)

f2 = open(DataDest, "w")
'''

#f2 = open ("/home/cy/project/test8.txt", "w") 
f2 = open ("/home/cy/project/qemu12_processed_1.log", "w") 

text1 = []
temp_result = []




def fetch(text,text1):
    text2 = []
    line2 = 0
    # XXX Seems should be from the second line
    for line in xrange(0,len(text)):
        if not text[line].startswith('Trace'):
            text2.append(text[line])
        else:
            if text[line-1].startswith('&'):
                not_found = 1
                address = text[line].split()[2].split('[')[1].split(']')[0]
                address = address.lstrip('0')
                
                
                for line1 in xrange(0,len(text1)):
                    if text1[line1].startswith(' ---- 0x' + address) and \
                    text1[line1-1].startswith('OP after'):
                        not_found = 0
                        for subline1 in xrange(-1,20000):
                            if text1[line1 + subline1] != '# end \n':   # There is a space after end!!!
                                text2.append(text1[line1 + subline1])
                            else:
                                break
                        text2.append('# end \n')
                    if not not_found:
                        break
                '''
                if(not_found):
                    print 'The TB is NOT found in this file chunk'
                '''

            text2.append(text[line])
    return text2

buf = []
#FILE_LINE_SIZE = 2000 #210846699 #Real Line Size
#total_count = 1

FILE_CHUNK_SIZE = 1000000
count = 0


#while (total_count <= FILE_LINE_SIZE):
for total_count, line in enumerate(f1):
    #line = linecache.getline(DataWarehouse, total_count)
    '''
    if total_count > 20000000: # To control the size
        break
    '''
    if line and count <= FILE_CHUNK_SIZE:
        text1.append(line)
        count += 1
        #total_count += 1
        continue
    elif line != '# end \n':
        text1.append(line)
        #total_count += 1
        continue
    elif line == '# end \n':
        text1.append(line)
        #total_count += 1
        count = 0
        '''
        for i in xrange(len(text)):
            print text[i],
        '''
        #print 'pre'
        text = fetch(text,text1)
        #print 'after'
        '''
        for i in xrange(len(text)):
            print text[i],
        '''
        #print buf
        #print
        text1 = []
        print 'total_count: '+str(total_count)+' | '+'chunk: '+str(total_count / 1000000)
        #break
        '''
        print text1
        print
        
        '''

for line2 in xrange(0,len(text)):
    f2.write(text[line2])
#f2.write('1111')
f2.close()


'''
for line in open(DataWarehouse):
    print 1
    if line and count <= 5:   # Use if line.strip() use judge the string is not '\n'
        text1.append(line)
        count += 1
        print '2'
        continue
    if line != '# end \n':
        text1.append(line)
        count += 1
        print '2'
    else:
        text1.append('# end \n')
        count += 1
        break
print str(count) + ' lines are read'
    #print len(text1)
    #print text1
    #print line
# XXX :The lines could be not continuous, NOT reach the '# end '

buf = fetch(text,text1)
for line2 in xrange(0,len(buf)):
    f2.write(buf[line2])
count = 0
text1 = []
'''



'''
buf = fetch(text, text1)
for line2 in xrange(0,len(buf)):
    f2.write(buf[line2])
'''
'''            
for i in xrange(0,len(text2)):
    f2.write(text2[i])
'''
