from colorama import Fore, Style # styles: BRIGHT, NORMAL, DIM. Fore.WHITE, Style.RESET_ALL (EXAMPLE: Fore.GREEN + Style.BRIGHT + "a")
import socket, threading, os, sys, colorama
colorama.init(autoreset=True)
def username_creation():
    while True:
        username = input(Fore.BLUE + Style.BRIGHT + "Enter your username: " + Fore.WHITE + Style.RESET_ALL)
        if not username: print(Fore.RED + Style.BRIGHT + 'Please actually create a username.' + Fore.WHITE + Style.RESET_ALL)
        if len(username)>16 or len(username)<3: print(Fore.RED + Style.BRIGHT + 'Please pick a username under 16 characters and over 3 characters.' + Fore.WHITE + Style.RESET_ALL)
        if username and len(username)<16 and len(username)>3: return username
username = username_creation()

HOST, PORT, client_socket = '127.0.0.1', 5050, socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT)), print(Style.BRIGHT + Fore.GREEN + 'Connected with success. Prefix is !\n' + Fore.BLUE + Style.NORMAL+'!clear - Clears the chat (Client side)\n!exit - Exits the client (works better than ctrl+c for some reason)\n!onlineusers - Tells you how many connected clients are online\n' + Fore.WHITE, Style.RESET_ALL)
def send_message():
    while True:
        message = input("Enter message: ")
        if message.lower() == '!clear': os.system('cls' if os.name == 'nt' else 'clear'), print(Style.BRIGHT + Fore.GREEN + "Chat cleared!\n" + Fore.BLUE + Style.NORMAL + '!clear - Clears the chat (your messages and the other client.)\n!exit - Exits the client (works better than ctrl+c for some reason)\n!onlineusers - Tells you how many connected clients are online\n' + Fore.WHITE, Style.RESET_ALL)
        if message.lower() == '!exit': client_socket.close(), exit('Connection closed.')
        if not message: print('Please actually write something.')
        else: client_socket.sendall(f'{message}'.encode('utf-8'))
        sys.stdin.read(0)

send_thread = threading.Thread(target=send_message)
send_thread.start(), client_socket.sendall(username.encode('utf-8'))

while True:
    try:
        message = client_socket.recv(1024).decode('utf-8')
        if message.startswith('There are currently') and message.endswith('other client(s) online.'): print(f'\n{message}\nEnter message: ', end='', flush=True)
        else: print(f'\n{message}'), print("Enter message: ", end='', flush=True)
    except ConnectionResetError: client_socket.close(), exit("\nConnection to the server was lost.")
