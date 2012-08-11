import time

a=[]
b=''

print time.time()
for i in xrange(10000000):
    a.append(2)
print '%f'%time.time()

print time.time()
for i in xrange(10000000):
    b+='1'
print '%f'%time.time()
