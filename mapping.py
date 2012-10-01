#XXX: begin from line 0


# index (mapping) from the line number, begin from 0
def index(text):
    index0 = {}
    i = 0
    for line in xrange(len(text)):
        if text[line].startswith('@'):
            index0[i] = line
            i += 1
    return index0


# from 1 to 2
def mapping(text):
    index0 = {}
    index0 = index(text)
    indexall = {}
    
    for i in xrange(len(index0)):
        line = index0[i]
        line += 1
        temp1 = line
        while (not text[line].startswith('@')) and (line!=len(text)-1):
            line += 1
        temp2 = line - 1
        #print 'temp2',temp2
        indexall[i] = (temp1,temp2)

    return indexall


# from multiple to 1
def backmapping(text):
    index0 = {}
    index0 = index(text)
    indexall = {}
    
    for i in xrange(len(index0)):
        line = index0[i]
        line += 1
        temp1 = line
        while (not text[line].startswith('@')) and (line!=len(text)-1):
            line += 1
        temp2 = line - 1
        #print 'temp2',temp2
        for j in xrange(temp1,temp2+1):
            indexall[j] = i

    return indexall


