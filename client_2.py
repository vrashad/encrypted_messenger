import socket
import threading
from cryptography.fernet import Fernet
import base64
import hashlib

def generate_key(password):
    return base64.urlsafe_b64encode(hashlib.sha256(password.encode()).digest())

def encrypt_message(message, key):
    return Fernet(key).encrypt(message.encode()).decode()

def decrypt_message(encrypted_message, key):
    return Fernet(key).decrypt(encrypted_message.encode()).decode()

def receive_messages(sock, key, encrypt):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                break
            if encrypt:
                message = decrypt_message(data.decode(), key)
            else:
                message = data.decode()
            print("Qəbul edilən mesaj:", message)
        except Exception as e:
            print("Mesajı deşifrə etmək və ya qəbul etmək alınmadı:", str(e))
            break

def connect_to_server(host, port, encrypt, key):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((host, port))
    threading.Thread(target=receive_messages, args=(sock, key, encrypt)).start()
    while True:
        message = input("Mesajınızı daxil edin (dayandırmaq üçün 'quit' daxil edin): ")
        if message.lower() == "quit":
            break
        if encrypt:
            message = encrypt_message(message, key)
        sock.sendall(message.encode())
    sock.close()

if __name__ == "__main__":
    host, port = input("Serverin ünvanını daxil edin (ip:port): ").split(':')
    encrypt = input("Mesajlar şifrələnsin? (y/n): ").lower() == 'y'
    key = generate_key(input("Şifrələmə açarını daxil edin: ")) if encrypt else None
    connect_to_server(host, int(port), encrypt, key)
