import socket

cl = socket.socket()
host = 'localhost'
port = 8888
cl.connect((host,port))

data = cl.recv(1024)
print(data.decode('utf-8'))
cl.send('hello word'.encode('utf-8'))
data1 = cl.recv(1024)

print(data1.decode('utf-8'))
cl.close()