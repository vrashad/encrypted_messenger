import socket
import threading

def client_thread(conn, clients):
    while True:
        try:
            data = conn.recv(1024)
            if not data:
                break
            for c in clients:
                if c != conn:
                    c.sendall(data)
        except:
            break
    conn.close()
    clients.remove(conn)
    print("Client disconnected")

def start_server(host, port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen()
    clients = []
    print("Serverin dinlədiyi ünvan", host, port)
    while True:
        conn, addr = server_socket.accept()
        clients.append(conn)
        print(f"{addr} qoşulub")
        threading.Thread(target=client_thread, args=(conn, clients)).start()

if __name__ == "__main__":
    start_server('127.0.0.1', 999)
