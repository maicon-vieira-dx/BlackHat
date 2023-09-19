import sys
import socket
import threading

HEX_FILTER = ' '.join(
   [(len(repr(chr(i))) == 3 ) and chr(i) or '.' for i in range(256))]
)

def hexdump(src,length =16,show=true):
	if isinstance(src,bytes):
	     src = src.decode()
	results = list()
	for i in range(0, len(src), length):
	  word = str(src[i:i+length])
	  printable = word.translate(HEX_FILTER)
	  hexa = ' '.join([f'{ord(c}:02X' for c in word])
	  
	  hexwidth = length*3
	  result.append(f'{i:04x} {hexa: <{hexwidth}} {printable}')
	if show:
	  for line in results:
	  	print(line)
	else:
	  return results
	 
def receive_from(connection):
	  buffer = b" "
	  connection.settimeout(10)
	  try:
	  	while True:
	  		data = connection.recv(4096)
	          if not data:
	          	break
	   except Exception as e:
	   	print("Error", e)
	   	pass
	   	
	  return buffer
	  

	  def request handler(buffer):
	  	return buffer
	  def response_handler(buffer):
	  	return buffer
	  
	  
	  def main():
	  	if len(sys.argv[1:]) != 5):
	  		print("Usage ./proxy.py [localhost] [localport]", end=' ')'
	  		print("[remotehost] [remoteport] [receivefirst]")
	  		print("Example ./proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
	  		sys.exit(0)
	  		
	  	local_host = sys.argv[1]
	  	local_port = int(sys.argv[2])
	  
	      remote_host = sys.argv[3]
	      remote_port = int(sys.argv[4])
	  
	      receive_first = sys.argv[5]
	  
	      if "True" in receive_first:
	      	receive_first = true
	      else:
	      	receive_first = false
	      	
	      server_loop(local_host, local_port, remote_host, remote_port, receive_first)
	      	
	  
	  
def __name__ == "__main__":
	  main()
	  
	  
	  
	  
	  
	  
	  
	  
	  