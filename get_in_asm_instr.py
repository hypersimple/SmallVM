f = open("../qemu25_in_asm.log", "r")
text = f.readlines()
f.close()


result = []

for line in text:
    try:
        result.append(line.split()[1])
    except:
        pass


result = list(set(result))

for j in result:
    print j
