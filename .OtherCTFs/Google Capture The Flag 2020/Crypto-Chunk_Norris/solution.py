import os
os.chdir(os.path.dirname(__file__))

### Crypto
import random
import Crypto.Util.number as u
import gmpy2

### given
with open("output.txt") as vars:
    exec(vars.read()) # n, e, c

a = 0xe64a5f84e2762be5
chunk_size = 64

def gen_prime(bits):
  s = random.getrandbits(chunk_size)
  while True:
    s |= 0xc000000000000001
    p = 0
    for _ in range(bits // chunk_size):
      p = (p << chunk_size) + s
      s = a * s % 2**chunk_size
    if gmpy2.is_prime(p):
      return p

### Try
bits = 1024

def gen_prime():
    return gen_prime(bits)

def mk_prime(s):
    while True:
        s |= 0xc000000000000001
        p = 0
        for _ in range(bits // chunk_size):
            p = (p << chunk_size) + s
            s = a * s % 2**chunk_size
        if gmpy2.is_prime(p):
            return p

ss = lambda :random.getrandbits(chunk_size)

def try_patten(st, end, old=None):
    if old is None:
        old = list()
    for i in range(st, end+1):
        val = mk_prime(i)
        try:
            print(i, old.index(val))
        except ValueError:
            print(i, len(old))
            old.append(val)

"""
if s % 2 == 1:
    mk_prime(s) == mk_prime(s-1)
else:
    mk_prime(s) == mk_prime(s+1)
"""

from itertools import combinations_with_replacement
def try_patten2(st, end, old=None):
    if old is None:
        old = list()
    for i in combinations_with_replacement(range(st, end+1), 2):
        val = mk_prime(i[0]) * mk_prime(i[1])
        try:
            print(i, old.index(val))
        except ValueError:
            print(i, len(old))
            old.append(val)

"""
commutative property
"""

### solution
