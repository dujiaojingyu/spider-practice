import socket
import time
sock = socket.socket()
host = 'localhost'
port = 8888
sock.bind((host,port))

sock.listen(5)

while True:
    con,addr = sock.accept()
    con.send('你好'.encode('utf-8'))  #encode()表示将字符串转化成bytes类型
    data = con.recv(1024)
    print(type(data.decode()))
    time.sleep(2)
    con.send(data.decode().upper().encode('utf-8'))

sock.close()

        
        