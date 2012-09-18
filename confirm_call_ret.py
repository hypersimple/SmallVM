DataSource = "019call_ret.txt"

f = open(DataSource, "r")
text = f.readlines()
f.close()

stack = []

for i in xrange(len(text)):
    type1 = text[i].split()[2]
    try:
        if type1 == 'call':
            call_addr = text[i].split()[4]
            stack.append(call_addr)
        elif type1 == 'ret':
            ret_addr = text[i].split()[4]
            ret_addr1 = stack.pop()
            if ret_addr == ret_addr1:
                pass
            else:
                print 'Wrong!'
                print text[i]
    except:
        #pass
        print 'Wrong!'
        print text[i]
