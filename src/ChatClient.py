import socket
import json
import select
import subprocess
import time

class ChatClient(object):
	
	def __init__(self, name):
		self.name = name
		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((socket.gethostname(), 0))
		serversocket.listen(5)
		self.socket_list = {"Master": self.socket}
		self.user_list = {}
		self.update_catalog()
		self.check_catalog()
		

	def update_catalog(self)
		data = {"type" : "nsbs-chat", "owner" : name, "port" : self.socket.getsockname()[1]}
		catalog_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = json.dumps(data)
		data = data.encode('utf_8')
		catalog_socket.sendto(data, ('catalog.cse.nd.edu', 9097))

	def check_catalog(self):
		subprocess.check_call(['curl', 'http://catalog.cse.nd.edu:9097/query.json', '--output', 'catalog'])    
		f = open('catalog')                                                                                   
		data = json.load(f)
		users  = [x  for x in data if 'type' in x and x['type'] == 'nsbs-chat']
		for user in users:
			name = user['owner']
			port = user['port']
			server = user['name']
			self.user_list[name] = {'server':server, 'port':port}         

	def send_msg(self, user):
		
		
	
	def handle_msg(self, msg):
		method = msg['msg']
		name = msg['name']
		if method == 'DM':
			message = msg['msg']
			print('DM From {}: {}'.format(name, message))
			
			
	def check_sockets(self):
		readable, writable, exceptional = select.select(socket_list.values(), [], socket_list.values()
		for read_socket in readable:                                                                  
			if read_socket == socket_list['Master']:
				(clientsocket, address) = serversocket.accept()
				sockets[str(address)] = clientsocket
			else:
				clientsocket = read_socket
				address = ''
				for x in sockets:
					if sockets[x] == clientsocket:
						address = x
				header = b''
				closed = False

				while ':' not in header.decode('utf_8'):
					msg = clientsocket.recv(1)
					if not msg:
						print('client closed removing socket detail for address', address)
						del sockets[address]
						closed = True
						break
                                        header += msg

				if not closed:
					size = int(header.decode('utf_8').split(':')[0])
					msg = ''
					while size > 0:
						rsp = clientsocket.recv(size)
						x = len(rsp)
						size -= x
						msg += rsp.decode('utf_8')
					msg = json.loads(msg)
					handle_msg(msg)
			#		return_msg = handle_msg(msg)
			#		return_msg = json.dumps(return_msg)
			#		return_msg = return_msg.encode('utf_8')
			#		header = '{}:'.format(len(return_msg))
			#		return_msg = header.encode('utf_8') + return_msg
			#		clientsocket.sendall(return_msg)

