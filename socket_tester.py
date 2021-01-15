import socket


HOST = '127.0.0.1'
PORT = 3000

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    print("Connecting...")
    s.connect((HOST, PORT))
    s.sendall(b'{"c":5}')
    data = s.recv(1024)

print(repr(data))
