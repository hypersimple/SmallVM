def check(text):
    #text2 = []
    #line2 = 0
    # XXX Seems should be from the second line
    #for line in xrange(0,len(text)):
    count = 0
    line = 0
    while(1):
        
        if (text[line].startswith('@') and text[line+1].startswith('@')) or\
        text[line].startswith('dohash # end error'):
            count += 1
            print line
            print text[line]
            
        line += 1
        if line+1 == len(text):
            break
    return count
    '''
    if line%1000 == 0:
        print line
    '''

DataSource = "qemu17_fetch_new.log"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array

print check(text)
