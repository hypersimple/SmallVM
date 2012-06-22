import re

'''
DataWarehouse = "/home/cy/project/qemu13_replace_OP.log"
#DataWarehouse = "/home/cy/project/test4.txt"
f1 = open(DataWarehouse)
aaa=f1.read(500000000)
bbb=aaa.split('\n')
print bbb[1]
print len(bbb)
#print aaa
'''

#print int(19*0.1)
#print 3/4

mem1 = {}
#dict1[1] = 18
#print dict1[18]

def qemu_st32_mem(mem, loc, data):   #data, memory, memory location
    mem[loc] = data & 0xff
    mem[loc+1] = (data & 0xff00) >> 8
    mem[loc+2] = (data & 0xff0000) >> 16
    mem[loc+3] = (data & 0xff000000) >> 24
    #print '%x'%mem[loc+1]
    return mem    # Seems not needed

def qemu_ld32_mem(mem, loc):
    result = mem[loc]
    result += (mem[loc+1] << 8)
    result += (mem[loc+2] << 16)
    result += (mem[loc+3] << 24)
    return result


def qemu_st16_mem(mem, loc, data):
    mem[loc] = data & 0xff
    mem[loc+1] = (data & 0xff00) >> 8
    return mem
    
def qemu_ld16u_mem(mem, loc):
    result = mem[loc]
    result += (mem[loc+1] << 8)
    return result
    
    
def qemu_ld16s_mem(mem, loc):
    result = mem[loc]
    result += (mem[loc+1] << 8)
    if result & 0x8000 == 0x8000:   # Signed extension
        result += 0xffff0000
    return result
        
    
a = int('12348678',16)
#mem = 
qemu_st32_mem(mem1,5,a)
print '1111: %x'%mem1[5]
print '2222: %x'%mem1[6]
print '2222: %x'%mem1[7]
print '2222: %x'%mem1[8]

print '%x'%qemu_ld32_mem(mem1, 5)

print '%x'%qemu_ld16s_mem(mem1, 5)


a = int('12345678',16)
#print a
b = a & 255
#print '%x' % b
c = a & 65280
c = c >> 8
#print '%x' % c

c = c << 8
r = c + b
#print '%x' % r


'''

# qemu_ld16s tmp0,tmp2,$0x0
# qemu_ld16u tmp0,tmp2,$0x1

# qemu_st16 tmp0,tmp2,$0x1

'''





'''

def read_in_chunks(file_object, chunk_size=200000000): # 200000000, 21 blocks

    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data
        
        
def dohash(data):
    dict1 = {}
    result = re.findall('OP after liveness analysis:\n ---- 0x.+', data)
    for i in xrange(len(result)):
        address = result[i].split('x')[1]
        #print address
        dict1[address] = re.search('OP after liveness analysis:\n ---- 0x'+ address +'[\s\S]+?# end \n', data).group()
        #print dict1
        if '76fda015' in dict1:
            print 1
    return dict1
    

f1 = open(DataWarehouse)
count = 0

for piece in read_in_chunks(f1):

    dict1 = dohash(piece)

aaa=f1.readlines(2)
print aaa


dict2 = {}

dict2['1'] = '2'
print dict1['1']
if '1' in dict2:
    print 33333
'''
