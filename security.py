# Master password hashers
from hashlib import pbkdf2_hmac
from os import urandom
from base64 import b64encode

# Password encryption into database
from cryptography.fernet import Fernet

# Creates a hash with a regular string password and salt
def get_hashed_key(master_pass, salt):
    key = pbkdf2_hmac('sha256', master_pass.encode('utf-8'), salt, 100000)
    return key.hex()

def generate_salt():
    random = urandom(64)
    return b64encode(random)

# Encrypts plaintext
def encrypt_text(plaintext):
    key = Fernet.generate_key()
    cipher = Fernet(key)
    encrypted = cipher.encrypt(plaintext.encode('utf-8'))
    return (encrypted.decode('utf-8'), key.decode('utf-8'))

# Decrypts plaintext with the saved key
def decrypt_text(encrypted, key):
    cipher = Fernet(key)
    decrypted = cipher.decrypt(encrypted.encode('utf-8'))
    return decrypted.decode('utf-8')
