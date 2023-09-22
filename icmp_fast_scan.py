import socket

# Especifique a faixa de endereços IP que você deseja enumerar
faixa_ip = "191.6.223."

# Enumere os endereços IP na faixa especificada
for i in range(1, 255):
    ip = faixa_ip + str(i)
    try:
        host = socket.gethostbyaddr(ip)
        print(f"Endereço IP: {ip} - Nome do Host: {host[0]}")
    except socket.herror:
        print(f"Endereço IP: {ip} - Nome do Host: Não disponível")
