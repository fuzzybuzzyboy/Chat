import socket
import threading

HOST = '127.0.0.1'
PORT = 5050

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

def send_message():
    while True:
        message = input("Enter message: ")
        client_socket.sendall(message.encode('utf-8'))
        print(f'You: {message}')
        print("\033[A                             \033[A")

send_thread = threading.Thread(target=send_message)
send_thread.start()

while True:
    message = client_socket.recv(1024).decode('utf-8')
    print(f'\nThem: {message}')
    print("Enter message: ", end='', flush=True)