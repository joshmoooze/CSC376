#Joshua John
#3.0

import sys 
import socket 
import receive 
import os
import struct

def receive_file(sock, filename):
	file = open(filename, 'wb')
	while True:
		file_bytes = sock.recv(1024)
		if file_bytes:
			file.write(file_bytes)
		else:
			break
	file.close()

def fileServer(port, filename, mainSock):
	print ("Starting server on " + str(port))
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1) 
	serversocket.bind(('', port)) 
	serversocket.listen(5) 
	mainSock.send(filename.encode()) 
	sock, addr = serversocket.accept() 
	serversocket.shutdown(socket.SHUT_WR)
	serversocket.close() 
	file_size_bytes= sock.recv( 4 )
	if file_size_bytes:
		file_size= struct.unpack( '!L', file_size_bytes[:4] )[0]
		if file_size:
			receive_file(sock, filename[1:])
		else:
			print('File does not exist or is empty')
	else:
		print('File does not exist or is empty')
	sock.close()


def run (sock, port):
	optionsMessage = "Enter an option ('m', 'f', 'x'):\n (M)essage (send)\n (F)ile (request)\ne(X)it" 
	print(optionsMessage) 
	option = sys.stdin.readline().replace("\n", "").upper() 
	if option == "M": 
		print("Enter your message:") 
		message = "m" + sys.stdin.readline().replace("\n", "") 
		sock.send(message.encode()) 
	elif option == "F": 
		print("Which file do you want?") 
		filename = "f" + sys.stdin.readline().replace("\n", "") 
		fileServer(port, filename, sock)
	elif option == "X": 
		os._exit(0)
	else: 
		print (option + " is not valid.") 
	run(sock, port) 
	

def Client (listenPort, serverPort, serverAddress): 
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
	sock.connect((serverAddress, serverPort)) 
	receiveThread = receive.Receive(sock) 
	receiveThread.start() 
	sock.send(str(listenPort).encode())
	while (receive.hasPort == False):
		i = 1
	receive.filePort = listenPort
	run(sock, listenPort) 
