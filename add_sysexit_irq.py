DataSource = "./qemu21/qemu21_ins3"
#DataSource = "test_sysexit.txt"

f = open(DataSource, "r")
text = f.readlines()  #Text is a string array
f.close()

line = 0
while(line <= len(text)-1):
    if text[line].startswith(' ---- 0x804de904'):
        while( not text[line].startswith('# end ') ):
            line += 1
        text.insert(line+1,'# mov_i32 esp,ecx\n')
    line += 1
        
        
        
        
f2 = open("./qemu21/qemu21_ins4","w")
#f2 = open("test_sysexit_result.txt","w")
for line2 in text:
    f2.write(line2)
f2.close()
