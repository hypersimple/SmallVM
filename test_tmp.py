from mem_func import *
import struct

memory_file = "/home/cy/xp19_1.dmp"

def get_memory(memory_file):
    f = open(memory_file, 'rb')
    data = f.read()
    f.close()
    return bytearray(data)

mem = get_memory(memory_file)
qemu_st32_mem(mem, 1, 2)

f = open('text.dmp','wb')
print 'Writing memory into file...'
for element in mem:
    f.write(struct.pack('B',element))
f.close()
