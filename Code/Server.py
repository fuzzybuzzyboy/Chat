import socket, threading, os
HOST, PORT = '127.0.0.1', 5050
server_socket, clients, client_usernames, clients_pm, client_pm_check, client_id_counter = socket.socket(socket.AF_INET, socket.SOCK_STREAM), {}, {}, {}, {}, 0
server_socket.bind((HOST, PORT)), server_socket.listen()
Folder_Path = "Chat logs"
File_Path = os.path.join(Folder_Path, "logs.txt")
f = open(f"{File_Path}", "wt")
print(f'Messages are getting logged into a file (chat logs -> logs)\nServer is online and listening. (Running on port: {PORT}, Running on host: {HOST})\nThe ID of the clients is listed by oldest -> newest')
def send_private_message(username, recipient_id, message, sender, sender_id):
    print([id for _, id in client_usernames.values()])
    for client_address, (client_socket, _, client_id) in clients_pm.items():
        if client_id == recipient_id and client_id != client_pm_check.get(sender):
            f.write(f'\n{username} (Client {list(clients.keys()).index(client_address) + 1}), (Private message): sending to client {recipient_id}'), print(f'{username} (Client {sender_id}), (Private message): is sending a message to client {recipient_id}')
            try: client_socket.sendall(f'{username} (Client {sender_id}), (Private message): {message}'.encode('utf-8')), sender.sendall(f'Message sent to client {recipient_id} sucsessfully.'.encode('utf-8'))
            except Exception as e: print(f"Error sending private message to {recipient_id}: {e}")
            else: break
        elif client_id == recipient_id and client_id == client_pm_check.get(sender): client_socket.sendall('You cannot private messages yourself.'.encode('utf-8'))
        elif recipient_id not in [id for _, id in client_usernames.values()]:
            sender.sendall(f'Failed to send private message to client {recipient_id}. (R: Client doesn\'t exist.)'.encode('utf-8'))
            break
        else: print('Something went wrong')
def handle_client(client_socket, client_address):
    global client_id_counter
    client_id_counter += 1
    username = client_socket.recv(1024).decode('utf-8')
    print(f"New connection from {client_address}\nUsername: {username} (Client {list(clients.keys()).index(client_address) + 1})")
    clients[client_address] = client_socket
    clients_pm[client_address] = (client_socket, username, str(client_id_counter))
    client_usernames[client_address] = (username, str(client_id_counter))
    client_pm_check[client_socket] = (str(client_id_counter))
    try:
        client_socket.sendall(f"Hello {username.capitalize()}, there are currently {len(clients)-1} other client(s) online.".encode('utf-8'))
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if message.lower() in ['!onlineusers', '!clear'] and not message.lower().startswith('!pm') or message and not message.lower().startswith('!pm'): f.write(f'\n{username} (Client {list(clients.keys()).index(client_address) + 1}): {message}')
            if not message.lower().startswith('!pm') and message.lower() not in ['!clear', '!onlineusers'] and message:
                for recipient_address, recipient_socket in clients.items():
                    if recipient_socket != client_socket and message.lower()!='!onlineusers' and message.lower()!='!exit' and not message.lower().startswith('!pm'): recipient_socket.sendall(f'{username.capitalize()} (Client {list(clients.keys()).index(client_address) + 1}): {message}'.encode('utf-8'))
                print(f"{username.capitalize()} (Client {list(clients.keys()).index(client_address) + 1}): {message}")
            elif message.lower() == '!onlineusers': print(f"{username} (Client {list(clients.keys()).index(client_address) + 1}) has requested for currently online users."), client_socket.sendall(f"There are currently {len(clients)-1} other client(s) online.".encode('utf-8'))
            elif message.lower() == '!clear': print(f"{username} (Client {list(clients.keys()).index(client_address) + 1}) has cleared their chat.")
            elif message.lower().startswith('!pm'):
                if len(message.split(' ', 3)) == 4: parts = message.split(' ', 2)
                elif len(message.split(' ', 3)) == 3: parts = message.split(' ', 3)
                send_private_message(username, parts[1], ' '.join(parts[2:]), client_socket, list(clients.keys()).index(client_address) + 1)
            elif not message:
                print(f"Something went wrong with handeling {username} (client {list(clients.keys()).index(client_address)}).")
                break
    except Exception as e: print(f"Error handling client (Crash or forcibly closed) {client_address}: {e}")
    print(f"User disconnected. ({client_address})")
    del clients[client_address], client_usernames[client_address], clients_pm[client_address], client_pm_check[client_socket]
    f.close()
    client_socket.close()

while True:
    client_socket, client_address = server_socket.accept()
    clients[client_address] = client_socket
    client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
    client_thread.start()
