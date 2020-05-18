import Crypto.Util.number as U

with open('shor') as f:
    All = f.read().splitlines()
    C = [ x.split()[-1] for x in All if x.startswith("Encrypted message") ]
    C = list(map(int,C))
    N = [ x.split()[-1] for x in All if x.startswith("N") ]
    N = list(map(int,N))
    e = [ x.split()[-1] for x in All if x.startswith("e") ]
    e = list(map(int,e))
    G = [ x.split()[-1] for x in All if x.startswith("Base element") ]
    G = list(map(int,G))
    n = [ x.split()[-1] for x in All if x.startswith("Order of the base element mod N") ]
    n = list(map(int,n))

for i in range(len(C)):
    solved = False
    while not solved:
        range_ = (2,6,3) #eval(input("Enter Range >>"))
        for j in range(*range_):
            G_ = pow(G[i],n[i]//j,N[i])
            P = U.GCD(N[i], G_+1)
            if P != 1 and P%N[i] != 0:
                solved = True
                break
            P = U.GCD(N[i], G_-1)
            if P != 1 and P%N[i] != 0:
                solved = True
                break
    Q = N[i] // P
    assert U.isPrime(P) and U.isPrime(Q) and P!=Q, "Not valid P & Q"
    phi = (P-1)*(Q-1) #] phi(n) [Euler totient function](https://en.wikipedia.org/wiki/Euler%27s_totient_function)
    assert U.GCD(e[i],phi) == 1, "Wrong exponent (e)"
    assert 3 <= e[i] < phi, "e not in range [3,ϕ(n))"
    d = U.inverse(e[i],phi)
    M = pow(C[i],d,N[i])
    print (':)',U.long_to_bytes(M))
