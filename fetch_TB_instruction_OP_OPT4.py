import re
import time

#DataSource = "/home/cy/project/test4.txt"
#DataSource = "/home/cy/project/qemu12_cutted_1.log"
#DataSource = "/home/cy/project/qemu12_cutted.log"
DataSource = "/home/cy/project/qemu15_cutlines.log"
#DataWarehouse = "/home/cy/qemu_all_op.log"
DataWarehouse = "/home/cy/project/qemu13_replace_OP.log"
#DataWarehouse = "/home/cy/project/test5.txt"
#DataDest = "/home/cy/project/test6.txt"


f = open(DataSource, "r")
text = f.readlines()  #Text is a string array

#f1 = open(DataWarehouse, "r")

#f2 = open ("/home/cy/project/test8_2.txt", "w") 
#f2 = open ("/home/cy/project/qemu12_processed_1_temp.log", "w")
f2 = open ("/home/cy/project/qemu15_fetch.log", "w")


def fetch(text,dict1):
    #text2 = []
    #line2 = 0
    # Seems should be from the second line, Done
    #for line in xrange(0,len(text)):
    line = 1
    while(1):
        #print '1 '+str(time.time())
        if text[line].startswith('Trace') and text[line-1].startswith('&'):
            #not_found = 1
            address = text[line].split()[2].split('[')[1].split(']')[0]
            address = address.lstrip('0')
            #print '2 '+str(time.time())
            if address in dict1:
            #print '3 '+str(time.time())
                text[line:line] = dict1[address]
            #print '4 '+str(time.time())
        line += 1
        if line == len(text):
            break
        if line%1000 == 0:
            print line
        #print '5 '+str(time.time())
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


def dohash(data):
    dict1 = {}
    result = re.findall('OP after liveness analysis:\n ---- 0x.+', data)
    for i in xrange(len(result)):
        address = result[i].split('x')[1]
        #print address
        dict1[address] = re.search('OP after liveness analysis:\n ---- 0x'+ address +'[\s\S]+?# end \n', data).group()
        #print dict1
        #if '76fda015' in dict1:
            #print 1
    return dict1


f1 = open(DataWarehouse)
count = 0

for piece in read_in_chunks(f1):

    dict1 = dohash(piece)

    text = fetch(text,dict1)
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
