import socket
import threading
from serveraddress import *


name = input("Enter username: ")

# print(
#     '\nWelcome to TCP Chat service.\n\n'
#     'Type simple text messages and broadcast them to\nother online clients on the network.\n\n'
#     '\'@<user_1> @<user_2> .. <text>\'\n - sends a message privately to the listed users.\n'
# )

c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c.connect((IP, PORT))
c.send(bytes(name, 'utf-8'))


def send_message():
    while True:
        c.send(bytes(input(), 'utf-8'))


T = threading.Thread(target=send_message)
T.daemon = True
T.start()

while True:
    data = c.recv(1024).decode('utf-8')
    if not data:
        break
    print(data)
