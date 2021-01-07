import sqlite3
import os.path

from security import encrypt_text, decrypt_text, get_hashed_key, generate_salt

def get_database_path():
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    return os.path.join(BASE_DIR, 'credentials.db')

def get_user_identity():
    query = 'SELECT * FROM Identification LIMIT 1'
    rows = execute_query(query)
    return rows[0] if rows else None

def is_verified(entered_pass, user_info):
    hashed_master_pass = user_info[1]
    hashed_entered_pass = get_hashed_key(entered_pass, user_info[2])
    return hashed_master_pass == hashed_entered_pass

def execute_query(query, values = None):
    try:
        db_path = get_database_path()
        with sqlite3.connect(db_path) as conn:
            cur = conn.cursor()

            if values is None:
                cur.execute(query)
            else:
                cur.execute(query, values)

            return cur.fetchall()
    except sqlite3.Error as error:
        print(error)
    
def save_portfolio(name, master_pass):
    salt = generate_salt()
    hashed_pass = get_hashed_key(master_pass, salt)

    query = 'INSERT INTO Identification (name, masterhash, salt) VALUES (?, ?, ?);'
    values = (name, hashed_pass, salt)
    execute_query(query, values)

def find_credential(website):
    query = 'SELECT * FROM Credentials WHERE website = ? COLLATE NOCASE;'
    rows = execute_query(query, (website,))

    if rows:
        print('Search successful.')
        display_database_credential(rows)
    else:
        print('No matching website was found.')

def save_credential(website, username, password):
    encrypted_pass, key = encrypt_text(password)
    query = 'INSERT INTO Credentials (website, username, password, keycode) VALUES (?, ?, ?, ?);'
    values = (website, username, encrypted_pass, key)
    execute_query(query, values)

    print('\nNew login details created.')
    display_credential(website, username, password)

def list_credential():
    query = 'SELECT * FROM Credentials ORDER BY website;'
    rows = execute_query(query)

    if rows:
        display_database_credential(rows)
    else:
        print('No login credentials found.')

def find_email(email):
    query = 'SELECT * FROM Credentials WHERE username = ? ORDER BY website;'
    rows = execute_query(query, (email,))

    if rows:
        display_database_credential(rows)
    else:
        print('This email has not been registered.')
        
def delete_credential(website):
    query = 'SELECT * FROM Credentials WHERE website = ? COLLATE NOCASE;'
    rows = execute_query(query, (website,))

    if rows:
        print('Search successful.')
        num_of_matches = len(rows)
        id_map = [row[0] for row in rows]
        id_to_delete = id_map[0]
        
        if num_of_matches > 1:
            display_database_credential(rows)
            chosen_match = select_match(num_of_matches) - 1
            id_to_delete = id_map[chosen_match]

        query = 'SELECT * FROM Credentials WHERE id = ?;'
        selected = execute_query(query, (id_to_delete,))
        display_database_credential(selected)
        prompt_row_delete(id_to_delete)

    else:
        print('No matching website was found.')

def prompt_row_delete(row_id):
    choice = input('\n[!] Are you sure you want to delete this? Enter [y/n]: ').lower()

    if choice == 'y':
        print('Successfully deleted chosen credentials.')
        query = 'DELETE FROM Credentials WHERE id = ?;'
        execute_query(query, (row_id,))
    elif choice == 'n':
        print('Cancelling deletion.')
    else:
        print('Invalid option. Cancelling deletion.')

def select_match(matches):
    try:
        selection = int(input('\nEnter the match number you want to delete: '))
        if selection < 1 or selection > matches:
            print('Not a valid selection.')
            return select_match(matches)
        else:
            return selection
    except:
        print('Not a valid selection.')
        return select_match(matches)

def display_database_credential(rows):
    for count, row in enumerate(rows):
        password = decrypt_text(row[3], row[4])
        if len(rows) > 1:
            display_credential(row[1], row[2], password, count + 1)
        else:
            display_credential(row[1], row[2], password)

def display_credential(website, username, password, count = 0):
    if count != 0:
        print('\n[{}] '.format(count), end='')
    else:
        print('\n    ', end='')

    print('[' + website.upper() + ']')
    print('    User: ' + username)
    print('    Pass: ' + password)
