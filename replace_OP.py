
#DataSource = "/home/cy/project/qemu12_processed_ccs.log"
#DataSource = "/home/cy/project/qemu13.log"
#DataSource = "/home/cy/project/qemu12_cutted_1.log"
#DataSource = "/home/cy/project/qemu12_cutted.log"
#DataWarehouse = "/home/cy/qemu_all_op.log"
#DataWarehouse = "/home/cy/project/test5.txt"
#DataDest = "/home/cy/project/qemu12_ready.log"
#DataDest = "/home/cy/project/qemu13_replace_OP.log"

# XXX: Note: we should purge the beginning and the end of the text because of the incomplete "OP:" statements

def replace_OP(sourcefile,destfile):
    f1 = open(sourcefile, "r")
    text = f1.readlines()
    f1.close()
    #result = re.search('OP:[\s\S]+?# end \n', text_string)
    for line in xrange(0,len(text)):
        if text[line] == "OP:\n":
            text[line] = ''
            for subline in xrange(1,20000):
                if not text[line+subline].startswith('OP after'):
                    text[line+subline] = ''
                else:
                    break
    #return text
    f2 = open (destfile, "w")
    for line2 in xrange(0,len(text)):
        f2.write(text[line2])
    f2.close()


'''
f = open(DataSource, "r")
text = f.readlines()
f.close()

text = replace_OP(text)

f2 = open (DataDest, "w")
for line2 in xrange(0,len(text)):
    f2.write(text[line2])

f2.close()
'''
