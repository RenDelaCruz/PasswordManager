from database_manager import find_credential, save_credential, delete_credential, list_credential, find_email, save_portfolio

def menu():
    print('_' * 40 + '\n')
    print(' ' * 7 + 'Menu' + ' ' * 29 + '\n')
    print(' [1] - Retrieve a password')
    print(' [2] - Create new login credentials')
    print(' [3] - Delete a password')
    print(' [4] - List all login credentials') 
    print(' [5] - Find sites connected to an email')
    print(' [x] - Exit')
    print('_' * 40)
    return input('\nEnter: ').lower()

def retrieve():
    print('Retrieving a password.')
    website = input('\nEnter the website: ')
    find_credential(website)

def create():
    print('Creating new login credentials.')
    website = input('\nEnter the website for the login: ')
    username = input('Enter the username or email: ')
    password = input('Enter the password for this website: ')
    save_credential(website, username, password)

def delete():
    print('Deleting a password.')
    website = input('\nEnter the website whose password will be deleted: ')
    delete_credential(website)

def itemize():
    print('Listing all credentials.')
    list_credential()

def connected():
    print('Finding sites connected to an email.')
    email = input('\nEnter the email to search: ').lower()
    find_email(email)

def setup_login():
    print('\nSetting up new password portfolio.')
    name = input('\nEnter your name: ')
    master_pass = input('Enter your master password: ')
    confirm_pass = input('Enter your password again: ')

    if master_pass != confirm_pass:
        print('\nPasswords do not match. Try setup again.')
        return setup_login()
    
    print('\nSuccessfully created new password portfolio.')
    print('\nNOTE: Do not forget your master password. It is needed to access all your other passwords.')
    print(' '*6 + 'Your master password is securely hashed, so the plain password itself is never stored.')
    print(' '*6 + 'Furthermore, all your passwords will be encrypted. If possible, save a copy of ')
    print(' '*6 + '"credentials.db" as a backup of your password database.')

    save_portfolio(name, master_pass)
