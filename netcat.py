import argparse
import socket
import os
import subprocess
import sys
import textwrap
import threading


def execute(cmd):
    current_dir = os.getcwd()
    if not cmd:
        return "Nenhum comando executado"
    elif cmd.lower().startswith("cd "):
        _, path = cmd.split(" ", 1)
        new_dir = os.path.join(current_dir, path)
        os.chdir(new_dir)
        return f" "
    else:
        output = subprocess.check_output(cmd, shell=True, stderr=subprocess.STDOUT, universal_newlines=True, cwd=current_dir)
        return output


class NetCat:
    def __init__(self, args, buffer=None):
        self.args = args
        self.buffer = buffer
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def run(self):
        if self.args.listen:
            self.listen()
        else:
            self.send()

    def send(self):
        print(f'[-] Tentando estabelecer conexão com o alvo...')
        self.socket.connect((self.args.target, self.args.port))
        print(f'[*] Conexão estabelecida: {self.args.target}:{self.args.port}')
        try:
            while True:
                command = input("$ ")
                if command.lower() == "exit":
                    print('\nOperação finalizada!')
                    self.socket.close()
                    sys.exit()
                else:
                    self.socket.send(command.encode())
                    output = self.socket.recv(4096).decode()
                    print(output)
        except KeyboardInterrupt:
            print('\nOperação finalizada!')
            self.socket.close()
            sys.exit()

    def listen(self):
        print(f'[-] Aguardando conexão em {self.args.target}:{self.args.port}...')
        self.socket.bind((self.args.target, self.args.port))
        self.socket.listen(5)
        try:
            while True:
                client_socket, _ = self.socket.accept()
                client_thread = threading.Thread(target=self.handle, args=(client_socket,))
                client_thread.start()
        except KeyboardInterrupt:
            print("n\Terminal finalizado.")
            self.socket.close()
            sys.exit()

    def handle(self, client_socket):
        print(f'[*] Conexão estabelecida!')
        if self.args.execute:
            output = execute(self.args.execute)
            client_socket.send(output.encode())
        elif self.args.upload:
            file_buffer = b''
            while True:
                data = client_socket.recv(4096)
                if data:
                    file_buffer += data
                else:
                    break

            with open(self.args.upload, 'wb') as f:
                f.write(file_buffer)
            message = f'Arquivo salvo {self.args.upload}'
            client_socket.send(message.encode())

        elif self.args.command:
            while True:
                try:
                    while True:
                        cmd_buffer = client_socket.recv(1024).decode()
                        if cmd_buffer.lower() == "exit":
                            client_socket.send("Conexão encerrada.".encode())
                            break
                        else:
                            response = execute(cmd_buffer)
                            if response != '':
                                client_socket.send(response.encode())
                            else:
                                client_socket.send(f" ".encode())
                except:
                    self.socket.close()
                    sys.exit()

if __name__ == '__main__':
    buffer = ''
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
            netcat.py -t 192.16.1.108 -p 5555 -l -c #command shell
            netcat.py -t 192.16.1.108 -p 5555 -l -u=mytest.text #upload file
            netcat.py -t 192.16.1.108 -p 5555 -l -e=\"cat /etc/passwd\" #execute command
            echo 'ABC' | ./netcat.py -t 192.168.1.108 -p 135 #echo text to server port 135
            netcat.py -t 192.168.1.108 -p 5555 #connect to server
            '''))
    parser.add_argument('-c', '--command', action='store_true', help='commnad shell')
    parser.add_argument('-e', '--execute', help='execute specified command')
    parser.add_argument('-l', '--listen', action='store_true', help='listen')
    parser.add_argument('-p', '--port', type=int, default=1234, help='specified port')
    parser.add_argument('-t', '--target', default='127.0.0.1', help='specified IP')
    parser.add_argument('-u', '--upload', help='upload file')
    args = parser.parse_args()

    nc = NetCat(args, buffer.encode())
    nc.run()
