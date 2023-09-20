import socket
import argparse
import sys
import textwrap
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Event
def connect_server(host, port, verbose):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.settimeout(1)
    code = client.connect_ex((host, port))
    if code == 0:
        return f"[ABERTA]: {port}"
    elif verbose:
        return f"[FECHADA]: {port}"

class PortScanner:

    def __init__(self, args):
        self.args = args
        self.target = self.args.target
        self.ports = []
        self.verbose = self.args.verbose
        self.threads = self.args.threads
        if self.args.range:
            start, end = self.args.range.split('-')
            self.max = int(end)
            self.min = int(start)
            while self.min <= self.max:
                self.ports.append(self.min)
                self.min += 1
        elif self.args.port:
            self.ports.append(self.args.port)
            self.verbose = True
        count = 1
        while count < 65535:
            self.ports.append(count)
            count += 1

    def scan(self):
        with ThreadPoolExecutor(max_workers=int(self.threads)) as executor:
            futures = [executor.submit(connect_server, self.target, int(port), self.verbose) for port in self.ports]

            try:
                for future in as_completed(futures):
                    result = future.result()
                    if result:
                        print(result)
                    future.cancel()
            except KeyboardInterrupt:
                print('Sessão finalizada')
                sys.exit()


if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description='PORT SCAN',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Exemplo:
            python portscan.py -t 192.168.0.1 -v
            python portscan.py -t 192.168.0.1 -p 80
            python portscan.py -t 192.168.0.1 -l 21,22,80,443,445
            python portscan.py -t 192.168.0.1 -r 10-5000
            '''))
    parser.add_argument('-t', '--target', required=True, help='Alvo')
    parser.add_argument('-p', '--port', help="Portas do alvo")
    parser.add_argument('-l', '--list', help='Lista de portas para inspecionar')
    parser.add_argument('-r', '--range', help='Inserir máximo e mínimo de portas para escanear')
    parser.add_argument('-v', '--verbose', action='store_true', help='Visualizar todas as informações')
    parser.add_argument('-T', '--threads', default=30, help='Quantidade de threads para serem executadas simultaneamente')
    args = parser.parse_args()
    portSc = PortScanner(args)
    portSc.scan()
