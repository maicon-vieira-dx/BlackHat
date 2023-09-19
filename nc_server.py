import socket
import subprocess
import sys
import os

def main():
    host = "127.0.0.1"
    port = 1234
    current_dir = os.getcwd()

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f"Aguardando conexão em {host}:{port}...")

        client_socket, client_address = server_socket.accept()
        print(f"Conexão estabelecida com {client_address[0]}:{client_address[1]}")

        try:
            while True:
                command = client_socket.recv(1024).decode()
                if command.lower() == "exit":
                    client_socket.send("Conexão encerrada.".encode())
                    break
                elif command.lower().startswith("cd "):
                    _, path = command.split(" ", 1)
                    new_dir = os.path.join(current_dir, path)
                    try:
                        os.chdir(new_dir)
                        current_dir = os.getcwd()
                        client_socket.send(f"Diretório alterado para {current_dir}".encode())
                    except Exception as e:
                        client_socket.send(str(e).encode())
                elif command.lower() == "ls":
                    try:
                        dir_contents = "\n".join(os.listdir(current_dir))
                        client_socket.send(dir_contents.encode())
                    except Exception as e:
                        client_socket.send(str(e).encode())
                else:
                    try:
                        output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT,
                                                         universal_newlines=True, cwd=current_dir)
                        client_socket.send(output.encode())
                    except subprocess.CalledProcessError as e:
                        client_socket.send(str(e).encode())
        finally:
            client_socket.close()
            server_socket.close()
    except KeyboardInterrupt:
        print("\nOperação finalizada...")
        server_socket.close()
        sys.exit()

if __name__ == "__main__":
    main()
