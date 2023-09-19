import paramikito

def ssh_command(ip,port,password,cmd):
	
	client = paramikito.SSHClient()
	client.set_missing_host_key_policy(paramikito.AutoAddPolicy())
	client.connect(ip, port=port, username=user,password=password)
	
	_,stdout, stderr = client.exec_command(cmd)
	output = stdout.readlines() + stderr.readlines()
	
	if output:
		print('--- Output ---')
		for line in output:
			print(line.strip())
			
			
if __name__ == "__main__":
	
   import getpass
   
	user = input("Usuário: ") or "anonymous"
	ip = input("Alvo: ") or "192.168.0.1"
	password = getpass.getpass()
	port = input("Porta: ") or 2222
	cmd = input("Comando: ") or "id"
	
	ssh_command(ip, port, password, cmd)