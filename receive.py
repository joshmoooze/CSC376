#Joshua John
#3.0

import os 
import threading 
import socket 
import struct

global hasPort
hasPort = False


class Receive (threading.Thread): 
	def __init__(self, sock): 
		threading.Thread.__init__(self) 
		self.sock = sock 
		
	def send_file(self, sock, fileSize, file):
		print('File size is ' + str(fileSize))
		file_size_bytes = struct.pack('!L', fileSize)
		sock.send(file_size_bytes)
		while True:
			file_bytes = file.read(1024)
			if file_bytes:
				sock.send(file_bytes)
			else:
				break
		file.close()

	def fileClient(self, sock, port, fileSize, file):
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		sock.connect(("localhost", port)) 
		self.send_file(sock, fileSize, file)
		sock.shutdown(socket.SHUT_WR)
		sock.close()

	def no_file(self, sock, port):
		print ("no file")
		zero_bytes = struct.pack('!L', 0)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
		sock.connect(("localhost", port))
		sock.send(zero_bytes)
		sock.shutdown(socket.SHUT_WR)
		sock.close()

	def checkFile(self, sock, filePort, filename): 
		print(filename)
		try:
			file_stat = os.stat(filename)
			if file_stat.st_size:
				file = open(filename, 'rb')
				self.fileClient(sock, filePort, file_stat.st_size, file)
			else:
				self.no_file(sock, filePort)
		except:
				self.no_file(sock, filePort)

	
	def run(self): 
		global filePort
		filePort = int(self.sock.recv(1024).decode()) 
		global hasPort
		hasPort = True
		while True: 
			msg_bytes = self.sock.recv(1024) 
			message = msg_bytes.decode() 
			if len(message) > 0:
				if message[0] == "m":
					print(message[1:])
				elif message[0] == "f":
					print("Requesting File: " + message[1:] + " over port: " + str(filePort))
					self.checkFile(self.sock, filePort, message[1:])
			else:
				os._exit(0) 
