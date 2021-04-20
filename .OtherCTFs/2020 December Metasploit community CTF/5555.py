from pwn import *

IP = "172.15.18.85"
PORT = 5555

DELIMS = b"\x1b[2J\x1b[H"
LEFT = b"\e[D"
RIGHT = b"\e[C"

r = remote(IP, PORT)
r.recvuntil(DELIMS)

def go(paths, y=0, x=0):
	if y==9: return []
	if not paths[y][x]: return None
	l = go(paths, y+1, x-1)
	c = go(paths, y+1, x)
	r = go(paths, y+1, x+1)
	if c is not None:
		return [''] + c
	elif l is not None:
		return [LEFT] + l
	elif r is not None:
		return [RIGHT] + r


while 5:
	out = r.recvuntil(DELIMS, drop=True, timeout=3).decode()
	print(out)

	lines = out.splitlines()
	if not lines:
		while 5:
			out = r.recv()
			if len(out): print(out)

	paths=[]
	for line in lines[::-1]:
		paths.append([(0 if p in '0|' else 1) for p in line])
	v = lines[-1].index('^')
	route = go(paths, 0, v)
	print(route)

	r.send(route[1])

"""
nkpro@kali:~$ ssh -i Downloads/metasploit_ctf_kali_ssh_key.pem kali@3.91.100.63

kali@kali:~$ python3 5555.py
.
.
.
SCORE: 488
|   0   0     |
| 00          |
| 0   0       |
|     00      |
|        00   |
|  0      0   |
|0  0         |
| 0       0   |
|       0   0 |
| ^0    0     |

['', b'\\e[D', b'\\e[C', '', '', '', b'\\e[D', '', '']

SCORE: 489
|        0    |
|   0   0     |
| 00          |
| 0   0       |
|     00      |
|        00   |
|  0      0   |
|0  0         |
| 0       0   |
| ^     0   0 |
CONGRATULATIONS!  Check port 7878!

kali@kali:~$ curl http://172.15.18.85:7878
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8">
<title>Directory listing for /</title>
</head>
<body>
<h1>Directory listing for /</h1>
<hr>
<ul>
<li><a href="flag.png">flag.png</a></li>
</ul>
<hr>
</body>
</html>

kali@kali:~$ curl http://172.15.18.85:7878/flag.png --output flag.png

nkpro@kali:~$ ssh -i Downloads/metasploit_ctf_kali_ssh_key.pem kali@3.91.100.63 cat flag.png > flag.png
"""
