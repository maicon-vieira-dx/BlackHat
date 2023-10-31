from urllib import request, parse
import argparse
import requests
import textwrap
from bs4 import BeautifulSoup

def open_wordlist(wordlist):
    with open(wordlist, 'r', encoding='iso-8859-1') as file:
        return file.readlines()

def dirb_buster(target, directories, verbose=False):
    for directory in directories:
        response = requests.get(f'{target}/{directory}')
        if response.status_code == 200:
            print(f'[{response.status_code}]: {target}/{directory}')
        elif verbose:
            print(f'[{response.status_code}]: {target}/{directory}')

def request_http(target, header, data=None):
    if data:
    	try:
    		response = requests.get(target, headers=header)
    		print(f'HTTP [{response.status_code}')
    		return response
    	except Exception as e:
    		print(e)
    else:
    	try:
    		response = requests.post(target, headers=header, json=data)
    		print(f'HTTP [{response.status_code}]')
    		return response
class BurpSuite:
    def __init__(self, args):
        self.args = args
        self.header = {"User-Agent": "Mozilla/5.0 (Linux; Android 10;K) AppleWebKit/537.36 KHTML, li ke Gecko) Chrome/117.0.0.0 Mobile Safari/537.36", "Cookie": self.args.header}

    def run(self):
        if self.args.brute:
            if self.args.dirb:
                print(f'[*] Iniciando busca por diretórios: {self.args.target}')
                wordlist = open_wordlist(self.args.dirb)
                dirb_buster(self.args.target, wordlist, self.args.verbose)
        elif self.args.get:
            print(f'[*] Requisição GET para o alvo: {self.args.target};')
            self.get()
        elif self.args.post:
            print(f'[*] Requisição POST para o alvo: {self.args.target}')
            self.post()
        elif self.args.proxy:
            print('PROXY')
        elif self.args.crawler:
            print(f'[*] Iniciando reconhecimento Crawler no alvo: {self.args.target}')
            self.crawler()

    def get(self):
        response = self.fetch_request()
        if response:
            print(response)
    
    def post(self):
        if self.args.login and self.args.password:
            self.data = {"user": self.args.login, "password": self.args.password}
            response = self.fetch_request()
            if response:
                print(response)
    
    def crawler(self):
        if self.args.crawler == "link":
            response = self.fetch_request()
            soup = BeautifulSoup(response.read().decode(), 'html.parser')
            links = soup.find_all('a', href=True)
            for link in links:
                print('Todos os links: ', link)

    def fetch_request(self):
        if self.args.post:
            response = request_http(self.args.target, self.header, self.data)
            return response.info()
        if self.args.get:
            response = request_http(self.args.target, self.header)
            return response.info()
        if self.args.crawler:
            response = request_http(self.args.target, self.header)
            if response:
                soup = BeautifulSoup(response.read().decode(), 'html.parser')
                links = soup.find_all('a', href=True)
                for link in links:
                    print('Todos os links: ', link)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
                python burpSuite.py -t 127.0.0.1 --get -H <cookie>
                python burpSuite.py -t 127.0.0.1 --post -H <cookie> -l admin -p password
                python requestUrl.py -t 127.0.0.1 -r --post  -H <cookie> -L wordlist.txt -P wordlist.txt
                python burpSuite.py -t 127.0.0.1 --brute -dirb wordlist.txt
                python burpSuite.py -t 127.0.0.1 --crawler link
                '''))
    parser.add_argument('-t', '--target', required=True, help='Alvo da requisição')
    parser.add_argument('-post', '--post', action='store_true', help='Requisição de método post')
    parser.add_argument('-get', '--get', action='store_true', help='Requisição pelo método get')
    parser.add_argument('-b', '--brute', action='store_true', help='Ataque de brute force')
    parser.add_argument('-u', '--user', help='Cabeçalho User Agent')
    parser.add_argument('-H', '--header', help='Cookie do cabeçalho')
    parser.add_argument('-p', '--password', help='Senha para o usuário')
    parser.add_argument('-c', '--crawler', help='Usando crawler no sistema para achar links')
    parser.add_argument('-V', '--verbose', action='store_true', help='Método verbose para visualizar os detalhes')
    parser.add_argument('-proxy', '--proxy', action='store_true', help='Usando proxy na navegação')
    parser.add_argument('-d', '--dirb', help='Caminho para a wordlist')
    parser.add_argument('-l', '--login', help='Passar o login do usuário')
    parser.add_argument('-L', '--login-wordlist', help='Inserindo o caminho de uma wordlist')
    parser.add_argument('-P', '--password-wordlist', help='Inserindo o caminho de uma wordlist')
    args = parser.parse_args()
    bs = BurpSuite(args)
    bs.run()
