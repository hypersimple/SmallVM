def check(text):
    #text2 = []
    #line2 = 0
    # XXX Seems should be from the second line
    #for line in xrange(0,len(text)):
    count = 0
    line = 0
    while(1):
        
        if text[line].startswith('Trace') and text[line-1].startswith('&'):
            count += 1
            print line
            print text[line]
            
        line += 1
        if line == len(text):
            break
    return count
    '''
    if line%1000 == 0:
        print line
    '''

#DataSource = "/home/cy/project/qemu12_processed_ccs.log"
DataSource = "/home/cy/project/qemu15_fetch.log"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array

print check(text)
