
#XXX: The return value is NOT a set
# To calculate the destination parameter
def destpara(microop):
    destset = []
    if  microop.split()[1] == "mov_i32" or \
        microop.split()[1] == "movi_i32" or \
        microop.split()[1] == "movi_i64" or \
        \
        microop.split()[1] == "qemu_ld32" or \
        microop.split()[1] == "add_i32" or \
        \
        microop.split()[1] == "sub_i32" or \
        microop.split()[1] == "mul_i32" or \
        microop.split()[1] == "mul_i64" or \
        microop.split()[1] == "div_i32" or \
        \
        microop.split()[1] == "qemu_ld8u" or \
        microop.split()[1] == "qemu_ld8s" or \
        microop.split()[1] == "qemu_ld16u" or \
        microop.split()[1] == "qemu_ld16s" or \
        microop.split()[1] == "qemu_ld32u" or \
        microop.split()[1] == "qemu_ld32s" or \
        microop.split()[1] == "qemu_ld64" or \
        \
        microop.split()[1] == "neg_i32" or \
        microop.split()[1] == "and_i32" or \
        microop.split()[1] == "or_i32" or \
        microop.split()[1] == "xor_i32" or \
        microop.split()[1] == "not_i32" or \
        microop.split()[1] == "shl_i32" or \
        microop.split()[1] == "shr_i32" or \
        microop.split()[1] == "sar_i32" or \
        microop.split()[1] == "rotl_i32" or \
        microop.split()[1] == "rotr_i32" or \
        \
        microop.split()[1] == "deposit_i32" :
       
        destset.append( microop.split()[2].split(',')[0] )
    
    
    elif microop.split()[1] == "qemu_st8" or \
        microop.split()[1] == "qemu_st16" or \
        microop.split()[1] == "qemu_st32" or \
        microop.split()[1] == "qemu_st64" :
        
        #destset.append( microop.split()[2].split(',')[1] )
        destset.append( microop.split()[2].split(',')[1].split('{')[0] )    
    
    
    elif microop.split()[1] == "bswap32_i32" or \
        \
        microop.split()[1] == "ext8s_i32" or \
        microop.split()[1] == "ext8s_i32" or \
        microop.split()[1] == "ext16s_i32" or \
        microop.split()[1] == "ext16u_i32" or \
        microop.split()[1] == "ext32s_i64" or \
        microop.split()[1] == "ext32u_i64" :
        
        destset.append( microop.split()[2].split(',')[0] )
        destset.append( microop.split()[2].split(',')[1] )
    
    else:
        destset.append("$Unknown_dest_para")
        
    return destset
    
    

# To calculate the source parameter
def srcpara(microop):
    srcset = []
    
    if  microop.split()[1] == "mov_i32" or \
        microop.split()[1] == "movi_i32" or \
        microop.split()[1] == "movi_i64" or \
        \
        microop.split()[1] == "neg_i32" or \
        microop.split()[1] == "not_i32" :
        
        result = microop.split()[2].split(',')[1]
        if not result.startswith('$'):
            srcset.append(result)
        
        
    elif microop.split()[1] == "qemu_ld32" or \
        microop.split()[1] == "qemu_ld8u" or \
        microop.split()[1] == "qemu_ld8s" or \
        microop.split()[1] == "qemu_ld16u" or \
        microop.split()[1] == "qemu_ld16s" or \
        microop.split()[1] == "qemu_ld32u" or \
        microop.split()[1] == "qemu_ld32s" or \
        microop.split()[1] == "qemu_ld64" :
        #FIXME: Here we only consider ld32, ld16s, ld16u as described in the instruction_calc_pre2.py
        result = microop.split()[2].split(',')[1].split('{')[0]
        if not result.startswith('$'):
            srcset.append(result)


    elif microop.split()[1] == "qemu_st8" or \
        microop.split()[1] == "qemu_st16" or \
        microop.split()[1] == "qemu_st32" or \
        microop.split()[1] == "qemu_st64" :
        
        result = microop.split()[2].split(',')[0]
        if not result.startswith('$'):
            srcset.append(result)
        
    elif microop.split()[1] == "add_i32" or \
        \
        microop.split()[1] == "sub_i32" or \
        microop.split()[1] == "mul_i32" or \
        microop.split()[1] == "mul_i64" or \
        microop.split()[1] == "div_i32" or \
        \
        microop.split()[1] == "and_i32" or \
        microop.split()[1] == "or_i32" or \
        microop.split()[1] == "xor_i32" or \
        microop.split()[1] == "shl_i32" or \
        microop.split()[1] == "shr_i32" or \
        microop.split()[1] == "sar_i32" or \
        microop.split()[1] == "rotl_i32" or \
        microop.split()[1] == "rotr_i32" :
        
        #microop.split()[1] == "deposit_i32" :
        
        result = microop.split()[2].split(',')[1]
        if not result.startswith('$'):
            srcset.append(result)
            
        result = microop.split()[2].split(',')[2]
        if not result.startswith('$'):
            srcset.append(result)
            
        
    elif microop.split()[1] == "bswap32_i32" or \
        \
        microop.split()[1] == "ext8s_i32" or \
        microop.split()[1] == "ext8s_i32" or \
        microop.split()[1] == "ext16s_i32" or \
        microop.split()[1] == "ext16u_i32" or \
        microop.split()[1] == "ext32s_i64" or \
        microop.split()[1] == "ext32u_i64" :
        
        result = microop.split()[2].split(',')[0]
        if not result.startswith('$'):
            srcset.append(result)

        result = microop.split()[2].split(',')[1]
        if not result.startswith('$'):
            srcset.append(result)
        
        
    elif microop.split()[1] == "deposit_i32" :
        result = microop.split()[2].split(',')[2]
        if not result.startswith('$'):
            srcset.append(result)
        
    else:
        srcset.append("$Unknown_src_para")
        
    return srcset
