def qemu_st32_mem(mem, loc, data):   #data, memory, memory location
    mem[loc] = data & 0xff
    mem[loc+1] = (data & 0xff00) >> 8
    mem[loc+2] = (data & 0xff0000) >> 16
    mem[loc+3] = (data & 0xff000000) >> 24
    #print '%x'%mem[loc+1]
    return mem    # Seems not needed

def qemu_st16_mem(mem, loc, data):
    mem[loc] = data & 0xff
    mem[loc+1] = (data & 0xff00) >> 8
    return mem


def qemu_ld32_mem(mem, loc):
    result = 0
    if loc in mem:
        result = mem[loc]
    if loc+1 in mem:
        result += (mem[loc+1] << 8)
    if loc+2 in mem:
        result += (mem[loc+2] << 16)
    if loc+3 in mem:
        result += (mem[loc+3] << 24)
    return result

    
def qemu_ld16u_mem(mem, loc):
    result = 0
    if loc in mem:
        result = mem[loc]
    if loc+1 in mem:
        result += (mem[loc+1] << 8)
    return result
    
    
def qemu_ld16s_mem(mem, loc):
    result = 0
    if loc in mem:
        result = mem[loc]
    if loc+1 in mem:
        result += (mem[loc+1] << 8)
    if result & 0x8000 == 0x8000:   # Signed extension
        result += 0xffff0000
    return result
