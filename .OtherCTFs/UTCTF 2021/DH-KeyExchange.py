# Small P Problems

import Crypto.Util.number as U

p = 69691
g = 1001

A = 17016 # Alice public key
B = 47643 # Bob   public key

if not U.isPrime(q := (p-1)//2):
    print(f"On an unrelated note, {p} is not a safe prime")

def public_key(private_key):
    return pow(g, private_key, p)

def secret_key(public_key_1, private_key_2, p):
    return pow(public_key_1, private_key_2, p)

for i in range(1,100000):
    pk = public_key(i)
    if pk == A:
        print('\n', f'a is {i}')
        print(secret_key(B, i, p))
        break
    elif pk == B:
        print('\n', f'b is {i}')
        print(secret_key(A, i, p))
        break
    else:
        print('.', end='')
