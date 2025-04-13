import sqlite3
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from base64 import b64encode, b64decode
import os

key = os.urandom(32)

def encrypt_data(data):
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(data.encode(), AES.block_size))
    iv = b64encode(cipher.iv).decode('utf-8')
    ct = b64encode(ct_bytes).decode('utf-8')
    return iv, ct

def decrypt_data(iv, ct):
    iv = b64decode(iv)
    ct = b64decode(ct)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size).decode('utf-8')
    return pt

def init_db():
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT,
                        email TEXT UNIQUE,
                        phone TEXT UNIQUE,
                        password TEXT
                    )''')
    conn.commit()
    conn.close()

def add_user(name, email, phone, password):
    encrypted_email_iv, encrypted_email = encrypt_data(email)
    encrypted_phone_iv, encrypted_phone = encrypt_data(phone)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (name, email, phone, password) VALUES (?, ?, ?, ?)", 
                   (name, encrypted_email, encrypted_phone, password))
    conn.commit()
    conn.close()

def get_user_by_email_or_phone(identifier):
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE email = ? OR phone = ?", (identifier, identifier))
    user = cursor.fetchone()
    conn.close()

    if user:
        decrypted_email = decrypt_data(user[1], user[2])
        decrypted_phone = decrypt_data(user[3], user[4])
        return user[0], decrypted_email, decrypted_phone, user[5]
    return None
