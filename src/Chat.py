import ChatClient
import argparse


def start_chat(name)

	client = ChatClient(name)
	




if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('Name')
	args = parser.parse_args()

	start_chat(args.Name)
