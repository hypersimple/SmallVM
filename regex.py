import re, mmap

#f = open("/home/cy/project/test5.txt")
#f = open("/home/cy/qemu_all_op.log")
#text = f.read()
'''
with open("/home/cy/qemu_all_op.log") as f1:
    data = mmap.mmap(f.fileno(), 10000)
    result = re.search('OP after liveness analysis:\n ---- 0x'+'804dc10b'+'[\s\S]+?# end \n',text).group()
    
print result
'''
'''
[\s\S]*    match all the characters
 ?  minimum match
match: from the start to match
search: return the first match
findall: return a list of all results
'''

#file_object = open("/home/cy/project/test5.txt")

def read_in_chunks(file_object, chunk_size=5000000):
    """Lazy function (generator) to read a file piece by piece.
    Default chunk size: 1k."""
    while True:
        data = file_object.read(chunk_size)
        if not data:
            break
        yield data

#result=[]
f = open('/home/cy/qemu_all_op.log')
for piece in read_in_chunks(f):
    result = re.findall('OP after liveness analysis:\n ---- 0x'+'804dc10b'+'[\s\S]+?# end \n',piece)
    if result:
        break
if result:
    print result[len(result)-1]


#print text
matcher = re.compile('OP a[\s\S]+?# end \n')

matcher2 = re.compile('OP a[\s\S]+?asd')
aaa = "OP a ssdfds asd  asd"

#print matcher2.findall(aaa)[0]

m = re.match('OP a[\s\S]+?asd',aaa)
#print m.group()

#print re.search('OP after liveness analysis:\n ---- 0x'+'804dc10b'+'[\s\S]+?# end \n',text).group()
