import ChatClient
import argparse
import time
import select
import sys

def start_chat(name):

	client = ChatClient.ChatClient(name)
	start_time = time.time()
	while(True):
		client.check_sockets()
		client.check_catalog()
		current_time = time.time()
		t = current_time - start_time
		if t > 60:
			client.update_catalog()
			start_time = time.time()


		print('''Select Option: \n 1: show current users 
					\n 2: show current connections 
					\n 3: connect to a user
					\n 4: send message to a user''')

		i, o, e = select.select( [sys.stdin], [], [], 5 )
		if i:
			choice = sys.stdin.readline().strip()
			if choice == '1':
				client.show_current_users()
			elif choice == '2':
				client.show_current_connections()
			elif choice == '3':
				print('Enter the user you would like to connect to:')
				user = raw_input()
				client.request_DM(user)
			elif choice == '4':	
				print('Enter the user you would like to message:')
				user = raw_input()	
				print('Enter your message to {}:'.format(user))
				message = raw_input()
				client.send_DM(user, message)




if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('Name')
	args = parser.parse_args()

	start_chat(args.Name)
