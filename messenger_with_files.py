#Joshua John
#3.0

import sys 
import client, server 


args = sys.argv 
numArgs = len(args) 
serverAddress = 'localhost' 
isServer = True 
i = 0 
while i < numArgs:
	if args[i] == '-l': 
		listenPort = int(args[i + 1]) 
	if args[i] == '-p': 
		serverPort = int(args[i + 1]) 
		isServer = False 
	if args[i] == '-s': 
		serverAddress = int(args[i + 1]) 
		isServer = False 
	i += 1 


if (isServer): 
	server.Server(listenPort) 
else: 
	client.Client(listenPort, serverPort, serverAddress) 
