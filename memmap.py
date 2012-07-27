from mem_func import *

def preprocess_memmap(memmap_file,memmap_table,psscan_table):
    f = open(memmap_file, "r")
    text = f.readlines()
    f.close()
    
    for line in xrange(0,len(text)):
        try:
            if text[line].split()[1] == 'pid:':
                pid = text[line].split()[2]
                cr3 = pidmap(pid,psscan_table)
            if text[line].startswith('0x'):
                memmap_table[int(text[line].split()[0],16),cr3] = int(text[line].split()[1],16)
        except:
            pass
            
            
            
def memmap(virtual,cr3,memmap_table):
    if ((virtual & 0xfffff000),cr3) in memmap_table:
        return memmap_table[(virtual & 0xfffff000),cr3] + (virtual & 0x00000fff)
    else:
        #print 'memmap error: ' + '0x%x'%(virtual) + ' | cr3: ' +cr3
        # Too many errors
        return 0x01111111


def pidmap(pid,psscan_table):
    if pid in psscan_table:
        return psscan_table[pid]
    else:
        print 'pidmap error, pid: ' + str(pid)


def preprocess_psscan(psscan_file,psscan_table):
    f = open(psscan_file, "r")
    text = f.readlines()
    f.close()
    for line in xrange(len(text)):
        if text[line].startswith('0x'):
            pid = text[line].split()[2]
            cr3 = text[line].split()[4].split('x')[1]
            psscan_table[pid] = cr3  # return PID


memmap_table = {}   # the memory mapping table
psscan_table = {}


psscan_file = "/home/cy/psscan30"
memmap_file = "/home/cy/memmap30_2"

preprocess_psscan(psscan_file,psscan_table)
preprocess_memmap(memmap_file,memmap_table,psscan_table)

# less psscan30
# XXX: Firefox
# pid = '464' psscan29
pid = '2040'
cr3 = pidmap(pid,psscan_table)
#print cr3

loc_vir = \
0x9000018


print '0x%x'%memmap(loc_vir,cr3,memmap_table)


