import os, msvcrt; from local_colorama import *; username_mode = 0

def account_validation(username): return True if os.path.exists(os.path.join('accounts', f'{username}.txt')) and open(os.path.join('accounts', f'{username}.txt')).read() in ['Offline', 'Online'] else False
def account_username(username, mode): # mode 1: create a account and place it 'online', mode 2: create a account and place it 'offline', mode 3: open an already exisiting account and place it as 'online', mode 4: open an already existing account and place it as 'offline'
    global username_mode; username_mode = mode
    if mode==1: f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Online'); f.close()
    elif mode==2: f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Offline'); f.close()
    elif mode==3 and open(os.path.join('accounts', f'{username}.txt'), 'r').read() == 'Offline': f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Online'); f.close()
    elif mode==4 and open(os.path.join('accounts', f'{username}.txt'), 'r').read() == 'Online': f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Offline'); f.close()
    else: print('Error with account. Please validate that your account is【configured】correctly.')
def account_password(username, password, mode): # mode 1: create a account's password and place it as the password without verifying, mode 2: open an already exisiting account and change the password to the new password
    if mode==1: f = open(os.path.join('passwords', f'{username}.txt'), 'w'); f.write(password); f.close()
    elif mode==2 and open(os.path.join('passwords', f'{username}.txt'), 'r').read() == 'Offline': f = open(os.path.join('passwords', f'{username}.txt'), 'w'); f.write(password); f.close()
    else: print('Error with your account. Please validate that your account is【configured】correctly.')

nospace=False
def username_creation():
    while True:
        global nospace
        username = input(Fore.BLUE + Style.BRIGHT + "Please enter your username: " + Fore.WHITE + Style.RESET)
        for i in range(len(username)):
            if (nospace := True if username[i] == ' ' else False): break
        if not username: print(Fore.RED + Style.BRIGHT + 'Please actually create a username.' + Fore.WHITE + Style.RESET)
        if len(username)>16 or len(username)<3 or len(username)==3: print(Fore.RED + Style.BRIGHT + 'Please create a username under 16 characters and over 3 characters.' + Fore.WHITE + Style.RESET)
        if nospace==True: print(Fore.RED + Style.BRIGHT + 'Please create a username that doesn\'t contain any spaces.' + Fore.WHITE + Style.RESET)
        if username and len(username)<16 and len(username)>3 and len(username)!=3 and nospace == False:
            if os.path.exists(os.path.join('accounts', f'{username}.txt')): print('You have succsessfully logged into account: ' + Fore.RED + Style.BRIGHT + f'{username}' + Fore.WHITE + Style.RESET + '.'); account_username(username, 3)
            else: print('You have succsessfully created a new account called: ' + Fore.RED + Style.BRIGHT + f'{username}' + Fore.WHITE + Style.RESET + '.'); account_username(username, 1)
            return username

nospace=False
def password_creation(username):
    while True:
        global nospace
        print(Fore.BLUE + Style.BRIGHT + "Please enter your password: " + Fore.WHITE + Style.RESET, end='', flush=True)
        password = masked_input()
        for i in range(len(password)):
            if (nospace := True if password[i] == ' ' else False): break
        print()
        if not password: print(Fore.RED + Style.BRIGHT + 'Please actually create a password.' if username_mode in [1, 2] else Fore.RED + Style.BRIGHT + 'Please use an actual password' + Fore.WHITE + Style.RESET)
        if len(password)>17 or len(password)<3 or len(password)==3: print(Fore.RED + Style.BRIGHT + 'Please create a password under 16 characters and over 3 characters.' if username_mode in [1, 2] else Fore.RED + Style.BRIGHT + 'Your password is under 16 characters and over 3 characters long.' + Fore.WHITE + Style.RESET)
        if nospace==True: print(Fore.RED + Style.BRIGHT + 'Please create a password that doesn\'t contain any spaces.' if username_mode in [1, 2] else Fore.RED + Style.BRIGHT + Fore.RED + Style.BRIGHT + 'Your password doesn\'t contain any spaces.' + Fore.WHITE + Style.RESET)
        if password and len(password)<16 and len(password)>3 and len(password)!=3 and nospace == False and username_mode in [1, 2] and not os.path.exists(os.path.join('passwords', f'{username}.txt')):
            print('You have succsessfully created a new account using password: ' + Fore.RED + Style.BRIGHT + f'{password}' + Fore.WHITE + Style.RESET + '.'); account_password(username, password, 1)
            return password
        if os.path.exists(os.path.join('passwords', f'{username}.txt')) and password and len(password)<16 and len(password)>3 and len(password)!=3 and nospace == False and password == open(os.path.join('passwords', f'{username}.txt')).read():
            print('You have succsessfully logged into account using password: ' + Fore.RED + Style.BRIGHT + f'{password}' + Fore.WHITE + Style.RESET + '.') if password == open(os.path.join('passwords', f'{username}.txt')).read() else print('Incorrect password. Cannot validate you (somehow you managed to get this error message while there\'s already a check for it.).')#; account_password(username, password, 2)
            return password
        else: print('' + Fore.RED + Style.BRIGHT + 'Incorect password' + Fore.WHITE + Style.RESET + ', please try again with a different password or reset your password.')

def masked_input():
    input_chars = []
    while True:
        char = msvcrt.getch()
        if char in {b' ', b'\x00', b'\xe0', b'\x09', b'\1b', b'\2e', b'\3b', b'\3c', b'\3d', b'\3e', b'\3f', b'\x40', b'\x41', b'\x42', b'\x43', b'\x44', b'\x85', b'\x86', b'\x47', b'\x4f', b'\x48', b'\x50', b'\x4b', b'\x4d', b'\x49', b'\x51', b'\x52', b'\x53'}: msvcrt.getch(); continue
        if char == b'\r': break
        elif char == b'\b':
            if input_chars: input_chars.pop(); print('\b \b', end='', flush=True)
        else: input_chars.append(char.decode('utf-8')); print('*', end='', flush=True)
    return ''.join(input_chars)
