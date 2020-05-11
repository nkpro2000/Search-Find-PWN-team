from rsa_details import *

import Crypto.Util.number as u

for i in range(-10,10):
    for j in range(-10,10):
        if e1*i + e2*j == u.GCD(e1,e2) : break
    if e1*i + e2*j == u.GCD(e1,e2) : break

print (i, j)

if j<0 :
    m = (c2**i * u.inverse(c1, n)**(-j) ) % n

if i<0 :
    m = (c2**j * u.inverse(c1, n)**(-i) ) % n

print(m)
print(u.long_to_bytes(m))

if j<0 :
    m = (c1**i * u.inverse(c2, n)**(-j) ) % n

if i<0 :
    m = (c1**j * u.inverse(c2, n)**(-i) ) % n

print(m)
print(u.long_to_bytes(m))
