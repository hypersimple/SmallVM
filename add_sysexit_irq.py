DataSource = "./qemu25/qemu25_ins2_0"
#DataSource = "test_sysexit.txt"

# XXX: something to do with sysenter

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array
f.close()

line = 0
while(line <= len(text)-1):
    if text[line].startswith(' ---- 0x804de904'):
        print 'FOUND'
        print ''
        while( not text[line].startswith('# end ') ):
            line += 1
        text.insert(line+1,'# mov_i32 esp,ecx\n')
    line += 1
        
        
        
        
f2 = open("./qemu25/qemu25_tmp","w")
#f2 = open("test_sysexit_result.txt","w")
for line2 in text:
    f2.write(line2)
f2.close()
