#!/usr/bin/env python3

import gensafeprime
import contextlib
import textwrap
import hashlib
import fuckpy3 #pylint:disable=unused-import
import random
import numpy as np
import ast
import os
import re

banner = r"""
                 ___   ___   ___      _____ _             
                / _ \ / _ \ / _ \    |  ___| | __ _  __ _ 
               | | | | | | | | | |   | |_  | |/ _` |/ _` |
               | |_| | |_| | |_| |   |  _| | | (_| | (_| |
                \___/ \___/ \___/    |_|   |_|\__,_|\__, |
                                                    |___/ 
 ____  _                _                 ____                  _          
/ ___|| |__   __ _ _ __(_)_ __   __ _    / ___|  ___ _ ____   _(_) ___ ___ 
\___ \| '_ \ / _` | '__| | '_ \ / _` |   \___ \ / _ \ '__\ \ / / |/ __/ _ \
 ___) | | | | (_| | |  | | | | | (_| |    ___) |  __/ |   \ V /| | (_|  __/
|____/|_| |_|\__,_|_|  |_|_| |_|\__, |   |____/ \___|_|    \_/ |_|\___\___|
                                |___/                                      
"""

#
# Matrix stuff
#

def pascal_matrix(n, k):                                                                           #] Not used anywhere !!!
    matrix = np.ones((n, k)).astype(int)
    for r in range(1, n):
        for c in range(1, k):
            matrix[r,c] = matrix[r,c-1] + matrix[r-1,c]
    assert np.linalg.matrix_rank(matrix) == k
    m = [ list(map(int, row)) for row in matrix ]
    return m

def random_matrix(n, k):
    matrix = [ list(map(int, row)) for row in (np.random.rand(n,k)*1000).astype(int) ]
    assert np.linalg.matrix_rank(matrix) == k
    return matrix

def calc_det(A):
    n,_ = np.shape(A)
    if n== 1:
        return A[0,0]
    else:
        S=0
        for i in range(n):
            L = [x for x in range(n) if x != i]
            S += (-1)**i *A[0,i]*calc_det(A[1:,L])
        return int(S)

#
# OOO Secret Sharing Scheme                                #] it is like solving algebric equation with matrix representation.
#                                                          #] so 5 eq is enough for 5 vars (x[5])

def split_secret(key, n, k, matrix):                                                               #] n,k == `{row,column}"(matrix),"` (100,5)
    assert len(matrix) == n, "misshaped matrix"
    assert len(matrix[0]) == k, "misshaped matrix"
    x = [ int.from_bytes(key, byteorder='little') ]        #0] int.from_bytes(key,byteorder='little') == U.bytes_to_long(bytes(reversed(key))) 
    for _ in range(k-1):
        x.append(random.randint(0, P))
    x = np.array(x)
    shares = [ (n,int(i)) for n,i in enumerate(np.dot(matrix, x)) ]                                ;split_secret.x,split_secret.shares=x,shares ####
    return shares[1:]                                      #] May be we have to find shares[0] which can be alternative to secret_id+".2"

def reconstitute_secret(keys, matrix, xi=0):               #### #] xi is index of x in split_secret, so x[0] (xi=0) is secret                  
        k = len(matrix[0])
        assert k <= len(keys), "not enough keys"                                                   #] Any 5 keys enough (shares[5][5])
        assert np.linalg.matrix_rank(matrix) == k, "linearly dependent keys"
        subkeys = sorted(keys[:k])
        submatrix = [ matrix[e[0]] for e in subkeys ]
        subshares = [ e[-1] for e in subkeys ]
        det = calc_det(np.array(submatrix))
        inv_float = np.linalg.inv(submatrix)
        key = (int(sum([ i*j for i,j in zip([ i*pow(det, -1, P) for i in [ int(round(h)) for h in [ det * inv_float[xi][i] for i in range(k) ] ] ], subshares) ])) % P).to_bytes(32, byteorder='little')                                                           ####
        #SameAsAbove...[ i*j for i,j in zip([ int(round(inv_float[xi][i]*det))*pow(det, -1, P) for i in range(k) ], subshares) ]...
        return key

#
# Menu library
#

def one_menu(items, done_option=True, default=None):
    choices = [ None ]
    for item in items:
        if type(item) in (str, bytes):
            print(item)
        else:
            print("%d <- %s" % (len(choices), item[0]))
            choices.append(item[1])
    if done_option:
        print("0 <- Done.")

    cstr = input("Choice: ")
    if not cstr:
        return default if default is not None else one_menu(items, done_option=done_option)

    choice = int(cstr)
    assert 0 <= choice < len(choices), "Invalid choice!"
    assert choice or done_option, "Invalid choice!"
    return choices[choice]

def menu(*items, do_while=False, loop=False, done_option=False, default=None):
    if do_while: yield True
    c = default
    while True:
        c = one_menu(items, done_option=done_option, default=c)
        if callable(c): yield c()
        elif c is None: break
        else: yield c
        if not loop: break

#
# Menu handlers
#

def share_user_flag():
    secret = input("Enter secret to share: ").bytes()

    secret_id = hashlib.md5(secret).hexdigest()[:6]
    print("Your secret's ID is:", secret_id)

    shares = split_secret(secret, N, K, M)
    random.shuffle(shares)

    total_shares = int(input("Number of shares to make: "))
    assert total_shares >= K, "Too few shares; you won't be able to reconstitute the secret!"
    with open(os.path.join(SHAREDIR, secret_id+".1"), "w") as f:
        f.write(str(shares[0]))
    print("Your shares are:", shares[1:total_shares])
    print("Your stored share is safe with us!")

def redeem_user_flag():
    secret_id = input("Enter the secret's ID: ")
    assert re.match(r"^\w\w\w\w\w\w$", secret_id), "Invalid ID format!"

    user_shares = ast.literal_eval(input("Enter your shares of the secret: "))
    stored_share = ast.literal_eval(open(os.path.join(SHAREDIR, secret_id+".1")).read().strip())
    shares = user_shares + [ stored_share ]
    secret = reconstitute_secret(shares, M).strip(b"\x00")
    print("Your secret is:", secret)

def share_actual_flag():
    the_flag = open(os.path.join(os.path.dirname(__file__), "flag"), "rb").read().strip()
    shares = split_secret(the_flag, N, K, M)
    sanity_flag = reconstitute_secret(shares, M).strip(b"\x00")
    assert sanity_flag == the_flag
    random.shuffle(shares)

    secret_id = os.urandom(3).hex()
    with open(os.path.join(SHAREDIR, secret_id+".1"), "w") as f:
        f.write(str(shares[0]))
    with open(os.path.join(SHAREDIR, secret_id+".2"), "w") as f:
        f.write(str(shares[1]))

    print("Our secret's ID is:", secret_id)
    print("Your shares are:", shares[2:K])
    print("Our stored shares are quite safe with us!")

def redeem_actual_flag():                                  #] So we can get flag by calling redeem_user_flag with secret_id of actual_flag 
    secret_id = input("Enter the secret's ID: ")                                                   #] But we need tuple in secret_id+".2"
    assert re.match(r"^\w\w\w\w\w\w$", secret_id), "Invalid ID format!"

    user_shares = ast.literal_eval(input("Enter your shares of the secret: "))
    stored_share1 = ast.literal_eval(open(os.path.join(SHAREDIR, secret_id+".1")).read().strip())
    stored_share2 = ast.literal_eval(open(os.path.join(SHAREDIR, secret_id+".2")).read().strip())
    shares = [ stored_share1, stored_share2 ] + user_shares
    assert len(set(s[0] for s in shares)) == len(shares), "Duplicate shares."

    secret = reconstitute_secret(shares, M).strip(b"\x00")
    if secret.startswith(b"OOO{"):
        print("Congrats! You have decoded our secret. We must have trusted you!")


def login():
    global USER
    global SHAREDIR

    print("Welcome to the...")
    print(banner)
    print('\n'.join(textwrap.wrap("OOO has finally solved the flag sharing problem by making it quick and easy for aspiring cheaters to share flags by utilizing a secure and exciting secret sharing scheme! OOO reserves the right to withhold flag shares where deemed appropriate.", width=80)))
    print()

    USER = input("Username: ")
    assert USER.lower() != "ooo", "No way!"
    assert USER.lower() != "zardus", "That's me!"
    assert USER.lower() != "malina", "Nope!"
    assert re.match(r"^\w+$", USER), "Invalid username format!"

    SHAREDIR = os.path.join(os.path.dirname(__file__), "shares", USER)
    with contextlib.suppress(FileExistsError):
        os.makedirs(SHAREDIR)

    main_menu()

def main_menu():
    for _ in menu(
        *[ f"What do, {USER}?" ] +
        [
            ("Share useless flag.", share_user_flag),
            ("Redeem useless flag.", redeem_user_flag),
            ("Store scoring flag.", share_actual_flag),
            ("Retrieve scoring flag.", redeem_actual_flag)
        ],
        loop=True, done_option=True
    ):
        pass

if not os.path.exists(os.path.join(os.path.dirname(__file__), "prime.ooo")):                       #] So P value is same for every session
    print("[STARTUP] Generating prime...")
    with open("prime.ooo", 'w') as _f:
        _f.write(str(gensafeprime.generate(256)))

if not os.path.exists(os.path.join(os.path.dirname(__file__), "matrix.ooo")):                      #] So M value is same for every session
    print("[STARTUP] Generating matrix...")
    with open("matrix.ooo", 'w') as _f:
        _f.write(str(random_matrix(100, 5)))

P = ast.literal_eval(open(os.path.join(os.path.dirname(__file__), "prime.ooo")).read().strip())    #] prime no. of bitlength 256 (P=2*Q+1; Q is prime)
M = ast.literal_eval(open(os.path.join(os.path.dirname(__file__), "matrix.ooo")).read().strip())   #] random_matrix[100][5]
N = len(M)                                                                                         #] 100 (no. of rows in M)
K = len(M[0])                                                                                      #] 5 (no. of column in M)

def sanity_check(n=N, k=K, m=M):
    def one_check(secret):
        shares = split_secret(secret, n, k, m)
        random.shuffle(shares)
        new_secret = reconstitute_secret(shares[:k], m)
        assert secret.ljust(32, b"\x00") == new_secret

    for _ in range(1000):
        one_check(os.urandom(random.randint(0, 31)))
    one_check(open(os.path.join(os.path.dirname(__file__), "flag"), "rb").read().strip())

if __name__ == '__main__':
    USER = None
    SHAREDIR = None                                                                                #] ./shares/$USER/
    try:
     login()
    except Exception as e:
     print("ERROR:", e)

'''#0
PY> int.to_bytes(int.from_bytes(b'nkpro','little'),32,'little').rstrip(b'\x00')
b'nkpro'
PY> bytes(reversed(U.long_to_bytes(int.from_bytes(b'nkpro','little'))))
b'nkpro'
PY> int.to_bytes(int.from_bytes(b'nkpro','little'),len(b'nkpro'),'little')
b'nkpro'
PY> #int.from_bytes(key,byteorder='big') == U.bytes_to_long(key)
'''

M_,P_ = M,P
__all__ = ('N', 'K', 'split_secret', 'reconstitute_secret', 'random_matrix', 'calc_det', 'pascal_matrix','M_','P_')

#CTFchallenge:"ooo-flag-sharing@DC28_Quals #crypto"
#[Writeups](https://ctftime.org/task/11589)
