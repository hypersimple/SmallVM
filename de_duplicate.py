'''
def read_in_chunks(file_object, chunk_size=50000000): # 200000000, 21 blocks

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
'''

def de_deplicate(sourcefile,destfile):

    f1 = open(sourcefile, "r")
    text = f1.readlines()
    f1.close()

    for line in xrange(len(text)):
        if text[line].startswith('@'):
            for subline in xrange(1,200):
                if (line+subline) < len(text):
                    if text[line+subline] == text[line]:
                        text[line+subline] = ''
                    else:
                        break
                        
    for line in xrange(len(text)):
        if text[line].startswith('# exit_tb'):
            text[line] = '# exit_tb\n'

    f2 = open (destfile, "w") 
    for line2 in xrange(0,len(text)):
        f2.write(text[line2])
    f2.close()
'''
sourcefile = "/home/cy/qemu17.log"
destfile = "/home/cy/project/qemu17_de_duplicate.log"

de_deplicate(sourcefile,destfile)
'''
