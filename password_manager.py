from menu import menu, retrieve, create, delete, itemize, connected, setup_login
from database_manager import get_user_identity, is_verified

def main():
    print('_' * 18)
    print('\n Password Manager\n ver. 1.1')
    print('_' * 18)

    user_info = get_user_identity()
    if user_info:
        entered_pass = input('\nEnter the master password: ')
        if is_verified(entered_pass, user_info):
            print('Password accepted.')
            print('\nWelcome, {}.'.format(user_info[0]))
        else:
            print('Password not accepted.')
            exit()
    else:
        setup_login()
        input('\nPress enter to continue: ')

    while True:
        option = menu()

        if option == '1':
            retrieve()
        elif option == '2':
            create()
        elif option == '3':
            delete()
        elif option == '4':
            itemize()
        elif option == '5':
            connected()
        elif option == 'x':
            exit()
        else:
            print('Invalid option.')

        input('\nPress enter to continue: ')

if __name__ == '__main__':
    main()
    