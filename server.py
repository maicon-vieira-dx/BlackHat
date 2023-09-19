import socket


host = '127.0.0.1'
port = 8000

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))
client.send(b'GET / HTTP/1.1 \r\nHost: hacker.com\r\n\r\n')
response = client.recv(4096)

print(response.decode())
client.close()