## The keys for the RSA algorithm are generated in the following way
> source: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Key_generation

    1. Choose two distinct prime numbers p and q.
        * For security purposes, the integers p and q should be chosen at random, and should be similar in magnitude but differ in length by a few digits to make factoring harder. Prime integers can be efficiently found using a primality test.
        * p and q are kept secret.
    2. Compute n = pq.
        * n is used as the modulus for both the public and private keys. Its length, usually expressed in bits, is the key length.
        * n is released as part of the public key.
    3. Compute λ(n), where λ is Carmichael's totient function. Since n = pq, λ(n) = lcm(λ(p),λ(q)), and since p and q are prime, λ(p) = φ(p) = p − 1 and likewise λ(q) = q − 1. Hence λ(n) = lcm(p − 1, q − 1).
        * λ(n) is kept secret.
        * The lcm may be calculated through the Euclidean algorithm, since lcm(a,b) = |ab|/gcd(a,b).
    4. Choose an integer e such that 1 < e < λ(n) and gcd(e, λ(n)) = 1; that is, e and λ(n) are coprime.
        * e having a short bit-length and small Hamming weight results in more efficient encryption  – the most commonly chosen value for e is 2^16 + 1 = 65,537. The smallest (and fastest) possible value for e is 3, but such a small value for e has been shown to be less secure in some settings.
        * e is released as part of the public key.
    5. Determine d as d ≡ e^(-1) (mod λ(n)); that is, d is the modular multiplicative inverse of e modulo λ(n).
        * This means: solve for d the equation d⋅e ≡ 1 (mod λ(n)); d can be computed efficiently by using the Extended Euclidean algorithm, since, thanks to d and λ(n) being coprime, said equation is a form of Bézout's identity, where d is one of the coefficients.
        * d is kept secret as the private key exponent.

The public key consists of the modulus n and the public (or encryption) exponent e. The private key consists of the private (or decryption) exponent d, which must be kept secret. p, q, and λ(n) must also be kept secret because they can be used to calculate d. In fact, they can all be discarded after d has been computed.

In the original RSA paper, the Euler totient function φ(n) = (p − 1)(q − 1) is used instead of λ(n) for calculating the private exponent d. Since φ(n) is always divisible by λ(n) the algorithm works as well. That the Euler totient function can be used can also be seen as a consequence of the Lagrange's theorem applied to the multiplicative group of integers modulo pq. Thus any d satisfying d⋅e ≡ 1 (mod φ(n)) also satisfies d⋅e ≡ 1 (mod λ(n)). However, computing d modulo φ(n) will sometimes yield a result that is larger than necessary (i.e. d > λ(n)). Most of the implementations of RSA will accept exponents generated using either method (if they use the private exponent d at all, rather than using the optimized decryption method based on the Chinese remainder theorem described below), but some standards like FIPS 186-4 may require that d < λ(n). Any "oversized" private exponents not meeting that criterion may always be reduced modulo λ(n) to obtain a smaller equivalent exponent.

Since any common factors of (p − 1) and (q − 1) are present in the factorisation of n − 1 = pq − 1 = (p − 1)(q − 1) + (p − 1) + (q − 1), it is recommended that (p − 1) and (q − 1) have only very small common factors, if any besides the necessary 2.

Note: The authors of the original RSA paper carry out the key generation by choosing d and then computing e as the modular multiplicative inverse of d modulo φ(n), whereas most current implementations of RSA, such as those following PKCS#1, do the reverse (choose e and compute d). Since the chosen key can be small whereas the computed key normally is not, the RSA paper's algorithm optimizes decryption compared to encryption, while the modern algorithm optimizes encryption instead.

### some code for 3. and 4.

```python3
>>> import Crypto.Util.number as u 
>>> p, q = 5, 7
>>> n, phin, carn = p*q, (p-1)*(q-1), 12 #Carmichael_function
>>> # Carmichael_function(n) = m, where a^m mod n is 1 for every a(between 1 and n where that is coprime to n)
>>> list(map(lambda a: pow(a,carn,n), (i for i in range(1,n) if u.GCD(i,n)==1)))
[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
>>> # https://en.wikipedia.org/wiki/Carmichael_function
>>> phin_ = 0
>>> for i in range(n+1):                                     
...  if u.GCD(i,n) == 1:
...   phin_ += 1
... 
>>> phin_ == phin
True
>>> # https://en.wikipedia.org/wiki/Euler%27s_totient_function
>>> for i in range(n+1):                                 
...  print(i, pow(i, phin, n), pow(i, carn, n), u.GCD(i, n))
... 
0 0 0 35
1 1 1 1
2 1 1 1
3 1 1 1
4 1 1 1
5 15 15 5
6 1 1 1
7 21 21 7
8 1 1 1
9 1 1 1
10 15 15 5
11 1 1 1
12 1 1 1
13 1 1 1
14 21 21 7
15 15 15 5
16 1 1 1
17 1 1 1
18 1 1 1
19 1 1 1
20 15 15 5
21 21 21 7
22 1 1 1
23 1 1 1
24 1 1 1
25 15 15 5
26 1 1 1
27 1 1 1
28 21 21 7
29 1 1 1
30 15 15 5
31 1 1 1
32 1 1 1
33 1 1 1
34 1 1 1
35 0 0 35
>>> for i in range(n+1):
...  print('%2d. %2d %2d %2d | %2d %2d' % (i, pow(i,phin,n),pow(i,carn,n),u.GCD(i,n), u.GCD(i,phin),u.GCD(i,carn)))
... 
 0.  0  0 35 | 24 12
 1.  1  1  1 |  1  1
 2.  1  1  1 |  2  2
 3.  1  1  1 |  3  3
 4.  1  1  1 |  4  4
 5. 15 15  5 |  1  1
 6.  1  1  1 |  6  6
 7. 21 21  7 |  1  1
 8.  1  1  1 |  8  4
 9.  1  1  1 |  3  3
10. 15 15  5 |  2  2
11.  1  1  1 |  1  1
12.  1  1  1 | 12 12
13.  1  1  1 |  1  1
14. 21 21  7 |  2  2
15. 15 15  5 |  3  3
16.  1  1  1 |  8  4
17.  1  1  1 |  1  1
18.  1  1  1 |  6  6
19.  1  1  1 |  1  1
20. 15 15  5 |  4  4
21. 21 21  7 |  3  3
22.  1  1  1 |  2  2
23.  1  1  1 |  1  1
24.  1  1  1 | 24 12
25. 15 15  5 |  1  1
26.  1  1  1 |  2  2
27.  1  1  1 |  3  3
28. 21 21  7 |  4  4
29.  1  1  1 |  1  1
30. 15 15  5 |  6  6
31.  1  1  1 |  1  1
32.  1  1  1 |  8  4
33.  1  1  1 |  3  3
34.  1  1  1 |  2  2
35.  0  0 35 |  1  1
```

## Proofs of correctness
[see](https://en.wikipedia.org/wiki/RSA_\(cryptosystem\)#Proofs_of_correctness "wikipedia")

### Proof using Euler's theorem
> source: https://en.wikipedia.org/wiki/RSA_(cryptosystem)#Proof_using_Euler's_theorem

Although the original paper of Rivest, Shamir, and Adleman used Fermat's little theorem to explain why RSA works, it is common to find proofs that rely instead on Euler's theorem.

We want to show that m^(ed) ≡ m (mod n), where n = pq is a product of two different prime numbers and e and d are positive integers satisfying ed ≡ 1 (mod φ(n)). Since e and d are positive, we can write ed = 1 + hφ(n) for some non-negative integer h. Assuming that m is relatively prime to n, we have

`m^(ed) = m^(1+hφ(n)) = m (m^(φ(n)))^(h) ≡ m (1)^(h) ≡ m  (mod n)`

where the second-last congruence follows from Euler's theorem.

More generally, for any e and d satisfying ed ≡ 1 (mod λ(n)), the same conclusion follows from Carmichael's generalization of Euler's theorem, which states that m^(λ(n)) ≡ 1 (mod n) for all m relatively prime to n.

When m is not relatively prime to n, the argument just given is invalid. This is highly improbable (only a proportion of 1/p + 1/q − 1/(pq) numbers have this property), but even in this case the desired congruence is still true. Either m ≡ 0 (mod p) or m ≡ 0 (mod q), and these cases can be treated using the previous proof.
