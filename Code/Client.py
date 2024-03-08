from colorama import Fore, Style # styles: BRIGHT, NORMAL, DIM. Fore.WHITE, Style.RESET_ALL (EXAMPLE: Fore.GREEN + Style.BRIGHT + "a")
import socket, threading, os, sys, colorama
colorama.init(autoreset=True)
def username_creation():
    while True:
        username = input(Fore.BLUE + Style.BRIGHT + "Enter your username: " + Fore.WHITE + Style.RESET_ALL)
        if not username: print(Fore.RED + Style.BRIGHT + 'Please actually create a username.' + Fore.WHITE + Style.RESET_ALL)
        if len(username)>16 or len(username)<3 or len(username)==3: print(Fore.RED + Style.BRIGHT + 'Please pick a username under 16 characters and over 3 characters.' + Fore.WHITE + Style.RESET_ALL)
        if username and len(username)<16 and len(username)>3 and len(username)!=3: return username
username = username_creation()

HOST, PORT, client_socket = '127.0.0.1', 5050, socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)), print(Style.BRIGHT + Fore.GREEN + 'Connected with success. Prefix is \'!\'. Client IDS go from oldest -> newest\n' + Fore.BLUE + Style.NORMAL+'!clear - Clears the chat (Client side)\n!exit - Exits the client (works better than ctrl+c for some reason)\n!onlineusers - Tells you how many connected clients are online\n!PM (Private message for short)︱Example: !PM [Client ID] [Your message]\n' + Fore.WHITE, Style.RESET_ALL)
def send_message():
    while True:
        message = input("Enter message: ")
        if message.lower() == '!clear': os.system('cls' if os.name == 'nt' else 'clear'), print(Style.BRIGHT + Fore.GREEN + "Chat cleared!\n" + Fore.BLUE + Style.NORMAL + '!clear - Clears the chat (your messages and the other client.)\n!exit - Exits the client (works better than ctrl+c for some reason)\n!onlineusers - Tells you how many connected clients are online\n!PM (Private message for short)︱Example: !PM [Client ID] [Your message]\n' + Fore.WHITE, Style.RESET_ALL)
        elif message.lower() == '!exit': client_socket.close(), exit('Connection closed.')
        elif message.lower().startswith('!pm'):
            if len(message.split(' ', 3)) == 4: parts = message.split(' ', 2)
            else: parts = message.split(' ', 3)
            if len(parts) == 3 and parts[1].isnumeric(): client_socket.sendall(f'!pm {parts[1]} {' '.join(parts[2:])}'.encode('utf-8'))
            elif not parts[1].isnumeric(): print('Invalid private message format. Please use a client ID instead of random words')
            else: print("Invalid private message format. Use: !pm [Client ID] [Your message]")
        elif len(message)>500: print(Fore.RED + Style.BRIGHT + 'Please write something under 500 characters.' + Style.RESET_ALL + Fore.WHITE)
        elif not message: print(Fore.RED + Style.BRIGHT + 'Please actually write something.' + Style.RESET_ALL + Fore.WHITE)
        elif len(message)<500 and message and not message.lower().startswith('!pm'): client_socket.sendall(f'{message}'.encode('utf-8'))
        sys.stdin.read(0)

send_thread = threading.Thread(target=send_message)
send_thread.start(), client_socket.sendall(username.encode('utf-8'))

while True:
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message: print(f'\n{message}'), print("Enter message: ", end='', flush=True)
    except ConnectionResetError: client_socket.close(), exit("\nConnection to the server was lost.")
