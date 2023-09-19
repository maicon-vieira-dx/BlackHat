import socket
import argparse
import textwrap


def connectServer(host,port, verbose):
	
	try:
		client = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		client.settimeout(0.1)
		code = client.connect_ex((host,port))
		if verbose and code == 0:
			print(f"[FECHADA]: {port}")
		else:
			print(f"[ABERTA]: {port}")
		
class PortScanner:

	def __ini__(self, args):
		self.args = args
		self.target = self.args.target
		self.ports = []
		if self.args.list:
			for ports in self.args.list:
				self.ports +=a
		

if __name__ == '__main__':
	
	parser = argparse.ArgumentParser(
		description='PORT SCAN',
		formatter_class=argparse.RawDescriptionHelpFormatter,
		epilog=textwrap.dedent(''' Exemplo:
			python portscan.py -t 192.168.0.1 -v
			python portscan.py -t 192.168.0.1 -p 80
			python portscan.py -t 192.168.0.1 -l 21,22,80,443,445
			python portscan.py -t 192.168.0.1 -max=5000
			python portscan.py -t 192.168.0.1 -min=5000
			python portscan.py -t 192.168.0.1 -all
		'''))
		parser.add_argument('-t', '--target', required=True, help='Alvo')
		parser.add_argument('-p', '--port', default=80, help="Portas do alvo")
		parser.add_argument('-l', '--list', help='Lista de portas para inspecionar')
		parser.add_argument('-max', '--maximum', help='Máximo de verificações no alvo')
		parser.add_argument('-min', '--minimum', help='')
		
		portSc = PortScanner(parser)