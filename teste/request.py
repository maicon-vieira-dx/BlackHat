import socket

# Configurações do servidor FTP
ftp_server = "ftp.example.com"
ftp_port = 21
username = "user"
password = "password"

# Criação do socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((ftp_server, ftp_port))

# Recebe a mensagem de boas-vindas
response = client_socket.recv(4096).decode()
print(response)

# Envia o nome de usuário
client_socket.sendall(f"USER {username}\r\n".encode())
response = client_socket.recv(4096).decode()
print(response)

# Envia a senha
client_socket.sendall(f"PASS {password}\r\n".encode())
response = client_socket.recv(4096).decode()
print(response)

# Fecha a conexão
client_socket.close()
