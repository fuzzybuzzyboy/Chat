from colorama import Fore, Style # styles: BRIGHT, NORMAL, DIM. Fore.WHITE, Style.RESET_ALL (EXAMPLE: Fore.GREEN + Style.BRIGHT + "a")
import socket, threading, os, sys
def username_creation():
    while True:
        username = input("Enter your username: ")
        if not username: print('Please actually create a username')
        if len(username)>16: print('Please pick a name under 16 characters')
        if username and len(username)<16: return username
username = username_creation()

HOST, PORT, client_socket = '127.0.0.1', 5050, socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))
print(Style.BRIGHT + Fore.GREEN + 'Connected with success. Prefix is !\n' + Fore.BLUE + Style.NORMAL+'!clear - Clears the chat (your messages and the other client.)\n!exit - Exits the client (works better than ctrl+c for some reason)\n!onlineusers - Tells you how many connected clients are online\n' + Fore.WHITE, Style.RESET_ALL)

def send_message():
    while True:
        message = input("Enter message: ")
        if message.lower() == '!clear':
            os.system('cls' if os.name == 'nt' else 'clear')
            print(Fore.BLUE + Style.NORMAL + '!clear - Clears the chat (your messages and the other client.)\n!exit - Exits the client (works better than ctrl+c for some reason)\n!onlineusers - Tells you how many connected clients are online\n' + Fore.WHITE, Style.RESET_ALL)
        if message.lower() == '!exit':
            client_socket.close()
            break
        client_socket.sendall(f'{message}'.encode('utf-8'))
        if message=="": print('Please actually write something.')
        sys.stdin.read(0)

send_thread = threading.Thread(target=send_message)
send_thread.start()
client_socket.sendall(username.encode('utf-8'))

while True:
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith('There are currently') and message.endswith('other client(s) online.'): print(f'\n{message}\nEnter message: ', end='', flush=True)
        else:
            print(f'\n{message}')
            print("Enter message: ", end='', flush=True)
    except ConnectionResetError:
        print("\nConnection to the server was lost.")
        break
