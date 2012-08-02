
sourcefile = "./qemu35/qemu35_ins_total2"
destfile = "./qemu35/ld_i32_st_i32"

f1 = open(sourcefile, "r")
text = f1.readlines()
f1.close()

result = []

count = 0
while(count<=len(text)-1):
    if text[count].startswith('# ld_') or text[count].startswith('# st_'):
        result.append(text[count])
    count+=1
    
result=list(set(result))
    
f2 = open(destfile,"w")
for line in result:
    f2.write(line)
f2.close()
    
