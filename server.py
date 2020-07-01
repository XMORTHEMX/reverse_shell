import socket
import threading

HEADER_SIZE = 64
FORMAT = "utf-8"
DISCONNECT_MESSAGE = "!KILL"

SERVER_NAME = 'LAPTOP-BAVC5R5S'
SERVER = socket.gethostbyname(SERVER_NAME)
PORT = 1235
ADDR = (SERVER, PORT)

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def send(msg, conn):
	msg = msg.encode(FORMAT)
	msg_len = f"{len(msg):<{HEADER_SIZE}}".encode(FORMAT)
	conn.send(msg_len)
	conn.send(msg)


def recieve(conn, local_format = "850", get_out = False):
	msg_len = conn.recv(HEADER_SIZE).decode(FORMAT)
	
	if msg_len:
		msg_len = int(msg_len)
		msg = conn.recv(msg_len).decode(local_format)
		if get_out:
			return msg
		else:
			print(msg)


def handle_client(conn, addr):
	print(f"[CONNECTION STABLISHED AT]{addr}")
	root_len = conn.recv(HEADER_SIZE).decode(FORMAT)
	root_len = int(root_len)
	root = conn.recv(root_len).decode(FORMAT)
	
	print(f"root is {root}")
	connected = True
	
	while connected:
		inp = input(root + "$")
		if inp == DISCONNECT_MESSAGE:
			connected = False 
			break
		if inp[:2] == "cd":
			send(inp, conn)
			root = recieve(conn, local_format = FORMAT, get_out = True)
			continue
		
		send(inp, conn)
		out = recieve(conn)
		

		
def main():
	server.listen()
	while True:
		conn, addr = server.accept()
		thread = threading.Thread(target = handle_client, args = (conn, addr))
		thread.start()
		print(f"[ACTIVE CONNECTIONS]{threading.activeCount() - 1}")

if __name__ == "__main__":
	print(f"SERVER LISTENING ON {ADDR}")
	main()
	print(f"SERVER SUTDOWN")