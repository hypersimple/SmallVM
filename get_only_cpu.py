def get_only_cpu(sourcefile,destfile):
    f = open(sourcefile, "r")
    text = f.readlines()
    f.close()
    count = 0
    while(count<=len(text)-1):
        if not text[count].startswith('@'):
            text[count] = ''
        count += 1
        
    f2 = open(destfile,"w")
    for line2 in text:
        f2.write(line2)
    f2.close()
    
    
get_only_cpu('qemu19_de_duplicate.log','qemu19_cpu.log')
