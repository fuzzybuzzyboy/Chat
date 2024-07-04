import os

def account(username, mode): # mode 1: create a account and place it 'online', mode 2: create a account and place it 'offline', mode 3: open an already exisiting account and place it as 'online', mode 4: open an already existing account and place it as 'offline'
    if mode==1: f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Online'); f.close()
    elif mode==2: f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Offline'); f.close()
    elif mode==3 and open(os.path.join('accounts', f'{username}.txt'), 'r').read() == 'Offline': f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Online'); f.close()
    elif mode==4 and open(os.path.join('accounts', f'{username}.txt'), 'r').read() == 'Online': f = open(os.path.join('accounts', f'{username}.txt'), 'w'); f.write('Offline'); f.close()
    else: print('Error changing account. Please validate that your account is configured correctly.')