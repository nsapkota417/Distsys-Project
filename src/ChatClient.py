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
		self.socket.listen(5)
		self.socket_list = {self.socket}
		self.user_list = {}
		self.accepted_connections = {}
		self.update_catalog()
		
	def show_current_users(self):
		for user in self.user_list:
			print(user)

	def show_current_connections(self):
		for user in self.accepted_connections:
			print(user)

	def update_catalog(self):
		data = {"type" : "nsbs-user", "owner" : self.name, "port" : self.socket.getsockname()[1]}
		catalog_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		data = json.dumps(data)
		data = data.encode('utf_8')
		catalog_socket.sendto(data, ('catalog.cse.nd.edu', 9097))

	def check_catalog(self):
		print('Looking for users....')
		subprocess.check_call(['curl', 'http://catalog.cse.nd.edu:9097/query.json', '--output', 'catalog'])    
		f = open('catalog')                                                                                   
		data = json.load(f)
		users  = [x for x in data if 'type' in x and (x['type'] == 'nsbs-user' or x['type'] == 'nsbs-group')]
		for user in users:
			name = user['owner']
			port = user['port']
			server = user['name']
			node_type = user['type']
			self.user_list[name] = {'server':server, 'port':port, 'type':node_type}         

	def send_DM(self, user, message):
		if user in self.accepted_connections:
			msg = {'method':'DM', 'name':self.name, 'message':str(message)}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			self.accepted_connections[user].sendall(msg)
		else:
			print('Unable to send message. User {} is either unknown or has not accepted request.'. format(user))

	def request_DM(self, user):	
		if user in self.user_list:
			msg = {'method':'Request', 'name':self.name}
			msg = json.dumps(msg)
			msg = msg.encode('utf_8')
			header = '{}:'.format(len(msg))
			msg = header.encode('utf_8') + msg
			server = self.user_list[user]['server']
			port = self.user_list[user]['port']
			req_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			try:
				print('connecting to {} on server {} on port {}'.format(user, server, port))
				req_socket.connect((server, port))
				req_socket.sendall(msg)
				self.socket_list.add(req_socket)
				print('Sent request to {}'.format(user))
			except socket.error:
				print('Unable to Connect to user {}'.format(user))	
		else:
			print('User {} is unknown.'.format(user))
			
	
	def handle_msg(self, msg, socket):
		method = msg['method']
		name = msg['name']
		if method == 'Request':
			print('DM Request From {}...'.format(name))
			print('accept DM request from {}? [y/n]...'.format(name))
			choice = raw_input()
			if choice == 'n':
				return_msg = {'method':'Response', 'name':self.name, 'Response':'n'}
				return_msg = json.dumps(return_msg)
				return_msg = return_msg.encode('utf_8')
				header = '{}:'.format(len(return_msg))
				return_msg = header.encode('utf_8') + return_msg
				socket.sendall(return_msg)
				self.socket_list.remove(socket)
			elif choice == 'y':
				self.accepted_connections[name] = socket
				return_msg = {'method':'Response', 'name':self.name, 'Response':'y'}
				return_msg = json.dumps(return_msg)
				return_msg = return_msg.encode('utf_8')
				header = '{}:'.format(len(return_msg))
				return_msg = header.encode('utf_8') + return_msg
				socket.sendall(return_msg)

		elif method == 'Response':
			response = msg['Response']
			if response == 'y':
				print('Messging Request from {} has been ACCEPTED.'.format(name))
				self.accepted_connections[name] = socket
			elif response == 'n':
				print('Messaging Request from {} has been DECLINED.'.format(name))
				self.socket_list.remove(socket)
 
		elif method == 'DM':
			x = [x for x in self.accepted_connections if self.accepted_connections[x] == socket]
			if not x:
				print('Message from {} has been declined as they have not been accepted'.format(user))

			else:	
				message = msg['message']
				print('DM From {}: {}'.format(name, message))
		
							
	def check_sockets(self):
		print('checking open sockets...')
		readable, writable, exceptional = select.select(list(self.socket_list), [], list(self.socket_list), 2)
		for read_socket in readable:                                                                  
			if read_socket == self.socket:
				print('accepting incomming connection...')
				(clientsocket, address) = read_socket.accept()
				self.socket_list.add(clientsocket)
			else:
				clientsocket = read_socket

				header = b''
				closed = False
				while ':' not in header.decode('utf_8'):
					msg = clientsocket.recv(1)
					if not msg:
						print('A Socket has been closed...')
						self.socket_list.remove(clientsocket)
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
					self.handle_msg(msg, clientsocket)

