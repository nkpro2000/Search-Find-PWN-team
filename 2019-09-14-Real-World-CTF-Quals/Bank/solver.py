from hashlib import sha1 as h
from itertools import permutations as p
import base64 as b64
print 'just copy %d>output to terminal\n\n'
a='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
msg='DEPOSIT'
a=[i for i in a]
b=raw_input('given(just copy from terminal)>')
for i in p(a,5):
	c=b+''.join(i)
	print(c)
	ha=h()
	ha.update(c)
	if ord(ha.digest()[-1]) == 0 and ord(ha.digest()[-2]) == 0 :
		i11=c
		print(c)
		break
from schnorr import *
sk=input('sk(any number)>')
print ''
r=schnorr_sign(msg,sk)
print ''
pk=point_mul(G,sk)
i12=b64.b64encode(str(pk[0])+','+str(pk[1]))
i1=i11+i12
if schnorr_verify(msg,pk,r):
	print '\n\nGOT !t\n'
	print 'signature>>>\n'+repr(r)
	i2=b64.b64encode(r)
print "\n\n1>"+i1
print "\n\n2>MQ=="
print "\n\n3>"+i2

print "\n\n4>"+i12
print "\n\n5>Mw=="
pk=input('\n\npk (tuple just displayed on your terminal)>')

msg='WITHDRAW'
print ''
r=schnorr_sign(msg,sk)
print ''
userpk=point_add((pk[0],-pk[1]),point_mul(G,sk))
print ''
i3=b64.b64encode(str(userpk[0])+','+str(userpk[1]))
print "\n\n6>"+i3
print "\n\n7>Mg=="
print ''
if schnorr_verify(msg,point_add(userpk,pk),r):
	print '\n\nGOT !t\n'
	print 'signature>>>\n'+repr(r)
	i4=b64.b64encode(r)
print "\n\n8>"+i4
print "\n\n~ENJOY~.................#nkpro"
