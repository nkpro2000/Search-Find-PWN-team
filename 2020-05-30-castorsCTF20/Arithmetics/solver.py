import pwn
import re
from word2number import w2n

server = pwn.remote('chals20.cybercastors.com',14429)
server.read(); server.write('\n')

question_pattern = re.compile(r'^What is (.*) \?$')
words_pattern = re.compile('.*?([a-z ]{2,})')

ops = {'plus' : '+',
       'minus' : '-',
       'multiplied-by' : '*',
       'divided-by' : '//',
       'mod' : '%',
       'power' : '**',
       }

while 5:
    question = server.read().decode()
    print(question)
    
    if question.startswith('Wow!'):
        # you got flag :)
        break
    
    q = question_pattern.match(question)
    if not q:
        continue # not question ?
    q = q.groups()[0]
    
    for op in ops:
        if op in q:
            q = q.replace(op, ops[op])
    
    word = words_pattern.match(q)
    while word:
        word = word.groups()[0]
        q = q.replace(word, str(w2n.word_to_num(word))+' ')
        word = words_pattern.match(q)
    
    answer = eval(q)
    print(answer)
    
    server.writeline(str(answer))

#CTFchallenge:"Arithmetics@castorsCTF20 #coding"
