from replace_OP import *
from de_duplicate import *
#from cutlines_cr3 import *

def preprocess(sourcefile):
    sourcefile_name = sourcefile.split('.')[0]
    replace_OP(sourcefile,sourcefile_name+'_replace_OP.log')
    de_deplicate(sourcefile_name+'_replace_OP.log',sourcefile_name+'_de_duplicate.log')
    #cutlines_cr3(sourcefile1+'_de_duplicate.log',sourcefile1+'_cutlines_cr3.log',line)

#Warning:XXX: cannot be the ../ path
preprocess('qemu019_2.log')  #XXX: DO NOT use ../qemu35.log

