import re

# XXX TODO FIXME Warning: The inserted CPU states are wrong, and the up address is inserted repeatedly, the data will bloat

# May need to be done iteratively

#DataSource = "/home/cy/project/test4.txt"
#DataSource = "/home/cy/project/qemu12_cutted_1.log"
#DataSource = "/home/cy/project/qemu12_cutted.log"
#DataSource = "/home/cy/project/qemu13_cutlines.log"
DataSource = "/home/cy/project/fetch3_test1.txt"
#DataWarehouse = "/home/cy/qemu_all_op.log"
#DataWarehouse = "/home/cy/project/qemu13_replace_OP.log"
DataWarehouse = "/home/cy/project/fetch3_test2.txt"
#DataWarehouse = "/home/cy/project/test5.txt"
#DataDest = "/home/cy/project/test6.txt"


f = open(DataSource, "r")
text = f.readlines()  #Text is a string array

#f1 = open(DataWarehouse, "r")

#f2 = open ("/home/cy/project/test8.txt", "w") 
#f2 = open ("/home/cy/project/qemu12_processed_1_temp.log", "w")
f2 = open ("/home/cy/project/fetch3_test_dest2.log", "w")


def fetch(text,text1):
    #text2 = []
    #line2 = 0
    # XXX Seems should be from the second line
    #for line in xrange(0,len(text)):
    line = 0
    while(1):
        if text[line].startswith('Trace') and text[line-1].startswith('&'):
            address1 = (text[line-2].split()[2].split('[')[1].split(']')[0]).lstrip('0')
            #not_found = 1
            address = (text[line].split()[2].split('[')[1].split(']')[0]).lstrip('0')
            result = re.search('OP after liveness analysis:\n ---- 0x'+ address1 +'[\s\S]+?OP after liveness analysis:\n ---- 0x'+ address +'[\s\S]+?# end \n', text1)    # Search from front
            if result:
                #not_found = 0
                #print 'leng'+str(len(result.group()))
                #print result.group()
                text[line:line] = result.group()
            else:
                print address+' NOT FOUND'
        line += 1
        if line == len(text):
            break
        if line%1000 == 0:
            print line
    return text
    '''
    if(not_found):
        print 'The TB is NOT found in this file chunk'
    '''

# XXX : The chunk may be not continuous for '# end \n', so should be executed twice with changed chunk_size

def read_in_chunks(file_object, chunk_size=200000000): # 200000000, 21 blocks

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


f1 = open(DataWarehouse)
count = 0

for piece in read_in_chunks(f1):
    text = fetch(text,piece)
    #print len(text)
    count += 1
    print 'The chunk number is: '+str(count)
    
    if count == 2:
        break
    
f1.close()   # XXX: new
#print len(text)
#print text[26945]

for line2 in xrange(0,len(text)):
    f2.write(text[line2])
f2.close()
#f2.write('1111')
