import socket
import threading
import re
from serveraddress import *

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((IP, PORT))

s.listen(10)

print('TCP Chat server is online at '+IP+':'+str(PORT), '\nServer log:')
group = []
socks = {}


def broadcast(message, to):
    for who in to:
        try:
            who.send(bytes(message, 'utf-8'))
        except:
            pass


def handle_client(c, a):
    name = c.recv(1024).decode('utf-8')
    if name in socks.keys():
        broadcast('That username is taken', [c])
        c.close()
        return
    group.append(c)
    socks[name] = c
    broadcast(name + ' has connected', group)
    print(name + ' has connected')
    while True:
        data = c.recv(1024).decode('utf-8')
        if not data:
            broadcast(name + ' has disconnected', group)
            print(name + ' has disconnected')
            group.remove(c)
            socks.pop(name)
            c.close()
            return
        x = re.search('^@[a-z0-9A-Z]+ ', data)
        to_name = []
        while x is not None:
            to_name.append(x.group()[1:-1])
            data = data[len(x.group()):]
            x = re.search('^@[a-z0-9A-Z]+ ', data)

        to = [socks[x] for x in to_name if x in socks.keys()]

        for x in to_name:
            if x not in socks.keys():
                broadcast('user '+x+' is not available', [c])

        if len(to_name) == 0:
            to = group
            data = '<'+name+'>: '+data
        else:
            data = '<'+name+'>: '+'(personally) '+data
        broadcast(data, to)


while True:
    c, address = s.accept()
    T = threading.Thread(target=handle_client, args=(c, address))
    T.daemon = True
    T.start()
