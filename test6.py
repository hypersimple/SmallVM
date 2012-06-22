a=[0,1,2,3]
#a[1:] = 'b'
a[1:1] = '5'
#print a
#print a[-1]

import re
#DataWarehouse = "/home/cy/project/qemu13_replace_OP.log"
DataWarehouse = "/home/cy/project/fetch3_test2.txt"

f1 = open(DataWarehouse)
text1 = f1.read()

address1 = '7c832e70'
address = '7c832e9d'

#address = '7c913253'

a=re.search('OP after liveness analysis:\n ---- 0x'+ address1 +'[\s\S]+?OP after liveness analysis:\n ---- 0x'+ address +'[\s\S]+?# end \n', text1)
if a:
    print a.group()
