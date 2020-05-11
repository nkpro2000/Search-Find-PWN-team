import socket

s = socket.socket()

s.connect(("chal.tuctf.com",30100)) 

a = list("abcdefghijklmnopqrstuvwxyz")

for i in range(0,26):

	r = s.recv(1024).decode()

	print(r)

	r = r.split(": ")[-1].split('\n')[0]

	print(r)

	d = [a[(a.index(x.lower())+i)%26] for x in r]

	d = ''.join(d)

	print(d)

	s.send(d.encode())

	s.send(b'\n')
