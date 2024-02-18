import socket, threading, os, sys

HOST = '127.0.0.1'
PORT = 5050

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

print('Connected with success. Prefix is !\n!clear - Clears the chat (your messages and the other client.)\n')

def send_message():
    while True:
        message = input("Enter message: ")
        if message.lower() == '!clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            print("Chat cleared.")
        client_socket.sendall(message.encode('utf-8'))
        if message=="": print('Please actually write something.')
        sys.stdin.read(0)

send_thread = threading.Thread(target=send_message)
send_thread.start()

while True:
    try:
        message = client_socket.recv(1024).decode('utf-8')
        print(f'\n{message}')
        print("Enter message: ", end='', flush=True)
    except ConnectionResetError:
        print("\nConnection to the server was lost.")
        break
