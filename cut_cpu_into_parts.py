
def cut_parts(start_line,end_line,sourcefile,destfile):
    f2 = open(destfile,"w")
    count = 0
    for line in open(sourcefile):
        if count == end_line:
            break
        elif count >= start_line-1:
            f2.write(line)
        count += 1
    f2.close()
    
    
def cut_cpu_into_parts(sourcefile,destfile_all,chunk_size,chunk_number):
    for i in xrange(0,chunk_number+1):
        cut_parts(1+i*chunk_size,(i+1)*chunk_size,sourcefile,destfile_all+str(i))

# chunk_number: wc -l, use the beginning number, usually
#cut_cpu_into_parts('qemu25_cpu1.log','./qemu25/qemu25_cpu_part_',100000,8)
