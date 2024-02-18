import socket
import threading

HOST = '127.0.0.1'
PORT = 5050

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen()

clients = {}
print(f'Server is online and listening. (Running on port: \'{PORT}\', Running on host: \'{HOST}\')')

def handle_client(client_socket, client_address):
    print(f"New connection from {client_address}")
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message: break
            if message.lower() == '!clear': print(f"Person {list(clients.keys()).index(client_address) + 1} has cleared their chat.")
            else:
                for recipient_address, recipient_socket in clients.items():
                    if recipient_socket != client_socket:
                        recipient_socket.sendall(f'Person {list(clients.keys()).index(client_address) + 1} - {message}'.encode('utf-8'))
                print(f"Person {list(clients.keys()).index(client_address) + 1}: {message}")
    except Exception as e:
        print(f"Error handling client (Crash or forcibly closed) {client_address}: {e}")
    print(f"User disconnected. ({client_address})")
    del clients[client_address]
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    clients[client_address] = client_socket
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
