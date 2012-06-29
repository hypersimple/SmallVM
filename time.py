import time
a = 1
b = 2
c = []
c.append(1)
d = time.time()
for i in xrange(100000000):
    c[0] = (a + b)%6
e = time.time()

print e-d
