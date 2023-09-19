import socket
import os
import subprocess


def main():
    host = "127.0.0.1"
    port = 1234

    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))

        while True:
            command = input("$ ")
            if command.lower() == "exit":
                client_socket.send(command.encode())
                break
            elif command.lower().startswith("download"):
                client_socket.send(command.encode())
                response = client_socket.recv(1024).decode()
                if response.startswith("File not found"):
                    print(response)
                else:
                    filename = command.split()[1]
                    with open(filename, "wb") as file:
                        while True:
                            data = client_socket.recv(1024)
                            if not data:
                                break
                            file.write(data)
                    print(f"{filename} baixado com sucesso.")
            else:
                client_socket.send(command.encode())
                output = client_socket.recv(4096).decode()
                print(output)

        client_socket.close()

    except Exception as e:
        print(f"Erro: {e}")


if __name__ == "__main__":
    main()
