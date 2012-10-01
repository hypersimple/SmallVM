def qemu_st32_mem(mem, loc, data):   #data, memory, memory location
    #if not loc in mem:
        #print 'qemu_st32_mem error: loc: '+str(loc)
    try:
        if loc != 0xdeadbeef:
            mem[loc] = data & 0xff
            mem[loc+1] = (data & 0xff00) >> 8
            mem[loc+2] = (data & 0xff0000) >> 16
            mem[loc+3] = (data & 0xff000000) >> 24
            #print '%x'%mem[loc+1]
    except:
        print 'qemu_st32_mem error,loc: '+'%x'%loc
        #pass


def qemu_st32_vmem(vmem, loc_vir, data):   #data, memory, memory location
    #if not loc in mem:
        #print 'qemu_st32_mem error: loc: '+str(loc)
    try:
        if loc_vir != 0xdeadbeef:
            vmem[loc_vir] = data & 0xff
            vmem[loc_vir+1] = (data & 0xff00) >> 8
            vmem[loc_vir+2] = (data & 0xff0000) >> 16
            vmem[loc_vir+3] = (data & 0xff000000) >> 24
            #print '%x'%mem[loc+1]
    except:
        print 'qemu_st32_vmem error,loc_vir: '+'%x'%loc_vir
        #pass
        #raise
        

def qemu_st16_mem(mem, loc, data):
    try:
        if loc != 0xdeadbeef:
            mem[loc] = data & 0xff
            mem[loc+1] = (data & 0xff00) >> 8
    except:
        print 'qemu_st16_mem error,loc: '+'%x'%loc
        #pass


def qemu_st16_vmem(vmem, loc_vir, data):
    try:
        if loc_vir != 0xdeadbeef:
            vmem[loc_vir] = data & 0xff
            vmem[loc_vir+1] = (data & 0xff00) >> 8
    except:
        print 'qemu_st16_vmem error,loc_vir: '+'%x'%loc_vir
        #pass


def qemu_st8_mem(mem, loc, data):
    try:
        if loc != 0xdeadbeef:
            mem[loc] = data & 0xff
    except:
        print 'qemu_st8_mem error,loc: '+'%x'%loc
        #pass


def qemu_st8_vmem(vmem, loc_vir, data):
    try:
        if loc_vir != 0xdeadbeef:
            vmem[loc_vir] = data & 0xff
    except:
        print 'qemu_st8_vmem error,loc_vir: '+'%x'%loc_vir
        #pass


def qemu_ld32_mem(mem, loc):
    try:
        if loc == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = mem[loc]
            result += (mem[loc+1] << 8)
            result += (mem[loc+2] << 16)
            result += (mem[loc+3] << 24)
            return result
    except:
        print 'qemu_ld32_mem error,loc: '+'%x'%loc
        return 0xdeadbeef
        #pass
       
        
def qemu_ld32_vmem(vmem, loc_vir):
    try:
        if loc_vir == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = vmem[loc_vir]
            result += (vmem[loc_vir+1] << 8)
            result += (vmem[loc_vir+2] << 16)
            result += (vmem[loc_vir+3] << 24)
            return result
    except:
        print 'qemu_ld32_vmem error,loc_vir: '+'%x'%loc_vir
        return 0xdeadbeef
        #pass


    
def qemu_ld16u_mem(mem, loc):
    try:
        if loc == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = mem[loc]
            result += (mem[loc+1] << 8)
            return result
    except:
        print 'qemu_ld16u_mem error,loc: '+'%x'%loc
        return 0xdeadbeef
        #pass


def qemu_ld16u_vmem(vmem, loc_vir):
    try:
        if loc_vir == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = vmem[loc_vir]
            result += (vmem[loc_vir+1] << 8)
            return result
    except:
        print 'qemu_ld16u_vmem error,loc_vir: '+'%x'%loc_vir
        return 0xdeadbeef
        #pass


def qemu_ld16s_mem(mem, loc):
    try:
        if loc == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = mem[loc]
            result += (mem[loc+1] << 8)
            if result & 0x8000 == 0x8000:   # Signed extension
                result += 0xffff0000
            return result
    except:
        print 'qemu_ld16s_mem error,loc: '+'%x'%loc
        return 0xdeadbeef
        #pass


def qemu_ld16s_vmem(vmem, loc_vir):
    try:
        if loc_vir == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = vmem[loc_vir]
            result += (vmem[loc_vir+1] << 8)
            if result & 0x8000 == 0x8000:   # Signed extension
                result += 0xffff0000
            return result
    except:
        print 'qemu_ld16s_vmem error,loc_vir: '+'%x'%loc_vir
        return 0xdeadbeef
        #pass


def qemu_ld8u_mem(mem, loc):
    try:
        if loc == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = mem[loc]
            return result
    except:
        print 'qemu_ld8u_mem error,loc: '+'%x'%loc
        return 0xdeadbeef
        #pass


def qemu_ld8u_vmem(vmem, loc_vir):
    try:
        if loc_vir == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = vmem[loc_vir]
            return result
    except:
        print 'qemu_ld8u_vmem error,loc_vir: '+'%x'%loc_vir
        return 0xdeadbeef
        #pass



def qemu_ld8s_mem(mem, loc):
    try:
        if loc == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = mem[loc]
            if result & 0x80 == 0x80:   # Signed extension
                result += 0xffffff00
            return result
    except:
        print 'qemu_ld8s_mem error,loc: '+'%x'%loc
        return 0xdeadbeef
        #pass
        

def qemu_ld8s_vmem(vmem, loc_vir):
    try:
        if loc_vir == 0xdeadbeef:
            return 0xdeadbeef
        else:
            result = vmem[loc_vir]
            if result & 0x80 == 0x80:   # Signed extension
                result += 0xffffff00
            return result
    except:
        print 'qemu_ld8s_vmem error,loc_vir: '+'%x'%loc_vir
        return 0xdeadbeef
        #pass
