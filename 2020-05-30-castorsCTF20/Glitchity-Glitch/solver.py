import pwn

server = pwn.remote('chals20.cybercastors.com',14432)
read = server.readuntil('Choice:')
print(read.decode())
# buy VPN (glitchy item)
server.writeline('6')

money_pattern = re.compile(r'[\s\S]*?Your money: (\d*)')

while 5:
    read = server.readuntil('Choice:')
    print(read.decode())
    
    money = money_pattern.match(read.decode()).groups()[0]
    if int(money) >= 6000:
        # Now buy Flag
        server.writeline('5')
        read = server.readuntil('}')
        print(read.decode())
        break # GOT Flag
    
    # sell ITEM
    server.writeline('0')
    read = server.readuntil('Choice')
    print(read.decode())
    # VPN (glitchy item)
    server.writeline('1')

#CTFchallenge:"Glitchity_Glitch@castorsCTF20 #coding"
