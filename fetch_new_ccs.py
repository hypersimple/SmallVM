def read_in_chunks(file_object, chunk_size=5000000):

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data


def fetch(text,dict1):
    line = 0
    while(1):
        if text[line].startswith('@') and text[line+1].startswith('@'): #in case the end of the file, todo
            address = text[line].split()[1].split('=')[1]
            address = address.lstrip('0')
            if address in dict1:
                text[line+1:line+1] = dict1[address]
        line += 1
        if line+1 == len(text):
            break
        if line%1000000 == 0:
            print line
    return text

# trim 00 before the address, DONE




def dohash(data):
    dict1 = {}
    text2 = data.split('\n')
    text2_size = len(text2)
    #print len(text2)
    for line in xrange(len(text2)):
        if text2[line] == 'OP after liveness analysis:':
            #print text2[line+1]
            address = text2[line+1].split('x')[1]
            dict1[address] = text2[line]+'\n'
            for subline in xrange(1,2000):
                if (line+subline)<len(text2):
                    if text2[line+subline] != '# end ':
                        dict1[address] += text2[line+subline]+'\n'
                    else:
                        dict1[address] += '# end \n'
                        break
                else:
                    print 'dohash # end error'
                    dict1[address] = 'dohash # end error'
                    break
        if line % 100000 == 0:
            print float(line)/float(text2_size)
    return dict1


def fetch_new(sourcefile,DataWarehouse,destfile):
    
    f = open(sourcefile, "r")
    text = f.readlines()  #Text is a string array
    f.close()
    
    count = 0
    f1 = open(DataWarehouse)
    for piece in read_in_chunks(f1):
        dict1 = dohash(piece)
        text = fetch(text,dict1)
        #print len(text)
        count += 1
        print 'The chunk number is: '+str(count)
        #if count == 2:
        #break
    f1.close()

    f2 = open (destfile, "w")
    for line2 in xrange(0,len(text)):
        f2.write(text[line2])
    f2.close()



origin = "qemu17.log"

sourcefile_name = origin.split('.')[0]
sourcefile = sourcefile_name+'_cutlines_cr3.log'
DataWarehouse = sourcefile_name+'_de_duplicate.log'
destfile = sourcefile_name+'_fetch_new.log'


fetch_new(sourcefile,DataWarehouse,destfile)




# XXX : The chunk may be not continuous for '# end \n', so should be executed twice with changed chunk_size


