from urllib import request, parse
import argparse
import sys
from concurrent.futures import ThreadPoolExecutor
import textwrap


def fetch_request(target, header, data):
    if data:
        try:
            fetch = request.Request(target, headers=header, data=data)
            response = request.urlopen(fetch)
            return response.read().strip()
        except Exception as e:
            print(e)
    else:
        try:
            fetch = request.Request(target, headers=header)
            response = request.urlopen(fetch)
            return response.read().strip()
        except Exception as e:
            print(e)


class RequestHTTP:
    def __init__(self, args):
        self.args = args
        self.header = {"User-Agent": self.args.user_agent, "Cookie": self.args.cookie}

    def run(self):
        if self.args.request == 'get':
            self.get_method()
        else:
            self.post_method()

    def get_method(self):
        response = fetch_request(self.args.target, self.header, False)
        if response:
            print(response)

    def post_method(self):
        if self.args.login and self.args.password:
            data = parse.urlencode({"user": self.args.login, "password": self.args.password}).encode()
            response = fetch_request(self.args.target, self.header, data)
            if response:
                print(response.decode())
                print('POST')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='BHP Net Tool',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent('''Example:
                python requestUrl.py -t 127.0.0.1 -r get -u <user-agent> -c <cookie>
                python requestUrl.py -t 127.0.0.1 -r post -u <user-agent> -c <cookie> -l admin -p password
                python requestUrl.py -t 127.0.0.1 -r post -h <user-agent> -h <cookie> -L wordlist.txt -P wordlist.txt	
                '''))
    parser.add_argument('-t', '--target', required=True, help='Alvo da requisição')
    parser.add_argument('-r', '--request', default='get', help='Tipo da requisição')
    parser.add_argument('-u', '--user_agent', help='Cabeçalho User Agent')
    parser.add_argument('-c', '--cookie', help='Cookie do cabeçalho')
    parser.add_argument('-p', '--password', help='Senha para o usuário')
    parser.add_argument('-l', '--login', help='Passar o login do usuário')
    parser.add_argument('-L', '--login_wordlist', help='Inserindo o caminho de uma wordlist')
    parser.add_argument('-P', '--password_wordlist', help='Inserindo o caminho de uma wordlist')
    args = parser.parse_args()
    rqhttp = RequestHTTP(args)
    rqhttp.run()
