import socket, time

s=socket.socket()

s.connect(("chal.tuctf.com",30102))

a = "abcdefghijklmnopqrstuvwxyz"#[::-1]

ea = []

t = a

count = 0

while True :

    time.sleep(0.5)
    s.send((t+"\n").encode())

    time.sleep(0.5)
    d = s.recvfrom(1024)

    print("#"*9)
    print(d[0].decode())

    d = str(d[0])

    if d.find("Congratulations!") != -1 or d.find("Welcome") != -1:

        if d.find("Welcome") == -1:

            time.sleep(0.5)

            s.send((a+"\n").encode())

            time.sleep(0.5)
            d = s.recvfrom(1024)

            print(d[0].decode())

            d = str(d[0])

        dd = d.split("encrypted is ")

        dd = dd[-1].split("\\n")[0]

        ea = dd.split()

        print("@"*9+'\n')
        print(list(a),'\n',ea)
        print('\n'+"@"*9+'\n')

        if count == 5 : break
        else : count += 1

    if d.find("Decrypt") != -1 :

        d = d.split("Decrypt ")

        d = d[-1].split("\\n")[0]

        d = d.split()

        dd = []

        for x in d :

            dd.append(a[ea.index(x)])

        t = ''.join(dd)

        print("?!"*5,t,'\n')

eea = list(ea) ####

rea = [] ####

for i in ea:
    if i in rea : rea.append(i)

ea = ''.join(list(rea))

print("$"*18, "level 5 reached ")

if d.find("Decrypt") != -1 :

    d = d.split("Decrypt ")

    d = d[-1].split("\\n")[0]

    d = d.split()

    dd = []

    for x in d :

        dd.append(a[ea.find(x)%26])

    t = ''.join(dd)

    print("?!"*5,t,'\n')

while 5:

    time.sleep(0.5)
    s.send((t+"\n").encode())

    time.sleep(0.5)
    d = s.recvfrom(1024)

    print("$"*9)
    print(d[0].decode())

    d = str(d[0])

    if d.find("Decrypt") != -1 :

        d = d.split("Decrypt ")

        d = d[-1].split("\\n")[0]

        d = d.split()

        dd = []

        dd2 = [] ####

        dd3 = [] ####

        for x in d :

            dd.append(a[ea.find(x)%26])
            if x in eea : dd2.append(a[eea.index(x)]) ####
            if x in rea : dd3.append(a[rea.index(x)]) ####

        t = ''.join(dd)

        print("?!"*5,t,'\n',"####",dd2,dd3)



"""xx = ""

                for i in x :
                    if i == '>' : xx+='<'
                    elif i == '<' : xx+='>'
                    elif i == 'v' : xx+='^'
                    elif i == '^' : xx+='v'
                    elif i == ']' : xx+='['
                    elif i == '[' : xx+=']'
                    elif i == '_' : xx+='-'
                    elif i == '-' : xx+='_'
                    else : xx+=i

                ""xx = ":("

                if x == '<' : xx='>'
                elif x == '>' : xx='<'
                elif x == ']' : xx='['
                elif x == '[' : xx=']'
                elif x == 'v' : xx='^'
                elif x == '^' : xx='v'

                else :

                    if x[0] == '|' and x[-1] == '|' :
                        if x[1:] in ea : xx = x[1:]
                        elif x[:-1] in ea : xx = x[:-1]

                    elif x[0] == '|' : 
                        if x+'|' in ea : xx = x+'|'
                        elif x[1:] in ea : xx = x[1:]

                    elif x[-1] == '|' : 
                        if '|'+x in ea : xx = '|'+x
                        elif x[:-1] in ea : xx = x[:-1]


                xx = x


                if xx in ea : 
                    dd.append(a[::-1][ea[::-1].index(xx)])
                    print("\n!!! found "+xx+" !!!!!!!!!!!!!!!!!"+x+"\n")
                else :
                    dd.append('')
                    print("\n??? not found "+xx+" ??????????????????"+x+"\n")"""
















                
