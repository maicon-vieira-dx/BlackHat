from urllib import request, parser
import argparse
import sys
from concurrent.futures import ThreadPool
import textwrap

class RequestHTTP:
	def __init__():


if __name__ == '__main__':
	parser = argparse.ArgumentParser(
		description='RequestHTTP',
		formatter_class=argparse.RawDescriptionHelpFormatter('''Exemplo:
			python requestUrl.py -t 127.0.0.1 -r get -u <user-agent> -c <cookie>
			python requestUrl.py -t 127.0.0.1 -r post -u <user-agent> -c <cookie> -l admin -p password
			python requestUrl.py -t 127.0.0.1 -r post -h <user-agent> -h <cookie> -L wordlist.txt -P wordlist.txt	
		'''))
		parser.add_argument('-t','--target', required=True, help='Alvo da requisição')
		parser.add_argument('-r', '--request', default='get', help='Tipo da requisição')
		parser.add_argument('-u', '--user_agent', help='Cabeçalho User Agent')
		parser.add_argument('-c','--cookie', help='Cookie do cabeçalho')
		parser.add_argument('-l', '--login', help='Passar o login do usuário')
		parser.add_argument('-L', '--login_wordlist',help='Inserindo o caminho de uma wordlist')
		parser.add_argument('-P', '--password_wordlist', help='Inserindo o caminho de uma wordlist')
		args = parser.parse_args()