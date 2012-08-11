
sourcefile = "./qemu38/qemu38_ins_total"
destfile = "brcond38.txt"

f1 = open(sourcefile, "r")
text = f1.readlines()
f1.close()

result = []

count = 0
while(count<=len(text)-1):
    if text[count].startswith('# brcond'):
        result.append(text[count])
    count+=1
    
result=list(set(result))
    
f2 = open(destfile,"w")
for line in result:
    f2.write(line)
f2.close()
    
